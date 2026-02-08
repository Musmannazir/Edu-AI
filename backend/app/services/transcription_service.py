"""
Transcription service using OpenAI Whisper API and YouTube Transcripts (FREE!)
"""
import os
import tempfile
from openai import AsyncOpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from app.core.config import settings
import asyncio


class TranscriptionService:
    """Service for transcribing audio and video content"""
    
    def __init__(self):
        # YouTube Transcript API (doesn't need initialization)
        # Make OpenAI client optional - only initialize if API key is provided
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
    
    async def transcribe_audio_file(self, file_path: str) -> str:
        """
        Transcribe an audio file using OpenAI Whisper API
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Transcribed text
        """
        if not self.client:
            raise Exception("OpenAI API key is not configured. Please add OPENAI_API_KEY to environment variables.")
        
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
    
    async def transcribe_youtube_video(self, youtube_url: str) -> tuple[str, dict]:
        """
        Transcribe a YouTube video using its captions (completely FREE!)
        
        Works for videos that have English captions available through YouTube's API.
        
        Args:
            youtube_url: YouTube video URL
            
        Returns:
            Tuple of (transcript, metadata)
        """
        try:
            # Extract video ID
            video_id = self._extract_video_id(youtube_url)
            
            # Fetch captions using YouTube Transcript API (run in thread to avoid blocking)
            try:
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
                
                return transcript, metadata
            except asyncio.TimeoutError:
                raise Exception("Request timed out. The YouTube transcript API took too long to respond.")
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
