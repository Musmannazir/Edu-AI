# 🎯 Getting Started - Your First 30 Minutes

A step-by-step guide to get your AI Learning Assistant running and test all major features.

## ⏱️ Timeline

- **0-10 min**: Setup and installation
- **10-15 min**: Test transcription
- **15-20 min**: Test AI tutor
- **20-25 min**: Test quiz generation
- **25-30 min**: Explore and customize

---

## 🔧 Part 1: Setup (10 minutes)

### Prerequisites Check

Open a terminal and verify:

```bash
# Check Python version (need 3.10+)
python --version

# Check Node.js version (need 18+)
node --version

# Check npm
npm --version
```

If anything is missing, install from:
- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/

### Get Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Copy the key (you'll need it in a moment)

### Backend Setup (5 minutes)

```bash
# Navigate to project
cd AILearningAssistant\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies (this will take 3-4 minutes)
pip install -r requirements.txt

# Copy environment file
copy .env.example .env       # Windows
cp .env.example .env         # macOS/Linux
```

**📝 IMPORTANT**: Edit the `.env` file:
- Open `.env` in any text editor
- Find the line: `OPENAI_API_KEY=your-openai-api-key-here`
- Replace `your-openai-api-key-here` with your actual API key
- Save the file

```bash
# Start the backend
python main.py
```

You should see:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ Leave this terminal running!

### Frontend Setup (5 minutes)

Open a **NEW** terminal window:

```bash
# Navigate to frontend
cd AILearningAssistant\frontend

# Install dependencies (this will take 3-4 minutes)
npm install

# Start the development server
npm run dev
```

You should see:
```
- Local:        http://localhost:3000
- Ready in ...ms
```

✅ Leave this terminal running too!

---

## 🧪 Part 2: Test Features (15 minutes)

### Test 1: Video Transcription (5 minutes)

1. **Open browser**: http://localhost:3000

2. **Navigate to Transcribe page**:
   - Click on "Smart Transcription" card
   - Or go directly to http://localhost:3000/transcribe

3. **Try YouTube transcription**:
   ```
   YouTube URL: https://www.youtube.com/watch?v=your-video
   Subject: Mathematics (optional)
   Click "Transcribe"
   ```

4. **What happens**:
   - API fetches video
   - Transcribes audio
   - Generates structured notes
   - Extracts key concepts
   - All in 30-60 seconds!

5. **Expected result**:
   - See the transcript
   - AI-generated notes in markdown
   - Key concepts as tags

### Test 2: AI Tutor (5 minutes)

1. **Navigate to Tutor page**: http://localhost:3000/tutor

2. **Configure settings**:
   - Learning Style: Visual
   - Subject: Physics

3. **Ask questions**:
   ```
   Try these:
   - "Explain Newton's first law of motion"
   - "What is photosynthesis?"
   - "How does a computer store data?"
   ```

4. **Expected result**:
   - Personalized explanation
   - Tailored to your learning style
   - Conversation continues with context

### Test 3: API Documentation (3 minutes)

1. **Open**: http://localhost:8000/docs

2. **Try an endpoint**:
   - Find "POST /api/v1/notes/generate"
   - Click "Try it out"
   - Enter sample content:
     ```json
     {
       "content": "The mitochondria is the powerhouse of the cell",
       "subject": "Biology"
     }
     ```
   - Click "Execute"

3. **Expected result**:
   - AI generates structured notes
   - Returns JSON response

### Test 4: Flashcard Generation (2 minutes)

From API docs (http://localhost:8000/docs):

1. Find "POST /api/v1/flashcards/generate"
2. Try it out with:
   ```json
   {
     "content": "Python is a high-level programming language. It emphasizes code readability and allows programmers to express concepts in fewer lines of code.",
     "count": 5
   }
   ```

3. **Expected result**:
   - 5 flashcards with questions and answers
   - Ready to use for studying

---

## 🎨 Part 3: Customize & Explore (5 minutes)

### Customize AI Responses

**Backend** (`backend/app/services/ai_tutor_service.py`):

Find the system prompt around line 35:
```python
system_prompt = f"""You are a patient, encouraging AI tutor...
```

Modify to change AI personality!

### Add New Features

**Frontend** - Create new page:
```bash
# Create new page directory
mkdir frontend\src\app\flashcards
```

Create `page.tsx`:
```typescript
'use client'

export default function FlashcardsPage() {
  return (
    <div className="min-h-screen p-8">
      <h1 className="text-4xl font-bold">Flashcards</h1>
      {/* Your implementation */}
    </div>
  )
}
```

### Explore Database

The SQLite database is at: `backend/ai_learning_assistant.db`

View with:
- DB Browser for SQLite: https://sqlitebrowser.org/
- Or any SQLite viewer

---

## 🎯 What You've Accomplished

✅ Set up complete full-stack AI application
✅ Integrated OpenAI GPT-4 and Whisper
✅ Built working transcription system
✅ Created AI tutor with conversation
✅ Generated flashcards and notes
✅ Explored API documentation

---

## 🚀 Next Steps

### Learn More
1. **Read** [README.md](README.md) for detailed documentation
2. **Explore** [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for architecture
3. **Review** code in `backend/app/services/` for AI implementation

### Build Features
1. **Quiz page**: Generate and take quizzes
2. **Dashboard**: Track learning progress
3. **Study plans**: Display personalized schedules
4. **Flashcard review**: Spaced repetition system

### Enhance AI
1. Modify prompts in service files
2. Add new AI models (Claude, Gemini, etc.)
3. Implement RAG with vector database
4. Add streaming responses

### Deploy
1. **Backend**: Deploy to Railway, Render, or AWS
2. **Frontend**: Deploy to Vercel or Netlify
3. **Database**: Migrate to PostgreSQL

---

## 💡 Pro Tips

### Development
- Keep both terminals open (backend + frontend)
- Use VS Code with Python and ESLint extensions
- Enable auto-save for faster development
- Check browser console for errors

### Debugging
- Backend errors: Check terminal running `python main.py`
- Frontend errors: Check browser console (F12)
- API testing: Use http://localhost:8000/docs
- Database: Use SQLite browser

### Performance
- Transcription: Longer videos take more time
- AI responses: Can take 5-15 seconds
- First request: May be slower (model loading)

### Cost Management
- OpenAI charges per API call
- Monitor usage: https://platform.openai.com/usage
- Start with smaller content for testing
- Use environment variables for different API keys (dev/prod)

---

## ❓ Troubleshooting

### "Module not found" (Backend)
```bash
# Make sure venv is activated
venv\Scripts\activate

# Reinstall
pip install -r requirements.txt
```

### "Cannot connect to backend" (Frontend)
1. Check backend is running on port 8000
2. Check `.env.local` has correct URL
3. Try restarting both servers

### "OpenAI API error"
1. Verify API key in `.env`
2. Check you have credits: https://platform.openai.com/account/billing
3. Ensure no spaces in API key

### "Port already in use"
```bash
# Backend (port 8000)
# Windows: netstat -ano | findstr :8000
# macOS/Linux: lsof -i :8000

# Frontend (port 3000)
# Use different port: npm run dev -- -p 3001
```

---

## 🎉 Congratulations!

You now have a fully functional AI-powered learning assistant!

**Keep building, keep learning!** 🚀

---

**Need Help?**
- Check main [README.md](README.md)
- Review [QUICKSTART.md](QUICKSTART.md)
- Explore API docs at http://localhost:8000/docs
