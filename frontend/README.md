# Frontend Setup Guide

## Prerequisites

1. **Node.js 18+**: Download from [nodejs.org](https://nodejs.org/)
2. **npm** or **yarn**: Comes with Node.js

## Installation Steps

### 1. Install Dependencies

```bash
npm install
# or
yarn install
```

### 2. Configure Environment

```bash
# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local
```

### 3. Run Development Server

```bash
npm run dev
# or
yarn dev
```

The application will be available at http://localhost:3000

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Project Structure

```
frontend/
├── src/
│   ├── app/              # Next.js app directory
│   │   ├── transcribe/   # Transcription page
│   │   ├── tutor/        # AI Tutor page
│   │   ├── layout.tsx    # Root layout
│   │   └── page.tsx      # Home page
│   ├── components/       # Reusable components
│   │   └── Providers.tsx # App providers
│   └── lib/              # Utility functions
│       └── api.ts        # API client
├── public/               # Static files
├── package.json
├── next.config.js        # Next.js configuration
├── tailwind.config.js    # Tailwind CSS config
└── tsconfig.json         # TypeScript config
```

## Pages

### Home (`/`)
- Landing page with feature overview
- Navigation to different tools

### Transcribe (`/transcribe`)
- YouTube video transcription
- Audio/video file upload
- AI-generated notes

### AI Tutor (`/tutor`)
- Interactive chat with AI tutor
- Personalized explanations
- Learning style customization

## API Integration

The frontend communicates with the backend API through the `api.ts` module:

```typescript
import { transcriptionAPI, tutorAPI, quizAPI } from '@/lib/api'

// Example: Transcribe YouTube video
const result = await transcriptionAPI.transcribeYouTube(url, true, 'Math')

// Example: Ask tutor
const response = await tutorAPI.ask(1, question, context, 'visual')
```

## Styling

This project uses:
- **Tailwind CSS** for utility-first styling
- **Custom components** with reusable classes
- **Dark mode** support (system preference)

Utility classes defined in `globals.css`:
- `.btn-primary` - Primary button style
- `.btn-secondary` - Secondary button style
- `.card` - Card container
- `.input-field` - Input field style

## State Management

- **React Query** (`@tanstack/react-query`) for server state
- **Zustand** for client state (if needed)
- **React Context** via Providers

## Building for Production

```bash
# Build the application
npm run build

# Start production server
npm start
```

The build output will be in `.next/` directory.

## Deployment

### Vercel (Recommended)
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

### Other Platforms
1. Build the project: `npm run build`
2. Upload `.next`, `public`, and `package.json`
3. Set environment variables
4. Run `npm start`

## Environment Variables

- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000/api/v1)

## Troubleshooting

### Build Errors
```bash
# Clear cache and reinstall
rm -rf node_modules .next
npm install
npm run build
```

### API Connection Issues
1. Check backend is running on port 8000
2. Verify `NEXT_PUBLIC_API_URL` in `.env.local`
3. Check CORS settings in backend

### TypeScript Errors
```bash
# Check TypeScript
npx tsc --noEmit
```

## Development Tips

1. **Hot Reload**: Changes auto-reload in dev mode
2. **TypeScript**: Use type-safe API calls
3. **Components**: Create reusable components in `src/components/`
4. **API Calls**: Use React Query for caching and loading states
5. **Styling**: Use Tailwind classes for consistent design

## Adding New Pages

1. Create file in `src/app/[page-name]/page.tsx`
2. Add to navigation in `src/app/page.tsx`
3. Create API calls in `src/lib/api.ts` if needed
4. Use React Query for data fetching

Example:
```typescript
// src/app/flashcards/page.tsx
'use client'

import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { flashcardsAPI } from '@/lib/api'

export default function FlashcardsPage() {
  // Your component code
}
```
