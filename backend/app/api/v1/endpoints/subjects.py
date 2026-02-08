"""
Subject endpoints (placeholder for database operations)
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_subjects():
    """List all subjects"""
    return {"message": "Subject listing - to be implemented with database"}


@router.post("/")
async def create_subject():
    """Create a new subject"""
    return {"message": "Subject creation - to be implemented with database"}


@router.get("/{subject_id}")
async def get_subject(subject_id: int):
    """Get subject by ID"""
    return {"message": f"Get subject {subject_id} - to be implemented with database"}
