"""
Notes endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.nlp_service import nlp_service

router = APIRouter()


class GenerateNotesRequest(BaseModel):
    """Request model for generating notes"""
    content: str
    subject: Optional[str] = None


class NotesResponse(BaseModel):
    """Response model for notes"""
    notes: str
    summary: Optional[str] = None


@router.post("/generate", response_model=NotesResponse)
async def generate_notes(request: GenerateNotesRequest):
    """
    Generate structured notes from content
    """
    try:
        notes = await nlp_service.generate_notes(request.content, request.subject or "")
        summary = await nlp_service.summarize_text(request.content, max_length=150)
        
        return NotesResponse(notes=notes, summary=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract-concepts")
async def extract_concepts(content: str):
    """
    Extract key concepts from content
    """
    try:
        concepts = await nlp_service.extract_key_concepts(content)
        return {"concepts": concepts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
