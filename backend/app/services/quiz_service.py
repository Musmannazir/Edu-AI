"""
Quiz generation and adaptive learning service
"""
from openai import AsyncOpenAI
from typing import List, Dict, Optional
import json
from app.core.config import settings


class QuizService:
    """Service for generating and managing adaptive quizzes"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def generate_quiz(
        self,
        content: str,
        num_questions: int = 10,
        difficulty: str = "medium",
        question_types: List[str] = None
    ) -> List[Dict]:
        """
        Generate quiz questions from content
        
        Args:
            content: Content to generate quiz from
            num_questions: Number of questions to generate
            difficulty: Difficulty level (easy, medium, hard)
            question_types: Types of questions (mcq, true_false, short_answer)
            
        Returns:
            List of question dictionaries
        """
        if question_types is None:
            question_types = ["mcq", "true_false"]
        
        types_str = ", ".join(question_types)
        
        prompt = f"""Generate {num_questions} {difficulty} difficulty quiz questions from the following content.
        
Question types to include: {types_str}

For multiple choice questions (mcq):
- Provide 4 options (A, B, C, D)
- Mark the correct answer
- Include plausible distractors

For true/false questions:
- Include a statement and correct answer

For short answer questions:
- Include the question and a model answer

Content:
{content}

Generate questions in JSON format with fields: type, question, options (for mcq), correct_answer, explanation"""

        response = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert educator creating effective quiz questions. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get('questions', [])
    
    async def generate_adaptive_quiz(
        self,
        weak_topics: List[str],
        user_level: str,
        previous_performance: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Generate an adaptive quiz based on weak areas and performance
        
        Args:
            weak_topics: List of topics where user needs practice
            user_level: User's current level
            previous_performance: Previous quiz performance data
            
        Returns:
            List of adaptive question dictionaries
        """
        performance_context = ""
        if previous_performance:
            performance_context = f"\nPrevious performance: {json.dumps(previous_performance)}"
        
        prompt = f"""Generate an adaptive quiz focusing on these weak topics: {', '.join(weak_topics)}
        
User level: {user_level}{performance_context}

Generate 10 questions that:
1. Start easier and gradually increase difficulty
2. Focus heavily on the weak topics
3. Include explanations for incorrect answers
4. Help identify specific misconceptions

Return as JSON with fields: question, options, correct_answer, difficulty, topic, explanation"""

        response = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert at creating adaptive assessments that help students improve. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get('questions', [])
    
    def evaluate_quiz_attempt(
        self,
        questions: List[Dict],
        user_answers: List[str]
    ) -> Dict:
        """
        Evaluate a quiz attempt and identify weak areas
        
        Args:
            questions: List of quiz questions
            user_answers: List of user's answers
            
        Returns:
            Evaluation results with score and weak areas
        """
        correct = 0
        total = len(questions)
        weak_topics = {}
        results = []
        
        for i, (question, answer) in enumerate(zip(questions, user_answers)):
            is_correct = answer == question.get('correct_answer')
            if is_correct:
                correct += 1
            else:
                topic = question.get('topic', 'general')
                weak_topics[topic] = weak_topics.get(topic, 0) + 1
            
            results.append({
                'question_index': i,
                'correct': is_correct,
                'user_answer': answer,
                'correct_answer': question.get('correct_answer'),
                'explanation': question.get('explanation', '')
            })
        
        score = (correct / total) * 100 if total > 0 else 0
        
        # Identify topics with < 60% accuracy as weak
        weak_areas = [
            topic for topic, errors in weak_topics.items()
            if errors / total > (1 - settings.WEAK_AREA_THRESHOLD)
        ]
        
        return {
            'score': score,
            'correct': correct,
            'total': total,
            'weak_areas': weak_areas,
            'results': results,
            'passed': score >= (settings.MIN_QUIZ_ACCURACY * 100)
        }
    
    async def get_question_explanation(
        self,
        question: str,
        correct_answer: str,
        user_answer: str,
        learning_style: str = "visual"
    ) -> str:
        """
        Generate a personalized explanation for a quiz question
        
        Args:
            question: The quiz question
            correct_answer: The correct answer
            user_answer: User's answer
            learning_style: User's learning style
            
        Returns:
            Personalized explanation
        """
        style_prompts = {
            "visual": "Use analogies, diagrams descriptions, and visual metaphors",
            "auditory": "Use conversational tone and verbal explanations",
            "kinesthetic": "Use practical examples and real-world applications",
            "reading": "Use detailed written explanations with examples"
        }
        
        style_instruction = style_prompts.get(learning_style, style_prompts["visual"])
        
        prompt = f"""Explain why the answer to this question is '{correct_answer}' and not '{user_answer}'.

Question: {question}

{style_instruction} in your explanation.
Keep it concise but thorough."""

        response = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": f"You are a patient tutor explaining concepts to a {learning_style} learner."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content


# Singleton instance
quiz_service = QuizService()
