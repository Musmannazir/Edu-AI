"""
AI Tutor service for personalized learning assistance
"""
from openai import AsyncOpenAI
from typing import List, Dict, Optional
import json
from app.core.config import settings


class AITutorService:
    """Service for AI-powered tutoring and personalized learning"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.conversation_history = {}
    
    async def get_tutor_response(
        self,
        user_id: int,
        question: str,
        context: Optional[str] = None,
        learning_style: str = "visual",
        subject: Optional[str] = None
    ) -> str:
        """
        Get AI tutor response to student question
        
        Args:
            user_id: User ID for conversation context
            question: Student's question
            context: Additional context (notes, lecture content, etc.)
            learning_style: Student's learning style
            subject: Subject being studied
            
        Returns:
            Tutor's response
        """
        # Initialize conversation history for user if not exists
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        # Build system prompt based on learning style
        style_instructions = {
            "visual": "Use visual descriptions, analogies, and suggest diagrams. Structure information hierarchically.",
            "auditory": "Use conversational tone, explain things step-by-step verbally, use rhythm in explanations.",
            "kinesthetic": "Focus on practical examples, hands-on applications, and real-world scenarios.",
            "reading": "Provide detailed written explanations, definitions, and written examples."
        }
        
        style_instruction = style_instructions.get(learning_style, style_instructions["visual"])
        subject_context = f"specializing in {subject}" if subject else ""
        
        system_prompt = f"""You are a patient, encouraging AI tutor {subject_context}.
        
Teaching approach:
- {style_instruction}
- Break down complex topics into manageable chunks
- Use the Socratic method when appropriate
- Encourage critical thinking
- Provide examples and analogies
- Check for understanding
- Be supportive and encouraging

Remember: You're helping the student learn, not just giving answers."""

        # Build messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add context if provided
        if context:
            messages.append({
                "role": "system",
                "content": f"Reference material:\n{context}"
            })
        
        # Add conversation history (last 5 exchanges)
        messages.extend(self.conversation_history[user_id][-10:])
        
        # Add current question
        messages.append({"role": "user", "content": question})
        
        # Get response
        response = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        answer = response.choices[0].message.content
        
        # Update conversation history
        self.conversation_history[user_id].append({"role": "user", "content": question})
        self.conversation_history[user_id].append({"role": "assistant", "content": answer})
        
        return answer
    
    async def explain_concept(
        self,
        concept: str,
        depth_level: str = "intermediate",
        learning_style: str = "visual",
        include_examples: bool = True
    ) -> str:
        """
        Explain a concept in detail
        
        Args:
            concept: Concept to explain
            depth_level: beginner, intermediate, or advanced
            learning_style: Student's learning style
            include_examples: Whether to include examples
            
        Returns:
            Detailed explanation
        """
        depth_instructions = {
            "beginner": "Explain in simple terms, assume no prior knowledge",
            "intermediate": "Provide moderate detail with some technical terms",
            "advanced": "Use technical terminology and dive deep into nuances"
        }
        
        depth_instruction = depth_instructions.get(depth_level, depth_instructions["intermediate"])
        examples_instruction = "Include practical examples." if include_examples else ""
        
        prompt = f"""Explain the concept of '{concept}'.

Level: {depth_level}
{depth_instruction}
{examples_instruction}

Tailor explanation for {learning_style} learner.

Provide a clear, comprehensive explanation:"""

        response = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert educator explaining concepts clearly."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    async def generate_study_plan(
        self,
        weak_areas: List[str],
        available_hours_per_week: int,
        goals: List[str],
        deadline: Optional[str] = None
    ) -> Dict:
        """
        Generate a personalized study plan
        
        Args:
            weak_areas: Topics needing improvement
            available_hours_per_week: Study time available
            goals: Learning goals
            deadline: Optional deadline for goals
            
        Returns:
            Study plan dictionary
        """
        deadline_str = f"\nDeadline: {deadline}" if deadline else ""
        
        prompt = f"""Create a personalized study plan with these details:

Weak areas to focus on: {', '.join(weak_areas)}
Available study time: {available_hours_per_week} hours per week
Goals: {', '.join(goals)}{deadline_str}

Generate a study plan that:
1. Prioritizes weak areas
2. Distributes time effectively
3. Includes variety (reading, practice, review)
4. Has realistic daily/weekly tasks
5. Includes milestones and checkpoints

Return as JSON with structure:
{{
    "weekly_schedule": {{
        "Monday": [{{"time": "7-8 PM", "activity": "...", "topic": "..."}}],
        ...
    }},
    "priority_topics": [...],
    "milestones": [...],
    "tips": [...]
}}"""

        response = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert study planner creating effective, personalized learning schedules. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    async def recommend_resources(
        self,
        topic: str,
        current_level: str,
        learning_style: str
    ) -> List[Dict]:
        """
        Recommend learning resources for a topic
        
        Args:
            topic: Topic to find resources for
            current_level: Student's current level
            learning_style: Student's learning style
            
        Returns:
            List of recommended resources
        """
        style_preferences = {
            "visual": "videos, infographics, diagrams",
            "auditory": "podcasts, audiobooks, lectures",
            "kinesthetic": "interactive simulations, labs, hands-on projects",
            "reading": "textbooks, articles, written tutorials"
        }
        
        preferred_formats = style_preferences.get(learning_style, "various formats")
        
        prompt = f"""Recommend learning resources for the topic: {topic}

Student level: {current_level}
Preferred formats: {preferred_formats}

Suggest 5-7 high-quality resources including:
- Resource name
- Type (video, article, book, course, etc.)
- Brief description
- Estimated time to complete
- Why it's suitable for this learner

Return as JSON array."""

        response = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert at recommending educational resources. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get('resources', [])
    
    def clear_conversation_history(self, user_id: int):
        """Clear conversation history for a user"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]


# Singleton instance
ai_tutor_service = AITutorService()
