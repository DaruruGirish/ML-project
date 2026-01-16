# Detect The Stress - Backend API

Complete backend implementation for the Detect The Stress application.

## Features

- 🔐 **Twitter/X OAuth 2.0 Integration** - Secure authentication with PKCE
- 📊 **Stress Analysis Engine** - ML-powered tweet analysis
- 🗄️ **Database Models** - User, Analysis, and Resource management
- 📚 **Resources API** - Mental health content management
- 🔒 **Session Management** - Secure user sessions
- 🌐 **CORS Support** - Frontend integration ready

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```env
# Flask Configuration
FLASK_ENV=development
PORT=5000
SECRET_KEY=your-secret-key-here-change-in-production

# Database Configuration
DATABASE_URL=sqlite:///detect_stress.db

# Twitter/X OAuth Configuration
TWITTER_CLIENT_ID=your_twitter_client_id
TWITTER_CLIENT_SECRET=your_twitter_client_secret
TWITTER_REDIRECT_URI=http://localhost:5173/auth/callback

# Twitter API Configuration (Optional)
TWITTER_API_BEARER_TOKEN=your_bearer_token_here

# CORS Configuration
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Analysis Configuration
MAX_TWEETS_TO_ANALYZE=100
TWEET_LOOKBACK_DAYS=30
```

### 3. Get Twitter API Credentials

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a new app
3. Enable OAuth 2.0
4. Set callback URL: `http://localhost:5173/auth/callback`
5. Copy Client ID and Client Secret to `.env`

### 4. Initialize Database

The database will be created automatically on first run. To seed initial resources:

```python
from backend import create_app
from backend.utils.seed_resources import seed_resources

app = create_app()
with app.app_context():
    seed_resources()
```

Or set `SEED_RESOURCES=true` in `.env` to seed on startup.

### 5. Run the Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication

- `GET /api/auth/twitter/authorize` - Get Twitter OAuth URL
- `GET /api/auth/twitter/callback` - OAuth callback handler
- `POST /api/auth/manual` - Manual username authentication
- `GET /api/auth/status` - Check authentication status
- `POST /api/auth/logout` - Logout user

### Analysis

- `POST /api/analysis/analyze` - Analyze user tweets for stress
- `GET /api/analysis/history` - Get user's analysis history
- `GET /api/analysis/<id>` - Get specific analysis

### Resources

- `GET /api/resources/` - Get all resources (filter by `type` or `category`)
- `GET /api/resources/<id>` - Get specific resource
- `GET /api/resources/types` - Get available resource types
- `GET /api/resources/categories` - Get available categories

## Database Models

### User
- Stores user information and OAuth tokens
- Supports both OAuth and manual entry

### Analysis
- Stores stress analysis results
- Includes detailed metrics and tweet samples

### Resource
- Stores mental health resources (blogs, Wikipedia, games, etc.)
- Supports categorization and tagging

## Architecture

```
backend/
├── __init__.py          # App factory
├── config.py            # Configuration
├── models.py            # Database models
├── routes/              # API routes
│   ├── auth.py         # Authentication endpoints
│   ├── analysis.py     # Analysis endpoints
│   └── resources.py    # Resources endpoints
├── services/            # Business logic
│   ├── twitter_oauth.py    # OAuth service
│   ├── twitter_api.py      # Twitter API service
│   └── stress_analyzer.py  # Stress analysis engine
└── utils/
    └── seed_resources.py   # Database seeding
```

## Security Notes

- **Production**: Encrypt OAuth tokens in database
- **Production**: Use strong SECRET_KEY
- **Production**: Enable HTTPS
- **Production**: Use PostgreSQL instead of SQLite
- **Production**: Implement rate limiting
- **Production**: Add request validation middleware

## Testing

```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test authentication status
curl http://localhost:5000/api/auth/status
```

## Integration with Frontend

The backend is configured to work with the React frontend. Update the frontend API base URL:

```typescript
const API_BASE_URL = 'http://localhost:5000/api';
```
