# AI Learning Assistant

A comprehensive AI-powered learning platform that helps students throughout their entire academic journey with intelligent transcription, note generation, adaptive quizzes, and personalized tutoring.

## 🌟 Features

### Core Capabilities
- **🎥 Smart Transcription**: Automatically transcribe live lectures, uploaded videos, and YouTube content
- **📝 AI-Generated Notes**: Transform transcripts into structured, comprehensive study notes
- **🗂️ Content Organization**: Organize learning materials by subject and topic
- **🎴 Flashcard Generation**: Create flashcards automatically from your content
- **📊 Adaptive Quizzes**: Take personalized quizzes that adapt to your skill level
- **🤖 AI Tutor**: Get instant help from a personalized AI tutor
- **📈 Weak Area Identification**: Identify and focus on topics that need improvement
- **📅 Study Plan Generation**: Receive customized study plans based on your goals
- **🎯 Learning Style Adaptation**: Personalized explanations based on your learning style

## 🏗️ Architecture

### Backend (Python + FastAPI)
- **Framework**: FastAPI for high-performance async APIs
- **Database**: SQLAlchemy with PostgreSQL (production) / SQLite (development)
- **AI/ML**:
  - OpenAI GPT-4 for text generation, summarization, and tutoring
  - Whisper for speech-to-text transcription
  - LangChain for advanced AI workflows
  - Pinecone/ChromaDB for vector storage
- **Task Queue**: Celery + Redis for background processing

### Frontend (Next.js + React)
- **Framework**: Next.js 14 with TypeScript
- **UI**: Tailwind CSS for styling
- **State Management**: Zustand + React Query
- **Components**: Custom React components with Lucide icons

## 📋 Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- PostgreSQL (for production) or SQLite (for development)
- Redis (for task queue)
- OpenAI API key
- Optional: Pinecone API key, YouTube API key

## 🚀 Quick Start

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```env
   OPENAI_API_KEY=your-openai-api-key
   PINECONE_API_KEY=your-pinecone-api-key
   YOUTUBE_API_KEY=your-youtube-api-key
   DATABASE_URL=sqlite:///./ai_learning_assistant.db
   ```

5. **Run the backend**:
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`
   API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment**:
   ```bash
   # Create .env.local file
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local
   ```

4. **Run the development server**:
   ```bash
   npm run dev
   ```
   
   The application will be available at `http://localhost:3000`

## 📖 API Documentation

### Transcription Endpoints

**POST /api/v1/transcription/youtube**
```json
{
  "url": "https://www.youtube.com/watch?v=...",
  "generate_notes": true,
  "subject": "Mathematics"
}
```

**POST /api/v1/transcription/upload**
- Upload audio/video file
- Returns transcript and optionally generated notes

### Notes Endpoints

**POST /api/v1/notes/generate**
```json
{
  "content": "lecture transcript...",
  "subject": "Physics"
}
```

**POST /api/v1/notes/extract-concepts**
- Extract key concepts from content

### Flashcard Endpoints

**POST /api/v1/flashcards/generate**
```json
{
  "content": "study material...",
  "count": 10
}
```

### Quiz Endpoints

**POST /api/v1/quizzes/generate**
```json
{
  "content": "study material...",
  "num_questions": 10,
  "difficulty": "medium",
  "question_types": ["mcq", "true_false"]
}
```

**POST /api/v1/quizzes/evaluate**
- Evaluate quiz attempt and identify weak areas

**POST /api/v1/quizzes/adaptive**
- Generate adaptive quiz based on weak areas

### AI Tutor Endpoints

**POST /api/v1/tutor/ask**
```json
{
  "user_id": 1,
  "question": "How does photosynthesis work?",
  "learning_style": "visual",
  "subject": "Biology"
}
```

**POST /api/v1/tutor/explain**
- Get detailed concept explanation

**POST /api/v1/tutor/study-plan**
- Generate personalized study plan

**POST /api/v1/tutor/recommend-resources**
- Get learning resource recommendations

## 🗂️ Project Structure

```
AILearningAssistant/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   ├── transcription.py
│   │   │       │   ├── notes.py
│   │   │       │   ├── flashcards.py
│   │   │       │   ├── quizzes.py
│   │   │       │   └── tutor.py
│   │   │       └── router.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   └── models.py
│   │   └── services/
│   │       ├── transcription_service.py
│   │       ├── nlp_service.py
│   │       ├── quiz_service.py
│   │       └── ai_tutor_service.py
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── transcribe/
│   │   │   ├── tutor/
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components/
│   │   │   └── Providers.tsx
│   │   └── lib/
│   │       └── api.ts
│   ├── package.json
│   └── next.config.js
└── README.md
```

## 🔧 Configuration

### Environment Variables

**Backend (.env)**:
```env
# Application
APP_NAME=AI Learning Assistant
DEBUG=True
API_HOST=0.0.0.0
API_PORT=8000

# Database
DATABASE_URL=sqlite:///./ai_learning_assistant.db

# OpenAI
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-4-turbo-preview

# Vector Database
PINECONE_API_KEY=your-key-here
PINECONE_ENVIRONMENT=us-west1-gcp

# YouTube
YOUTUBE_API_KEY=your-key-here

# CORS
CORS_ORIGINS=http://localhost:3000
```

**Frontend (.env.local)**:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## 🎓 Usage Examples

### 1. Transcribe a YouTube Lecture

```typescript
import { transcriptionAPI } from '@/lib/api'

const result = await transcriptionAPI.transcribeYouTube(
  'https://www.youtube.com/watch?v=example',
  true,
  'Computer Science'
)

// Result includes: transcript, notes, key_concepts
```

### 2. Generate Flashcards

```typescript
import { flashcardsAPI } from '@/lib/api'

const flashcards = await flashcardsAPI.generate(
  'Your study material here...',
  10
)
```

### 3. Ask AI Tutor

```typescript
import { tutorAPI } from '@/lib/api'

const response = await tutorAPI.ask(
  1,
  'Explain quantum entanglement',
  undefined,
  'visual',
  'Physics'
)
```

### 4. Take Adaptive Quiz

```typescript
import { quizAPI } from '@/lib/api'

const quiz = await quizAPI.generateAdaptive(
  ['calculus', 'derivatives'],
  'intermediate',
  { accuracy: 0.65 }
)
```

## 🧪 Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality

```bash
# Python linting
flake8 app/

# TypeScript linting
npm run lint
```

## 📦 Database Models

- **User**: User accounts and preferences
- **Subject**: Academic subjects
- **Topic**: Topics within subjects
- **Lecture**: Video/audio lectures
- **Note**: Study notes
- **Flashcard**: Review flashcards
- **Quiz**: Quiz templates
- **QuizAttempt**: Quiz results
- **StudySession**: Learning sessions
- **StudyPlan**: Personalized study plans

## 🚀 Deployment

### Backend Deployment

1. Set up PostgreSQL database
2. Configure production environment variables
3. Run database migrations
4. Deploy with gunicorn or uvicorn
5. Set up Redis for Celery tasks

### Frontend Deployment

1. Build the production bundle:
   ```bash
   npm run build
   ```

2. Deploy to Vercel, Netlify, or custom hosting

## 🔐 Security

- API key authentication for backend endpoints
- CORS configuration for frontend-backend communication
- Environment variables for sensitive data
- SQL injection protection via SQLAlchemy ORM

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - feel free to use this project for learning and development.

## 🆘 Support

For issues and questions:
- Check the API documentation at `/docs`
- Review the code examples
- Open an issue on GitHub

## 🎯 Roadmap

- [ ] Real-time collaborative note-taking
- [ ] Mobile app (React Native)
- [ ] Spaced repetition algorithm for flashcards
- [ ] Voice input for AI tutor
- [ ] Integration with Learning Management Systems
- [ ] Offline mode support
- [ ] Multi-language support
- [ ] Advanced analytics dashboard

---

Built with ❤️ using AI to enhance learning
