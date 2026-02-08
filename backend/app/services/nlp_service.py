"""
NLP service for text summarization and processing
"""
from openai import AsyncOpenAI
from typing import List, Optional
import re
from app.core.config import settings


class NLPService:
    """Service for NLP tasks including summarization and content generation"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def generate_notes(self, transcript: str, subject: str = "") -> str:
        """
        Generate structured notes from a transcript
        
        Args:
            transcript: Lecture transcript
            subject: Subject context (optional)
            
        Returns:
            Structured notes in markdown format
        """
        subject_context = f"for a {subject} lecture " if subject else ""
        
        prompt = f"""Generate comprehensive, well-structured notes {subject_context}from the following transcript.
        
Format the notes with:
- Clear headings and subheadings
- Key concepts highlighted
- Important definitions
- Examples and explanations
- Summary points

Transcript:
{transcript}

Generate detailed, organized notes in markdown format:"""

        response = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert note-taking assistant that creates clear, comprehensive, and well-organized study notes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    
    async def summarize_text(self, text: str, max_length: int = 300) -> str:
        """
        Generate a concise summary of text
        
        Args:
            text: Text to summarize
            max_length: Maximum summary length in words
            
        Returns:
            Summary text
        """
        prompt = f"""Summarize the following text in {max_length} words or less. 
Focus on the key points and main ideas.

Text:
{text}

Summary:"""

        response = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert at creating concise, informative summaries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    async def extract_key_concepts(self, text: str) -> List[str]:
        """
        Extract key concepts and topics from text
        
        Args:
            text: Text to analyze
            
        Returns:
            List of key concepts
        """
        prompt = f"""Extract the main concepts, topics, and important terms from the following text.
Return them as a comma-separated list.

Text:
{text}

Key concepts:"""

        response = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert at identifying key concepts and topics in educational content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=300
        )
        
        concepts_text = response.choices[0].message.content
        concepts = [c.strip() for c in concepts_text.split(',')]
        return concepts
    
    async def generate_flashcards(self, content: str, count: int = 10) -> List[dict]:
        """
        Generate flashcards from content
        
        Args:
            content: Content to generate flashcards from
            count: Number of flashcards to generate
            
        Returns:
            List of flashcard dictionaries with question and answer
        """
        prompt = f"""Generate {count} flashcards from the following content.
Each flashcard should have a clear question and a concise answer.
Format as JSON array with 'question' and 'answer' fields.

Content:
{content}

Generate flashcards:"""

        response = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert at creating effective study flashcards. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500,
            response_format={"type": "json_object"}
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        return result.get('flashcards', [])
    
    def chunk_text(self, text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
        """
        Split text into chunks for processing
        
        Args:
            text: Text to chunk
            chunk_size: Size of each chunk
            overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        chunk_size = chunk_size or settings.CHUNK_SIZE
        overlap = overlap or settings.CHUNK_OVERLAP
        
        # Split by sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence.split())
            
            if current_length + sentence_length > chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                # Keep last few sentences for overlap
                overlap_sentences = []
                overlap_length = 0
                for s in reversed(current_chunk):
                    if overlap_length < overlap:
                        overlap_sentences.insert(0, s)
                        overlap_length += len(s.split())
                    else:
                        break
                current_chunk = overlap_sentences
                current_length = overlap_length
            
            current_chunk.append(sentence)
            current_length += sentence_length
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks


# Singleton instance
nlp_service = NLPService()
