# Backend Setup Guide

## Prerequisites

1. **Python 3.10+**: Download from [python.org](https://www.python.org/downloads/)
2. **pip**: Usually comes with Python
3. **Virtual environment** (recommended)

## Installation Steps

### 1. Create and Activate Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API keys
# Minimum required: OPENAI_API_KEY
```

### 4. Initialize Database

The database will be automatically created when you first run the application.

For production with PostgreSQL:
```bash
# Create database
createdb ai_learning_assistant

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://user:password@localhost:5432/ai_learning_assistant
```

### 5. Run the Application

```bash
python main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Documentation
- Interactive API docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### Main Endpoints
- `/api/v1/transcription/*` - Transcription services
- `/api/v1/notes/*` - Note generation
- `/api/v1/flashcards/*` - Flashcard creation
- `/api/v1/quizzes/*` - Quiz generation and evaluation
- `/api/v1/tutor/*` - AI tutoring

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black app/
```

### Type Checking
```bash
mypy app/
```

## Troubleshooting

### Import Errors
Make sure you're in the virtual environment:
```bash
# Check if venv is activated
which python  # macOS/Linux
where python  # Windows
```

### Database Errors
Delete the database file and restart:
```bash
rm ai_learning_assistant.db
python main.py
```

### API Key Errors
Verify your `.env` file has valid API keys:
```bash
cat .env  # macOS/Linux
type .env  # Windows
```

## Production Deployment

1. **Set DEBUG=False** in `.env`
2. **Use PostgreSQL** instead of SQLite
3. **Set up Redis** for Celery
4. **Use environment variables** for secrets
5. **Run with production server**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

## Environment Variables

Required:
- `OPENAI_API_KEY`: OpenAI API key for AI features

Optional:
- `PINECONE_API_KEY`: For vector database
- `YOUTUBE_API_KEY`: For YouTube metadata
- `DATABASE_URL`: PostgreSQL connection string

See `.env.example` for all available options.
