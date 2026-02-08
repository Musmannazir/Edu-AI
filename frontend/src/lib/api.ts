import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Transcription API
export const transcriptionAPI = {
  transcribeYouTube: async (url: string, generateNotes: boolean = true, subject?: string) => {
    const response = await api.post('/transcription/youtube', {
      url,
      generate_notes: generateNotes,
      subject,
    })
    return response.data
  },

  transcribeUpload: async (file: File, generateNotes: boolean = true, subject?: string) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('generate_notes', String(generateNotes))
    if (subject) formData.append('subject', subject)

    const response = await api.post('/transcription/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  summarize: async (transcript: string, maxLength: number = 300) => {
    const response = await api.post('/transcription/summarize', null, {
      params: { transcript, max_length: maxLength },
    })
    return response.data
  },
}

// Notes API
export const notesAPI = {
  generateNotes: async (content: string, subject?: string) => {
    const response = await api.post('/notes/generate', { content, subject })
    return response.data
  },

  extractConcepts: async (content: string) => {
    const response = await api.post('/notes/extract-concepts', null, {
      params: { content },
    })
    return response.data
  },
}

// Flashcards API
export const flashcardsAPI = {
  generate: async (content: string, count: number = 10) => {
    const response = await api.post('/flashcards/generate', { content, count })
    return response.data
  },
}

// Quiz API
export const quizAPI = {
  generate: async (
    content: string,
    numQuestions: number = 10,
    difficulty: string = 'medium',
    questionTypes?: string[]
  ) => {
    const response = await api.post('/quizzes/generate', {
      content,
      num_questions: numQuestions,
      difficulty,
      question_types: questionTypes,
    })
    return response.data
  },

  evaluate: async (questions: any[], userAnswers: string[]) => {
    const response = await api.post('/quizzes/evaluate', {
      questions,
      user_answers: userAnswers,
    })
    return response.data
  },

  generateAdaptive: async (
    weakTopics: string[],
    userLevel: string,
    previousPerformance?: any
  ) => {
    const response = await api.post('/quizzes/adaptive', {
      weak_topics: weakTopics,
      user_level: userLevel,
      previous_performance: previousPerformance,
    })
    return response.data
  },

  explainQuestion: async (
    question: string,
    correctAnswer: string,
    userAnswer: string,
    learningStyle: string = 'visual'
  ) => {
    const response = await api.post('/quizzes/explain', null, {
      params: { question, correct_answer: correctAnswer, user_answer: userAnswer, learning_style: learningStyle },
    })
    return response.data
  },
}

// Tutor API
export const tutorAPI = {
  ask: async (
    userId: number,
    question: string,
    context?: string,
    learningStyle: string = 'visual',
    subject?: string
  ) => {
    const response = await api.post('/tutor/ask', {
      user_id: userId,
      question,
      context,
      learning_style: learningStyle,
      subject,
    })
    return response.data
  },

  explainConcept: async (
    concept: string,
    depthLevel: string = 'intermediate',
    learningStyle: string = 'visual',
    includeExamples: boolean = true
  ) => {
    const response = await api.post('/tutor/explain', {
      concept,
      depth_level: depthLevel,
      learning_style: learningStyle,
      include_examples: includeExamples,
    })
    return response.data
  },

  generateStudyPlan: async (
    weakAreas: string[],
    availableHoursPerWeek: number,
    goals: string[],
    deadline?: string
  ) => {
    const response = await api.post('/tutor/study-plan', {
      weak_areas: weakAreas,
      available_hours_per_week: availableHoursPerWeek,
      goals,
      deadline,
    })
    return response.data
  },

  recommendResources: async (
    topic: string,
    currentLevel: string,
    learningStyle: string = 'visual'
  ) => {
    const response = await api.post('/tutor/recommend-resources', {
      topic,
      current_level: currentLevel,
      learning_style: learningStyle,
    })
    return response.data
  },

  clearHistory: async (userId: number) => {
    const response = await api.post(`/tutor/clear-history/${userId}`)
    return response.data
  },
}
