# Detect The Stress - Frontend

A modern, calming web application that analyzes Twitter/X posts to detect stress levels in users.

## Features

- 🎨 **Modern UI**: Built with React, TypeScript, and Tailwind CSS
- 🧩 **Component Library**: Uses shadcn/ui for consistent, accessible components
- 📱 **Responsive Design**: Works seamlessly on mobile and desktop
- 🔒 **Privacy-Focused**: User control over data access
- ⚡ **Real-Time Analysis**: Instant insights from Twitter activity
- 🎯 **Form Validation**: Comprehensive username validation
- ✨ **Smooth Animations**: Polished transitions and loading states

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **shadcn/ui** for UI components
- **Lucide React** for icons

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser and navigate to `http://localhost:5173`

### Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/          # shadcn/ui components
│   │   ├── Header.tsx
│   │   ├── Hero.tsx
│   │   ├── AuthenticationSection.tsx
│   │   ├── FeaturesSection.tsx
│   │   └── Footer.tsx
│   ├── lib/
│   │   └── utils.ts     # Utility functions
│   ├── App.tsx          # Main app component
│   ├── main.tsx         # Entry point
│   └── style.css        # Global styles with Tailwind
├── public/              # Static assets
├── index.html
├── tailwind.config.js
├── postcss.config.js
└── package.json
```

## Features Overview

### Authentication Options

1. **Twitter/X OAuth**: Connect your account securely (mock implementation)
2. **Manual Username Entry**: Enter any Twitter/X username for analysis

### Form Validation

- Username length validation (1-15 characters)
- Character validation (alphanumeric and underscore only)
- Real-time error feedback

### UI Components

- Modern card-based layout
- Smooth animations and transitions
- Loading states with spinners
- Success/error message displays
- Responsive design for all screen sizes

## Color Scheme

The application uses a calming color palette:
- **Primary**: Soft blue (#3B82F6)
- **Secondary**: Soft green (#10B981)
- **Accent**: Light pastel tones
- **Background**: Clean whites with subtle gradients

## Future Enhancements

- Backend API integration
- Real Twitter/X OAuth implementation
- Stress pattern visualization charts
- Historical data tracking
- Export functionality

## License

This project is part of the Detect The Stress application.
