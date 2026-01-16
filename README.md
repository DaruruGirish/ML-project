# Detect The Stress - Complete Application

A modern, calming web application that analyzes Twitter/X posts to detect stress levels in users, helping them understand their digital wellbeing.

## 🎯 Features

- **Multi-Platform Integration**: Twitter/X and Reddit OAuth 2.0 authentication
- **Manual Entry**: Analyze any public Twitter/X or Reddit username
- **Stress Analysis**: ML-powered analysis of posts and comments to detect stress patterns
- **Privacy-Focused**: User control over data access
- **Resources Hub**: Curated mental health resources (blogs, Wikipedia articles with direct links, games)
- **Modern UI**: Built with React, TypeScript, Tailwind CSS, and shadcn/ui
- **Complete Backend**: Flask API with database, OAuth services, and analysis engine

## 📁 Project Structure

```
.
├── frontend/              # React + TypeScript frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── lib/          # Utilities and API service
│   │   └── App.tsx       # Main app component
│   └── package.json
│
├── backend/              # Flask backend
│   ├── routes/           # API endpoints
│   ├── services/         # Business logic
│   ├── models.py         # Database models
│   └── config.py         # Configuration
│
├── src/                  # ML pipeline
│   ├── pipeline/         # Prediction pipeline
│   └── components/       # Data processing
│
└── app.py                # Main Flask application
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- Twitter Developer Account (for OAuth)

### Backend Setup

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Create `.env` file:**
```env
FLASK_ENV=development
PORT=5000
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///detect_stress.db
TWITTER_CLIENT_ID=your_client_id
TWITTER_CLIENT_SECRET=your_client_secret
TWITTER_REDIRECT_URI=http://localhost:5173/auth/callback
TWITTER_API_BEARER_TOKEN=your_bearer_token (optional)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

3. **Get API credentials (optional - can add later):**
   - **Twitter**: See `TWITTER_API_SETUP.md` for detailed instructions
   - **Reddit**: See `REDDIT_INTEGRATION.md` for detailed instructions
   - You can run the app without credentials (some features will be limited)

4. **Run the backend:**
```bash
python app.py
```

Backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Create `.env` file (optional):**
```env
VITE_API_BASE_URL=http://localhost:5000/api
```

4. **Run the frontend:**
```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

## 📚 API Documentation

### Authentication

- `GET /api/auth/twitter/authorize` - Get Twitter OAuth URL
- `GET /api/auth/twitter/callback` - OAuth callback
- `POST /api/auth/manual` - Manual username authentication
- `GET /api/auth/status` - Check auth status
- `POST /api/auth/logout` - Logout

### Analysis

- `POST /api/analysis/analyze` - Analyze user tweets
- `GET /api/analysis/history` - Get analysis history
- `GET /api/analysis/<id>` - Get specific analysis

### Resources

- `GET /api/resources/` - Get resources (filter by type/category)
- `GET /api/resources/<id>` - Get specific resource
- `GET /api/resources/types` - Get resource types
- `GET /api/resources/categories` - Get categories

## 🗄️ Database

The application uses SQLite by default (can be changed to PostgreSQL in production).

**Models:**
- `User` - User accounts and OAuth tokens
- `Analysis` - Stress analysis results
- `Resource` - Mental health resources

**Initialize database:**
```python
from backend import create_app
from backend.utils.seed_resources import seed_resources

app = create_app()
with app.app_context():
    seed_resources()  # Seed initial resources
```

## 🔒 Security Notes

**For Production:**
- Use strong `SECRET_KEY`
- Encrypt OAuth tokens in database
- Enable HTTPS
- Use PostgreSQL instead of SQLite
- Implement rate limiting
- Add request validation

## 🧪 Testing

```bash
# Test backend health
curl http://localhost:5000/api/health

# Test frontend
cd frontend
npm run build
npm run preview
```

## 📝 Environment Variables

See `.env.example` for all available configuration options.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is part of the Detect The Stress application.

## 🆘 Support

For issues and questions, please check the documentation in:
- `backend/README.md` - Backend documentation
- `frontend/README.md` - Frontend documentation

## 🎨 Design

The application features:
- Calming color scheme (soft blues and greens)
- Modern card-based layout
- Smooth animations and transitions
- Responsive design (mobile and desktop)
- Accessible components

---

**Note**: This tool provides insights based on language patterns and is not a substitute for professional mental health advice.
