"""
Flashcard endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.nlp_service import nlp_service

router = APIRouter()


class GenerateFlashcardsRequest(BaseModel):
    """Request model for generating flashcards"""
    content: str
    count: int = 10


class FlashcardResponse(BaseModel):
    """Response model for a flashcard"""
    question: str
    answer: str


@router.post("/generate", response_model=List[FlashcardResponse])
async def generate_flashcards(request: GenerateFlashcardsRequest):
    """
    Generate flashcards from content
    """
    try:
        flashcards = await nlp_service.generate_flashcards(request.content, request.count)
        return [FlashcardResponse(**card) for card in flashcards]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
