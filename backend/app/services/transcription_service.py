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


class TranscriptionService:
    """Service for transcribing audio and video content"""
    
    def __init__(self):
        # YouTube Transcript API (doesn't need initialization)
        # Make OpenAI client optional - only initialize if API key is provided
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
        self.whisper_model = None
        self.ffmpeg_path = self._get_ffmpeg_path()
    
    def _load_whisper_model(self, model_name: str = "base"):
        """Load local Whisper model (lazy loading)"""
        if self.whisper_model is None:
            print(f"Loading Whisper model '{model_name}'... This may take a moment on first run.")
            self.whisper_model = whisper.load_model(model_name)
        return self.whisper_model
    
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
    
    async def transcribe_audio_file(self, file_path: str) -> str:
        """
        Transcribe an audio file using OpenAI Whisper API or local Whisper (fallback)
        
        Tries to use OpenAI Whisper API first (if configured).
        Falls back to local Whisper model if API key is not configured or API calls fail.
        Both options are completely FREE!
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Transcribed text
        """
        # Try OpenAI API first (if configured)
        if self.client:
            try:
                print(f"Transcribing audio using OpenAI Whisper API...")
                with open(file_path, "rb") as audio_file:
                    transcript = await self.client.audio.transcriptions.create(
                        model=settings.WHISPER_MODEL,
                        file=audio_file,
                        response_format="text"
                    )
                return transcript
            except Exception as e:
                print(f"OpenAI API transcription failed ({str(e)}). Falling back to local Whisper...")
                # Continue to local fallback
        else:
            print(f"OpenAI API key not configured. Using local Whisper model...")
        
        # Fallback: Use local Whisper model (completely FREE!)
        try:
            return await self._transcribe_with_whisper(file_path)
        except Exception as e:
            raise Exception(f"Audio transcription failed: {str(e)}")
    
    async def transcribe_youtube_video(self, youtube_url: str) -> tuple[str, dict]:
        """
        Transcribe a YouTube video using captions (FREE) or local Whisper fallback
        
        First tries to fetch captions using the YouTube Transcript API (completely FREE!).
        If captions are not available, automatically falls back to downloading the audio
        and transcribing with local Whisper model (also completely FREE!).
        
        Args:
            youtube_url: YouTube video URL
            
        Returns:
            Tuple of (transcript, metadata)
        """
        try:
            # Extract video ID
            video_id = self._extract_video_id(youtube_url)
            
            # Try YouTube Transcript API first (fastest, no download needed)
            try:
                # Run get_transcript in a thread to avoid blocking the event loop (with 30 second timeout)
                transcript_list = await asyncio.wait_for(
                    asyncio.to_thread(
                        YouTubeTranscriptApi.get_transcript, 
                        video_id, 
                        languages=['en']
                    ),
                    timeout=30.0
                )
                # Combine transcript snippets into one string
                transcript = " ".join([item['text'] for item in transcript_list])
                
                # Get basic metadata
                metadata = self._get_youtube_metadata(youtube_url)
                metadata['transcription_method'] = 'youtube_api'
                
                return transcript, metadata
            except asyncio.TimeoutError:
                # YouTube API timeout - try fallback
                print(f"YouTube Transcript API timeout for {video_id}. Falling back to local Whisper transcription...")
                pass  # Continue to fallback
            except Exception as yt_error:
                # YouTube transcript not available - use fallback
                error_msg = str(yt_error)
                print(f"YouTube captions not available ({error_msg}). Falling back to local Whisper transcription...")
                pass  # Continue to fallback
            
            # Fallback: Download audio and transcribe with local Whisper
            print(f"Using local Whisper model to transcribe {youtube_url}...")
            transcript, metadata = await self._download_and_transcribe(youtube_url)
            metadata['transcription_method'] = 'local_whisper'
            return transcript, metadata
                
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
        """
        Download YouTube audio and transcribe it using local Whisper model (completely FREE!)
        
        Args:
            youtube_url: YouTube video URL
            
        Returns:
            Tuple of (transcript, metadata)
        """
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
            
            # Transcribe using local Whisper model (completely FREE!)
            print(f"Transcribing audio using local Whisper model...")
            transcript = await self._transcribe_with_whisper(audio_path)
            
            return transcript, metadata
    
    async def _transcribe_with_whisper(self, audio_path: str) -> str:
        """
        Transcribe audio using local Whisper model
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Transcribed text
        """
        try:
            # Load model (lazy loading - only loads once)
            model = self._load_whisper_model(model_name="base")
            
            # Run Whisper transcription in thread pool to avoid blocking event loop
            result = await asyncio.to_thread(model.transcribe, audio_path, language="en")
            
            transcript = result.get("text", "")
            return transcript.strip()
        except Exception as e:
            raise Exception(f"Whisper transcription failed: {str(e)}")
    
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
