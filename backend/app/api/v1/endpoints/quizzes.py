"""
Quiz endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from app.services.quiz_service import quiz_service

router = APIRouter()


class GenerateQuizRequest(BaseModel):
    """Request model for generating quiz"""
    content: str
    num_questions: int = 10
    difficulty: str = "medium"
    question_types: Optional[List[str]] = None


class EvaluateQuizRequest(BaseModel):
    """Request model for evaluating quiz"""
    questions: List[Dict]
    user_answers: List[str]


class AdaptiveQuizRequest(BaseModel):
    """Request model for adaptive quiz"""
    weak_topics: List[str]
    user_level: str
    previous_performance: Optional[Dict] = None


@router.post("/generate")
async def generate_quiz(request: GenerateQuizRequest):
    """
    Generate a quiz from content
    """
    try:
        questions = await quiz_service.generate_quiz(
            content=request.content,
            num_questions=request.num_questions,
            difficulty=request.difficulty,
            question_types=request.question_types
        )
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/evaluate")
async def evaluate_quiz(request: EvaluateQuizRequest):
    """
    Evaluate a quiz attempt
    """
    try:
        results = quiz_service.evaluate_quiz_attempt(
            questions=request.questions,
            user_answers=request.user_answers
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/adaptive")
async def generate_adaptive_quiz(request: AdaptiveQuizRequest):
    """
    Generate an adaptive quiz based on weak areas
    """
    try:
        questions = await quiz_service.generate_adaptive_quiz(
            weak_topics=request.weak_topics,
            user_level=request.user_level,
            previous_performance=request.previous_performance
        )
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain")
async def explain_question(
    question: str,
    correct_answer: str,
    user_answer: str,
    learning_style: str = "visual"
):
    """
    Get explanation for a quiz question
    """
    try:
        explanation = await quiz_service.get_question_explanation(
            question=question,
            correct_answer=correct_answer,
            user_answer=user_answer,
            learning_style=learning_style
        )
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
