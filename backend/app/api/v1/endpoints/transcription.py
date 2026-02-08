"""
Transcription endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional
from app.services.transcription_service import transcription_service
from app.services.nlp_service import nlp_service
import aiofiles
import os
from app.core.config import settings

router = APIRouter()


class YouTubeTranscribeRequest(BaseModel):
    """Request model for YouTube transcription"""
    url: HttpUrl
    generate_notes: bool = True
    subject: Optional[str] = None


class TranscriptionResponse(BaseModel):
    """Response model for transcription"""
    transcript: str
    notes: Optional[str] = None
    key_concepts: Optional[list] = None
    duration: Optional[int] = None
    title: Optional[str] = None


@router.post("/youtube", response_model=TranscriptionResponse)
async def transcribe_youtube(request: YouTubeTranscribeRequest):
    """
    Transcribe a YouTube video and optionally generate notes
    """
    try:
        # Transcribe video
        transcript, metadata = await transcription_service.transcribe_youtube_video(str(request.url))
        
        response_data = {
            "transcript": transcript,
            "title": metadata.get('title'),
            "duration": metadata.get('duration')
        }
        
        # Generate notes if requested
        if request.generate_notes:
            notes = await nlp_service.generate_notes(transcript, request.subject or "")
            concepts = await nlp_service.extract_key_concepts(transcript)
            response_data["notes"] = notes
            response_data["key_concepts"] = concepts
        
        return TranscriptionResponse(**response_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload", response_model=TranscriptionResponse)
async def transcribe_upload(
    file: UploadFile = File(...),
    subject: Optional[str] = None
):
    """
    Transcribe an uploaded audio/video file (notes generation disabled - requires paid OpenAI)
    """
    file_path = None
    try:
        # Save uploaded file
        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        # Transcribe using LOCAL Whisper (FREE!)
        transcript = await transcription_service.transcribe_audio_file(file_path)
        
        response_data = {"transcript": transcript}
        
        # Notes generation disabled (requires OpenAI API - paid)
        # Users can enable this by setting up OpenAI API key and uncommenting below:
        # if generate_notes:
        #     notes = await nlp_service.generate_notes(transcript, subject or "")
        #     concepts = await nlp_service.extract_key_concepts(transcript)
        #     response_data["notes"] = notes
        #     response_data["key_concepts"] = concepts
        
        return TranscriptionResponse(**response_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Clean up uploaded file
        if file_path and os.path.exists(file_path):
            try:
                import time
                time.sleep(0.1)  # Brief delay to ensure file is released
                os.remove(file_path)
            except Exception:
                pass  # Ignore cleanup errors


@router.post("/summarize")
async def summarize_transcript(transcript: str, max_length: int = 300):
    """
    Summarize a transcript
    """
    try:
        summary = await nlp_service.summarize_text(transcript, max_length)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
