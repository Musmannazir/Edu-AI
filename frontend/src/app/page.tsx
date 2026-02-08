import Link from 'next/link'
import { BookOpen, Brain, FileText, MessageSquare, Target, Sparkles, Zap, Award } from 'lucide-react'

export default function Home() {
  const features = [
    {
      icon: <FileText className="w-8 h-8" />,
      title: 'Smart Transcription',
      description: 'Automatically transcribe lectures and videos with AI-powered accuracy',
      href: '/transcribe',
      gradient: 'from-blue-500 to-cyan-500',
      badge: 'FREE'
    },
    {
      icon: <BookOpen className="w-8 h-8" />,
      title: 'AI-Generated Notes',
      description: 'Get structured, comprehensive notes from your lectures',
      href: '/notes',
      gradient: 'from-purple-500 to-pink-500'
    },
    {
      icon: <Brain className="w-8 h-8" />,
      title: 'Adaptive Quizzes',
      description: 'Practice with personalized quizzes that adapt to your level',
      href: '/quizzes',
      gradient: 'from-orange-500 to-red-500'
    },
    {
      icon: <MessageSquare className="w-8 h-8" />,
      title: 'AI Tutor',
      description: 'Get instant help from your personal AI tutor',
      href: '/tutor',
      gradient: 'from-green-500 to-emerald-500'
    },
    {
      icon: <Target className="w-8 h-8" />,
      title: 'Study Plans',
      description: 'Receive personalized study plans based on your goals',
      href: '/study-plan',
      gradient: 'from-indigo-500 to-purple-500'
    },
  ]

  return (
    <main className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 md:py-32">
        <div className="absolute inset-0 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 opacity-10"></div>
        <div className="container mx-auto px-4 text-center relative z-10">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-full text-sm font-medium mb-6 shadow-lg animate-fade-in">
            <Sparkles className="w-4 h-4" />
            Powered by Advanced AI
          </div>
          <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent animate-slide-up">
            AI Learning Assistant
          </h1>
          <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto text-gray-700 dark:text-gray-300 animate-fade-in">
            Transform your learning experience with AI-powered transcription, 
            intelligent note-taking, and personalized tutoring
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center animate-slide-up">
            <Link 
              href="/transcribe" 
              className="btn-gradient inline-flex items-center gap-2 text-lg px-8 py-4 group"
            >
              <Zap className="w-5 h-5 group-hover:rotate-12 transition-transform" />
              Get Started Free
            </Link>
            <Link 
              href="/tutor" 
              className="inline-flex items-center gap-2 px-8 py-4 bg-white dark:bg-gray-800 text-gray-800 dark:text-white rounded-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-300 border-2 border-gray-200 dark:border-gray-700"
            >
              <MessageSquare className="w-5 h-5" />
              Try AI Tutor
            </Link>
          </div>
          <div className="mt-12 flex justify-center gap-8 text-center">
            <div className="animate-fade-in">
              <div className="text-3xl font-bold text-indigo-600 dark:text-indigo-400">100%</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Free for YouTube</div>
            </div>
            <div className="animate-fade-in" style={{animationDelay: '100ms'}}>
              <div className="text-3xl font-bold text-purple-600 dark:text-purple-400">AI</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Powered</div>
            </div>
            <div className="animate-fade-in" style={{animationDelay: '200ms'}}>
              <div className="text-3xl font-bold text-pink-600 dark:text-pink-400">24/7</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Available</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
              Everything You Need to Excel
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Comprehensive AI-powered tools designed to accelerate your learning
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Link 
                key={index} 
                href={feature.href}
                className="group relative card-premium hover:scale-105 transition-all duration-300 cursor-pointer border-2 border-transparent hover:border-indigo-200 dark:hover:border-indigo-700 animate-slide-up"
                style={{animationDelay: `${index * 100}ms`}}
              >
                {feature.badge && (
                  <div className="absolute -top-3 -right-3">
                    <span className="inline-flex items-center px-3 py-1 bg-green-500 text-white text-xs font-bold rounded-full shadow-lg">
                      {feature.badge}
                    </span>
                  </div>
                )}
                <div className={`inline-flex p-4 rounded-xl bg-gradient-to-br ${feature.gradient} text-white mb-4 shadow-lg group-hover:scale-110 transition-transform`}>
                  {feature.icon}
                </div>
                <h3 className="text-2xl font-bold mb-3 text-gray-800 dark:text-white">
                  {feature.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {feature.description}
                </p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl md:text-5xl font-bold text-center mb-16 bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
            How It Works
          </h2>
          
          <div className="max-w-4xl mx-auto space-y-8">
            {[
              { step: 1, title: 'Upload or Record', description: 'Upload lecture videos, recordings, or use YouTube links', icon: <FileText className="w-6 h-6" /> },
              { step: 2, title: 'AI Processing', description: 'Our AI transcribes, analyzes, and generates structured notes', icon: <Brain className="w-6 h-6" /> },
              { step: 3, title: 'Study & Practice', description: 'Review notes, practice with flashcards, and take adaptive quizzes', icon: <BookOpen className="w-6 h-6" /> },
              { step: 4, title: 'Get Personalized Help', description: 'Ask your AI tutor questions and receive tailored study plans', icon: <MessageSquare className="w-6 h-6" /> },
            ].map((item, index) => (
              <div key={item.step} className="flex items-start gap-6 p-6 bg-white dark:bg-gray-800 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 animate-slide-up border border-gray-200 dark:border-gray-700" style={{animationDelay: `${index * 100}ms`}}>
                <div className="flex-shrink-0 w-14 h-14 bg-gradient-to-br from-indigo-500 to-purple-600 text-white rounded-xl flex items-center justify-center font-bold text-xl shadow-lg">
                  {item.step}
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-bold mb-2 text-gray-800 dark:text-white">{item.title}</h3>
                  <p className="text-gray-600 dark:text-gray-400">{item.description}</p>
                </div>
                <div className="text-indigo-600 dark:text-indigo-400">
                  {item.icon}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center card-premium bg-gradient-to-r from-indigo-600 to-purple-600 text-white border-0">
            <Award className="w-16 h-16 mx-auto mb-6" />
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Ready to Transform Your Learning?
            </h2>
            <p className="text-xl mb-8 opacity-90">
              Join thousands of students already using AI to accelerate their studies
            </p>
            <Link 
              href="/transcribe" 
              className="inline-flex items-center gap-2 px-8 py-4 bg-white text-indigo-600 rounded-lg font-bold text-lg shadow-xl hover:shadow-2xl hover:scale-105 transition-all duration-300"
            >
              <Sparkles className="w-5 h-5" />
              Start Learning Now - It&apos;s Free!
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 border-t border-gray-800">
        <div className="container mx-auto px-4 text-center">
          <div className="mb-4">
            <h3 className="text-2xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
              AI Learning Assistant
            </h3>
          </div>
          <p className="text-gray-400">&copy; 2026 AI Learning Assistant. Built with AI to enhance learning.</p>
        </div>
      </footer>
    </main>
  )
}
