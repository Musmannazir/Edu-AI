"""API v1 Router"""
from fastapi import APIRouter
from app.api.v1.endpoints import (
    transcription,
    notes,
    flashcards,
    quizzes,
    tutor,
    subjects,
    study_plans
)

api_router = APIRouter()

api_router.include_router(transcription.router, prefix="/transcription", tags=["transcription"])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
api_router.include_router(flashcards.router, prefix="/flashcards", tags=["flashcards"])
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])
api_router.include_router(tutor.router, prefix="/tutor", tags=["tutor"])
api_router.include_router(subjects.router, prefix="/subjects", tags=["subjects"])
api_router.include_router(study_plans.router, prefix="/study-plans", tags=["study-plans"])
