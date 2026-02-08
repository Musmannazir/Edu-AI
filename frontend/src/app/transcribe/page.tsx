'use client'

import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { transcriptionAPI } from '@/lib/api'
import toast from 'react-hot-toast'
import ReactMarkdown from 'react-markdown'
import { Youtube, Upload, Loader2, Sparkles, FileText, Copy, Check } from 'lucide-react'

export default function TranscribePage() {
  const [youtubeUrl, setYoutubeUrl] = useState('')
  const [subject, setSubject] = useState('')
  const [result, setResult] = useState<any>(null)
  const [copied, setCopied] = useState(false)

  const youtubeMutation = useMutation({
    mutationFn: (url: string) => transcriptionAPI.transcribeYouTube(url, false, subject),
    onSuccess: (data) => {
      setResult(data)
      toast.success('Transcription completed!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Transcription failed')
    },
  })

  const uploadMutation = useMutation({
    mutationFn: (file: File) => transcriptionAPI.transcribeUpload(file, false, subject),
    onSuccess: (data) => {
      setResult(data)
      toast.success('Transcription completed!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Transcription failed')
    },
  })

  const handleYoutubeSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!youtubeUrl) {
      toast.error('Please enter a YouTube URL')
      return
    }
    youtubeMutation.mutate(youtubeUrl)
  }

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      uploadMutation.mutate(file)
    }
  }

  const isLoading = youtubeMutation.isPending || uploadMutation.isPending

  const copyToClipboard = () => {
    if (result?.transcript) {
      navigator.clipboard.writeText(result.transcript)
      setCopied(true)
      toast.success('Copied to clipboard!')
      setTimeout(() => setCopied(false), 2000)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-12">
      <div className="container mx-auto px-4 max-w-7xl">
        {/* Hero Section */}
        <div className="text-center mb-12 animate-fade-in">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-full text-sm font-medium mb-4 shadow-lg">
            <Sparkles className="w-4 h-4" />
            Free YouTube Transcription
          </div>
          <h1 className="text-5xl md:text-6xl font-bold mb-4 bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
            Transcribe Lectures & Videos
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Transform your videos into searchable text instantly. 100% free for YouTube videos with captions.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-12">
          {/* YouTube Transcription */}
          <div className="group hover:scale-[1.02] transition-all duration-300 animate-slide-up">
            <div className="relative card-premium border-2 border-transparent hover:border-indigo-200 dark:hover:border-indigo-700">
              <div className="absolute -top-2 -right-2">
                <span className="inline-flex items-center px-3 py-1 bg-green-500 text-white text-xs font-bold rounded-full shadow-lg">
                  FREE
                </span>
              </div>
              <div className="flex items-center gap-3 mb-6">
                <div className="p-3 bg-gradient-to-br from-red-500 to-red-600 rounded-xl shadow-lg">
                  <Youtube className="w-6 h-6 text-white" />
                </div>
                <h2 className="text-2xl font-bold text-gray-800 dark:text-white">YouTube Video</h2>
              </div>
            
            <form onSubmit={handleYoutubeSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">
                  YouTube URL
                </label>
                <input
                  type="url"
                  value={youtubeUrl}
                  onChange={(e) => setYoutubeUrl(e.target.value)}
                  placeholder="https://www.youtube.com/watch?v=..."
                  className="input-field"
                  disabled={isLoading}
                />
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
                  disabled={isLoading}
                />
              </div>
              
              <button
                type="submit"
                disabled={isLoading}
                className="btn-gradient w-full flex items-center justify-center gap-2 group"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5 group-hover:rotate-12 transition-transform" />
                    Transcribe
                  </>
                )}
              </button>
            </form>
            </div>
          </div>

          {/* File Upload */}
          <div className="group hover:scale-[1.02] transition-all duration-300 animate-slide-up" style={{animationDelay: '100ms'}}>
            <div className="relative card-premium border-2 border-transparent hover:border-purple-200 dark:hover:border-purple-700">
              <div className="absolute -top-2 -right-2">
                <span className="inline-flex items-center px-3 py-1 bg-yellow-500 text-white text-xs font-bold rounded-full shadow-lg">
                  PREMIUM
                </span>
              </div>
              <div className="flex items-center gap-3 mb-6">
                <div className="p-3 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-xl shadow-lg">
                  <Upload className="w-6 h-6 text-white" />
                </div>
                <h2 className="text-2xl font-bold text-gray-800 dark:text-white">Upload Audio/Video</h2>
              </div>
            
            <div className="space-y-4">
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
                  disabled={isLoading}
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">
                  Choose File
                </label>
                <input
                  type="file"
                  accept="audio/*,video/*"
                  onChange={handleFileUpload}
                  disabled={isLoading}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none"
                />
              </div>
              
              <p className="text-sm text-gray-500 dark:text-gray-400 flex items-center gap-2">
                <FileText className="w-4 h-4" />
                Supported formats: MP3, MP4, WAV, M4A, WebM
              </p>
              <div className="mt-4 p-3 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
                <p className="text-sm text-yellow-800 dark:text-yellow-200">
                  ⚠️ Requires OpenAI API key for audio file transcription
                </p>
              </div>
            </div>
            </div>
          </div>
        </div>

        {/* Results */}
        {result && (
          <div className="space-y-6 animate-fade-in">
            {result.title && (
              <div className="card-premium bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-indigo-900/20 dark:to-purple-900/20 border-l-4 border-indigo-500">
                <div className="flex items-center gap-3 mb-2">
                  <FileText className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                  <h3 className="text-xl font-bold text-gray-800 dark:text-white">Video Title</h3>
                </div>
                <p className="text-lg text-gray-700 dark:text-gray-300 font-medium">{result.title}</p>
              </div>
            )}

            {result.notes && (
              <div className="card">
                <h3 className="text-xl font-semibold mb-4">AI-Generated Notes</h3>
                <div className="prose dark:prose-invert max-w-none">
                  <ReactMarkdown>{result.notes}</ReactMarkdown>
                </div>
              </div>
            )}

            {result.key_concepts && result.key_concepts.length > 0 && (
              <div className="card">
                <h3 className="text-xl font-semibold mb-4">Key Concepts</h3>
                <div className="flex flex-wrap gap-2">
                  {result.key_concepts.map((concept: string, index: number) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-primary-100 text-primary-800 rounded-full text-sm"
                    >
                      {concept}
                    </span>
                  ))}
                </div>
              </div>
            )}

            <div className="card-premium">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-gradient-to-br from-green-500 to-emerald-600 rounded-lg">
                    <FileText className="w-5 h-5 text-white" />
                  </div>
                  <h3 className="text-2xl font-bold text-gray-800 dark:text-white">Full Transcript</h3>
                </div>
                <button
                  onClick={copyToClipboard}
                  className="flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 rounded-lg transition-colors"
                >
                  {copied ? (
                    <>
                      <Check className="w-4 h-4 text-green-600" />
                      <span className="text-sm font-medium text-green-600">Copied!</span>
                    </>
                  ) : (
                    <>
                      <Copy className="w-4 h-4" />
                      <span className="text-sm font-medium">Copy</span>
                    </>
                  )}
                </button>
              </div>
              <div className="max-h-96 overflow-y-auto bg-gray-50 dark:bg-gray-900/50 rounded-lg p-6 border border-gray-200 dark:border-gray-700 custom-scrollbar">
                <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap leading-relaxed">
                  {result.transcript}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
