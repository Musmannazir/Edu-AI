# 🚀 Quick Start Guide

Get your AI Learning Assistant up and running in minutes!

## 📋 Prerequisites Checklist

- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- [ ] Git installed (optional)

## ⚡ Fast Setup (5 Minutes)

### Step 1: Backend Setup

Open a terminal and run:

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate
# OR (macOS/Linux)
source venv/bin/activate

# Install dependencies (this may take 2-3 minutes)
pip install -r requirements.txt

# Create environment file
copy .env.example .env    # Windows
# OR
cp .env.example .env      # macOS/Linux
```

**Important**: Edit the `.env` file and add your OpenAI API key:
```env
OPENAI_API_KEY=your-actual-api-key-here
```

Start the backend:
```bash
python main.py
```

✅ **Backend running at http://localhost:8000**

### Step 2: Frontend Setup

Open a NEW terminal window and run:

```bash
# Navigate to frontend
cd frontend

# Install dependencies (this may take 2-3 minutes)
npm install

# Create environment file
echo NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1 > .env.local

# Start the frontend
npm run dev
```

✅ **Frontend running at http://localhost:3000**

## 🎉 You're Ready!

Open your browser and visit:
- **Application**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs

## 🧪 Quick Test

### Test 1: Transcribe a YouTube Video

1. Go to http://localhost:3000/transcribe
2. Enter a YouTube URL (e.g., a lecture or educational video)
3. Optionally add a subject (e.g., "Mathematics")
4. Click "Transcribe"
5. Wait for the AI to generate transcript and notes!

### Test 2: Ask the AI Tutor

1. Go to http://localhost:3000/tutor
2. Select your learning style
3. Ask a question (e.g., "Explain photosynthesis")
4. Get a personalized response!

## 🔧 Common Issues

### Backend won't start?
- Check if Python virtual environment is activated
- Verify OpenAI API key in `.env` file
- Make sure port 8000 is not in use

### Frontend won't start?
- Run `npm install` again
- Check if backend is running
- Make sure port 3000 is not in use

### "Connection refused" error?
- Ensure backend is running on port 8000
- Check `.env.local` has correct API URL

## 📚 What's Next?

1. **Explore Features**: Try transcription, notes, quizzes, and tutoring
2. **Read Documentation**: Check [README.md](README.md) for detailed info
3. **Customize**: Modify AI prompts in backend services
4. **Add Features**: Build on top of the existing structure

## 💡 Tips

- Keep both terminal windows open (backend and frontend)
- API documentation at http://localhost:8000/docs is interactive
- Check browser console for frontend errors
- Check terminal for backend errors

## 🆘 Need Help?

- Review the main [README.md](README.md)
- Check [backend/README.md](backend/README.md) for backend details
- Check [frontend/README.md](frontend/README.md) for frontend details
- API docs at http://localhost:8000/docs

---

**Happy Learning! 🎓**
