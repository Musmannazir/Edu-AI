"""
Transcription service using OpenAI Whisper and YouTube Transcripts
"""
import os
import tempfile
import whisper
from openai import AsyncOpenAI
from typing import Optional
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from app.core.config import settings
import platform
import shutil
import asyncio
from functools import lru_cache


class TranscriptionService:
    """Service for transcribing audio and video content"""
    
    def __init__(self):
        # Initialize YouTube Transcript API
        self.youtube_api = YouTubeTranscriptApi()
        # Make OpenAI client optional - only initialize if API key is provided
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
        self.whisper_model = None
        self.ffmpeg_path = self._get_ffmpeg_path()
    
    def _get_ffmpeg_path(self) -> Optional[str]:
        """Get FFmpeg path for the system"""
        # Try to find ffmpeg in PATH
        ffmpeg = shutil.which('ffmpeg')
        if ffmpeg:
            return ffmpeg
        
        # Windows common paths
        if platform.system() == 'Windows':
            common_paths = [
                'C:\\ffmpeg\\bin\\ffmpeg.exe',
                'C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe',
                'C:\\Program Files (x86)\\ffmpeg\\bin\\ffmpeg.exe',
            ]
            for path in common_paths:
                if os.path.exists(path):
                    return path
        
        return None
    
    def _load_whisper_model(self, model_name: str = "base"):
        """Load local Whisper model (lazy loading)"""
        if self.whisper_model is None:
            print(f"Loading Whisper model '{model_name}'... This may take a moment on first run.")
            self.whisper_model = whisper.load_model(model_name)
        return self.whisper_model
    
    async def transcribe_audio_file(self, file_path: str) -> str:
        """
        Transcribe an audio file using LOCAL Whisper (FREE!)
        Falls back to OpenAI API only if local fails
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Transcribed text
        """
        # Try LOCAL Whisper first (FREE!)
        try:
            # Run in thread pool to avoid blocking
            transcript = await asyncio.to_thread(self._transcribe_with_local_whisper, file_path)
            return transcript
        except Exception as local_error:
            print(f"Local Whisper failed: {local_error}")
            
            # Only try OpenAI if we have a client configured
            if not self.client:
                raise Exception(f"Local Whisper transcription failed and OpenAI API key is not configured. Error: {str(local_error)}. Please ensure audio file is valid.")
            
            # Fallback to OpenAI API
            try:
                with open(file_path, "rb") as audio_file:
                    transcript = await self.client.audio.transcriptions.create(
                        model=settings.WHISPER_MODEL,
                        file=audio_file,
                        response_format="text"
                    )
                return transcript
            except Exception as e:
                raise Exception(f"Transcription failed: {str(e)}")
    
    def _transcribe_with_local_whisper(self, file_path: str) -> str:
        """Transcribe using local Whisper model"""
        model = self._load_whisper_model("base")  # base model is fast and accurate
        result = model.transcribe(file_path)
        return result["text"]
    
    async def transcribe_youtube_video(self, youtube_url: str) -> tuple[str, dict]:
        """
        Transcribe a YouTube video using its captions (completely FREE!)
        
        Args:
            youtube_url: YouTube video URL
            
        Returns:
            Tuple of (transcript, metadata)
        """
        try:
            # Extract video ID
            video_id = self._extract_video_id(youtube_url)
            
            # Run the synchronous YouTube API call in a thread pool to avoid blocking
            try:
                # Run fetch in a thread to avoid blocking the event loop (with 30 second timeout)
                transcript_data = await asyncio.wait_for(
                    asyncio.to_thread(
                        self.youtube_api.fetch, 
                        video_id, 
                        languages=['en']
                    ),
                    timeout=30.0
                )
                # Access the snippets attribute and combine transcript text
                transcript = " ".join([snippet.text for snippet in transcript_data.snippets])
                
                # Get basic metadata
                metadata = self._get_youtube_metadata(youtube_url)
                
                return transcript, metadata
            except asyncio.TimeoutError:
                raise Exception("Request timed out. The YouTube transcript API took too long to respond. Please try again.")
            except Exception as yt_error:
                # YouTube transcript not available
                error_msg = str(yt_error)
                raise Exception(f"Transcript not available: {error_msg}. This video may not have English captions.")
                
        except Exception as e:
            raise Exception(f"YouTube transcription failed: {str(e)}")
    
    def _extract_video_id(self, youtube_url: str) -> str:
        """Extract video ID from YouTube URL"""
        if "v=" in youtube_url:
            return youtube_url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in youtube_url:
            return youtube_url.split("youtu.be/")[1].split("?")[0]
        else:
            raise ValueError("Invalid YouTube URL")
    
    def _get_youtube_metadata(self, youtube_url: str) -> dict:
        """Get YouTube video metadata - simplified version without yt-dlp"""
        try:
            # Extract video ID
            video_id = self._extract_video_id(youtube_url)
            # Return basic metadata - could be enhanced with pytube or other libraries
            return {
                'title': f'Video: {video_id}',
                'url': youtube_url,
                'video_id': video_id
            }
        except Exception as e:
            return {'error': str(e)}
    
    async def _download_and_transcribe(self, youtube_url: str) -> tuple[str, dict]:
        """Download YouTube audio and transcribe it"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download audio
            audio_path = os.path.join(temp_dir, "audio.mp3")
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }],
                'outtmpl': audio_path.replace('.mp3', ''),
                'quiet': True,
                'ffmpeg_location': self.ffmpeg_path if self.ffmpeg_path else None
            }
            
            if not self.ffmpeg_path:
                ydl_opts.pop('ffmpeg_location')
            
            metadata = {}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=True)
                metadata = {
                    'title': info.get('title'),
                    'duration': info.get('duration'),
                    'uploader': info.get('uploader'),
                    'upload_date': info.get('upload_date')
                }
            
            # Transcribe
            transcript = await self.transcribe_audio_file(audio_path)
            
            return transcript, metadata
    
    async def transcribe_live_audio(self, audio_chunks: list) -> str:
        """
        Transcribe live audio in real-time
        
        Args:
            audio_chunks: List of audio data chunks
            
        Returns:
            Transcribed text
        """
        # This would be implemented with streaming audio processing
        # For now, we'll save chunks to a temp file and transcribe
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            # Combine audio chunks
            # Implementation depends on audio format
            temp_path = temp_file.name
            
        try:
            transcript = await self.transcribe_audio_file(temp_path)
            return transcript
        finally:
            os.unlink(temp_path)


# Singleton instance
transcription_service = TranscriptionService()
