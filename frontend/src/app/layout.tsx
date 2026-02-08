import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Providers from '@/components/Providers'
import Link from 'next/link'
import { Brain, Home, FileText, MessageSquare, BookOpen } from 'lucide-react'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'AI Learning Assistant',
  description: 'Your intelligent companion for effective learning',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>
          {/* Navigation Bar */}
          <nav className="sticky top-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg border-b border-gray-200 dark:border-gray-800 shadow-sm">
            <div className="container mx-auto px-4">
              <div className="flex items-center justify-between h-16">
                {/* Logo */}
                <Link href="/" className="flex items-center gap-2 group">
                  <div className="p-2 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg shadow-md group-hover:scale-110 transition-transform">
                    <Brain className="w-6 h-6 text-white" />
                  </div>
                  <span className="font-bold text-lg bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                    AI Learning
                  </span>
                </Link>

                {/* Navigation Links */}
                <div className="hidden md:flex items-center gap-1">
                  <Link 
                    href="/" 
                    className="flex items-center gap-2 px-4 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors text-gray-700 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400"
                  >
                    <Home className="w-4 h-4" />
                    Home
                  </Link>
                  <Link 
                    href="/transcribe" 
                    className="flex items-center gap-2 px-4 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors text-gray-700 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400"
                  >
                    <FileText className="w-4 h-4" />
                    Transcribe
                  </Link>
                  <Link 
                    href="/notes" 
                    className="flex items-center gap-2 px-4 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors text-gray-700 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400"
                  >
                    <BookOpen className="w-4 h-4" />
                    Notes
                  </Link>
                  <Link 
                    href="/tutor" 
                    className="flex items-center gap-2 px-4 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors text-gray-700 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400"
                  >
                    <MessageSquare className="w-4 h-4" />
                    AI Tutor
                  </Link>
                </div>

                {/* CTA Button */}
                <div className="hidden md:block">
                  <Link 
                    href="/transcribe" 
                    className="btn-gradient px-6 py-2 text-sm"
                  >
                    Get Started
                  </Link>
                </div>
              </div>
            </div>
          </nav>

          {children}
        </Providers>
      </body>
    </html>
  )
}
