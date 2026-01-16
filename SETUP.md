# Complete Setup Guide

Follow these steps to get the Detect The Stress application running.

## Step 1: Backend Setup

### 1.1 Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or use the setup script:

```bash
python setup_backend.py
```

### 1.2 Configure Environment

Create a `.env` file in the project root:

```env
# Flask Configuration
FLASK_ENV=development
PORT=5000
SECRET_KEY=your-secret-key-change-in-production

# Database
DATABASE_URL=sqlite:///detect_stress.db

# Twitter/X OAuth (Required for OAuth flow)
TWITTER_CLIENT_ID=your_client_id_here
TWITTER_CLIENT_SECRET=your_client_secret_here
TWITTER_REDIRECT_URI=http://localhost:5173/auth/callback

# Twitter API (Optional - for manual entry without OAuth)
TWITTER_API_BEARER_TOKEN=your_bearer_token_here

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Analysis Settings
MAX_TWEETS_TO_ANALYZE=100
TWEET_LOOKBACK_DAYS=30
```

### 1.3 Get Twitter API Credentials

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Sign in with your Twitter account
3. Create a new Project and App
4. In the App settings:
   - Enable OAuth 2.0
   - Set Type of App to "Web App"
   - Add callback URL: `http://localhost:5173/auth/callback`
   - Set App permissions to "Read" (for reading tweets)
5. Copy the Client ID and Client Secret to your `.env` file
6. (Optional) Generate a Bearer Token for public API access

### 1.4 Initialize Database

The database will be created automatically on first run. To seed initial resources:

```bash
python -c "from backend import create_app; from backend.utils.seed_resources import seed_resources; app = create_app(); app.app_context().push(); seed_resources()"
```

Or set `SEED_RESOURCES=true` in `.env` to seed on startup.

### 1.5 Run Backend

```bash
python app.py
```

Backend will start at `http://localhost:5000`

## Step 2: Frontend Setup

### 2.1 Navigate to Frontend Directory

```bash
cd frontend
```

### 2.2 Install Dependencies

```bash
npm install
```

### 2.3 Configure Environment (Optional)

Create `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:5000/api
```

### 2.4 Run Frontend

```bash
npm run dev
```

Frontend will start at `http://localhost:5173`

## Step 3: Verify Setup

1. **Backend Health Check:**
   ```bash
   curl http://localhost:5000/api/health
   ```
   Should return: `{"status": "healthy"}`

2. **Frontend:**
   - Open `http://localhost:5173` in your browser
   - You should see the landing page

3. **Test Authentication:**
   - Try the "Manual Username Entry" option first (doesn't require OAuth)
   - Enter a valid Twitter username
   - The analysis should start

## Troubleshooting

### Backend Issues

**ModuleNotFoundError:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`

**Database Errors:**
- Delete `detect_stress.db` and restart the app to recreate it

**Twitter API Errors:**
- Verify your credentials in `.env`
- Check that OAuth callback URL matches exactly
- Ensure your Twitter app has "Read" permissions

### Frontend Issues

**API Connection Errors:**
- Check that backend is running on port 5000
- Verify `VITE_API_BASE_URL` in frontend `.env`
- Check browser console for CORS errors

**Build Errors:**
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again

## Production Deployment

### Backend

1. Use PostgreSQL instead of SQLite
2. Set `FLASK_ENV=production`
3. Use a strong `SECRET_KEY`
4. Enable HTTPS
5. Encrypt OAuth tokens in database
6. Set up proper CORS origins
7. Use environment variables for all secrets

### Frontend

1. Build for production:
   ```bash
   cd frontend
   npm run build
   ```
2. Serve the `dist` folder with a web server (nginx, Apache, etc.)
3. Update API base URL to production backend

## Next Steps

- Train your ML model and update `src/pipeline/predict_pipeline.py`
- Add more resources to the database
- Customize the stress analysis algorithm
- Add rate limiting for production
- Implement caching for better performance

## Support

For detailed documentation:
- Backend: See `backend/README.md`
- Frontend: See `frontend/README.md`
