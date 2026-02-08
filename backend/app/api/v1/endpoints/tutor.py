"""
AI Tutor endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from app.services.ai_tutor_service import ai_tutor_service

router = APIRouter()


class TutorQuestionRequest(BaseModel):
    """Request model for tutor question"""
    user_id: int
    question: str
    context: Optional[str] = None
    learning_style: str = "visual"
    subject: Optional[str] = None


class ExplainConceptRequest(BaseModel):
    """Request model for concept explanation"""
    concept: str
    depth_level: str = "intermediate"
    learning_style: str = "visual"
    include_examples: bool = True


class StudyPlanRequest(BaseModel):
    """Request model for study plan generation"""
    weak_areas: List[str]
    available_hours_per_week: int
    goals: List[str]
    deadline: Optional[str] = None


class RecommendResourcesRequest(BaseModel):
    """Request model for resource recommendations"""
    topic: str
    current_level: str
    learning_style: str = "visual"


@router.post("/ask")
async def ask_tutor(request: TutorQuestionRequest):
    """
    Ask the AI tutor a question
    """
    try:
        response = await ai_tutor_service.get_tutor_response(
            user_id=request.user_id,
            question=request.question,
            context=request.context,
            learning_style=request.learning_style,
            subject=request.subject
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain")
async def explain_concept(request: ExplainConceptRequest):
    """
    Get explanation for a concept
    """
    try:
        explanation = await ai_tutor_service.explain_concept(
            concept=request.concept,
            depth_level=request.depth_level,
            learning_style=request.learning_style,
            include_examples=request.include_examples
        )
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/study-plan")
async def generate_study_plan(request: StudyPlanRequest):
    """
    Generate a personalized study plan
    """
    try:
        plan = await ai_tutor_service.generate_study_plan(
            weak_areas=request.weak_areas,
            available_hours_per_week=request.available_hours_per_week,
            goals=request.goals,
            deadline=request.deadline
        )
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recommend-resources")
async def recommend_resources(request: RecommendResourcesRequest):
    """
    Get resource recommendations for a topic
    """
    try:
        resources = await ai_tutor_service.recommend_resources(
            topic=request.topic,
            current_level=request.current_level,
            learning_style=request.learning_style
        )
        return {"resources": resources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clear-history/{user_id}")
async def clear_conversation_history(user_id: int):
    """
    Clear conversation history for a user
    """
    try:
        ai_tutor_service.clear_conversation_history(user_id)
        return {"message": "Conversation history cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
