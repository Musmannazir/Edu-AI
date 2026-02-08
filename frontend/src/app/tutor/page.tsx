'use client'

import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { tutorAPI } from '@/lib/api'
import { Send, Loader2, BookOpen } from 'lucide-react'
import toast from 'react-hot-toast'
import ReactMarkdown from 'react-markdown'

export default function TutorPage() {
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant'; content: string }>>([])
  const [learningStyle, setLearningStyle] = useState('visual')
  const [subject, setSubject] = useState('')

  const askMutation = useMutation({
    mutationFn: (q: string) => tutorAPI.ask(1, q, undefined, learningStyle, subject || undefined),
    onSuccess: (data) => {
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }])
      setQuestion('')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to get response')
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!question.trim()) return

    setMessages(prev => [...prev, { role: 'user', content: question }])
    askMutation.mutate(question)
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-12">
      <div className="container mx-auto px-4 max-w-4xl">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-4 flex items-center gap-3">
            <BookOpen className="w-10 h-10 text-primary-600" />
            AI Tutor
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Ask questions and get personalized explanations tailored to your learning style
          </p>
        </div>

        {/* Settings */}
        <div className="card mb-6">
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">
                Learning Style
              </label>
              <select
                value={learningStyle}
                onChange={(e) => setLearningStyle(e.target.value)}
                className="input-field"
              >
                <option value="visual">Visual</option>
                <option value="auditory">Auditory</option>
                <option value="kinesthetic">Kinesthetic</option>
                <option value="reading">Reading/Writing</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">
                Subject (Optional)
              </label>
              <input
                type="text"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                placeholder="e.g., Mathematics, Physics"
                className="input-field"
              />
            </div>
          </div>
        </div>

        {/* Chat Messages */}
        <div className="card mb-6 h-96 overflow-y-auto">
          {messages.length === 0 ? (
            <div className="text-center text-gray-500 dark:text-gray-400 mt-20">
              <p className="text-lg">Ask your AI tutor anything!</p>
              <p className="text-sm mt-2">Get personalized explanations and support</p>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] p-4 rounded-lg ${
                      message.role === 'user'
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-200 dark:bg-gray-700'
                    }`}
                  >
                    {message.role === 'assistant' ? (
                      <div className="prose dark:prose-invert max-w-none prose-sm">
                        <ReactMarkdown>{message.content}</ReactMarkdown>
                      </div>
                    ) : (
                      <p>{message.content}</p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="card">
          <div className="flex gap-4">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask a question..."
              className="input-field flex-1"
              disabled={askMutation.isPending}
            />
            <button
              type="submit"
              disabled={askMutation.isPending || !question.trim()}
              className="btn-primary flex items-center gap-2"
            >
              {askMutation.isPending ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
