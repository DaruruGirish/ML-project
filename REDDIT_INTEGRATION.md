# Reddit Integration - Complete Guide

## ✅ What's Been Added

Reddit integration has been fully implemented alongside Twitter! Users can now:

1. **Connect Reddit account** via OAuth
2. **Enter Reddit username manually** for analysis
3. **Analyze Reddit posts and comments** for stress detection
4. **View combined analysis** from both platforms

## 🎯 Features

### Backend

- ✅ Reddit OAuth 2.0 service (`backend/services/reddit_oauth.py`)
- ✅ Reddit API service (`backend/services/reddit_api.py`)
- ✅ Reddit authentication routes (`backend/routes/auth.py`)
- ✅ Updated analysis route to support both platforms
- ✅ Database models updated for Reddit support
- ✅ Configuration for Reddit credentials

### Database Updates

- ✅ User model now supports:
  - `reddit_id` - Reddit user ID
  - `reddit_access_token` - OAuth access token
  - `reddit_refresh_token` - OAuth refresh token
  - `is_reddit_connected` - Connection status
  - `reddit_karma` - User karma score

- ✅ Analysis model now supports:
  - `platform` - 'twitter' or 'reddit'
  - `total_posts_analyzed` - Works for both platforms
  - `posts_with_stress_indicators` - Works for both platforms
  - `content_samples` - Stores Reddit posts or Twitter tweets

## 📋 Setup Instructions

### 1. Get Reddit API Credentials

1. **Go to Reddit Apps**: https://www.reddit.com/prefs/apps
2. **Click "create another app..."** or "create app"
3. **Fill out the form:**
   - **Name**: Detect The Stress
   - **App type**: Select "web app"
   - **Description**: Stress detection and mental health analysis
   - **About URL**: `http://localhost:5173`
   - **Redirect URI**: `http://localhost:5173/auth/reddit/callback`
4. **Click "create app"**
5. **Copy credentials:**
   - **Client ID**: The string under your app name (looks like: `abc123def456...`)
   - **Client Secret**: The "secret" field (click "edit" to reveal)

### 2. Add to .env File

Add these to your `.env` file:

```env
# Reddit OAuth Configuration
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
REDDIT_REDIRECT_URI=http://localhost:5173/auth/reddit/callback
REDDIT_USER_AGENT=DetectTheStress/1.0 by YourUsername

# Reddit Analysis Configuration
MAX_REDDIT_POSTS_TO_ANALYZE=100
MAX_REDDIT_COMMENTS_TO_ANALYZE=50
```

**Important**: 
- Replace `YourUsername` in `REDDIT_USER_AGENT` with your Reddit username
- Reddit requires a User-Agent string that identifies your app

### 3. Update Frontend

The frontend needs to be updated to show Reddit option. See `frontend/` directory for components that need updating.

## 🔌 API Endpoints

### Reddit Authentication

- `GET /api/auth/reddit/authorize` - Get Reddit OAuth URL
- `GET /api/auth/reddit/callback` - OAuth callback handler
- `POST /api/auth/reddit/manual` - Manual Reddit username entry

### Analysis (Updated)

- `POST /api/analysis/analyze` - Now supports `platform` parameter:
  ```json
  {
    "username": "username",
    "platform": "reddit"  // or "twitter"
  }
  ```

## 📊 How It Works

### Reddit OAuth Flow

1. User clicks "Connect Reddit Account"
2. Redirected to Reddit authorization page
3. User logs in and grants permissions
4. Reddit redirects back with authorization code
5. Backend exchanges code for access token
6. User info and tokens saved to database

### Reddit Content Analysis

1. Fetches user's recent posts and comments
2. Analyzes text content for stress indicators
3. Uses same stress analysis algorithm as Twitter
4. Returns stress level, category, and confidence score
5. Stores analysis results in database

## 🎨 Frontend Updates Needed

Update these components to show Reddit option:

1. **AuthenticationSection.tsx**:
   - Add Reddit OAuth card
   - Add Reddit manual entry option
   - Show both Twitter and Reddit options side by side

2. **API Service** (`frontend/src/lib/api.ts`):
   - Add Reddit authentication methods
   - Update analysis to include platform parameter

3. **Dashboard/Results**:
   - Show platform badge (Twitter/Reddit)
   - Display platform-specific content samples

## 🔍 Example Usage

### Analyze Reddit User

```bash
POST /api/analysis/analyze
{
  "username": "spez",
  "platform": "reddit"
}
```

### Connect Reddit Account

```bash
GET /api/auth/reddit/authorize
# Returns auth_url for Reddit OAuth
```

### Manual Reddit Entry

```bash
POST /api/auth/reddit/manual
{
  "username": "spez"
}
```

## 📝 Reddit API Limits

- **Rate Limits**: 60 requests per minute (OAuth)
- **Public API**: No authentication needed for public posts
- **User-Agent Required**: Must identify your app
- **Content Access**: Can read public posts and comments

## 🔒 Security Notes

- Reddit tokens stored in database (encrypt in production)
- User-Agent must identify your app
- OAuth tokens expire (refresh tokens available)
- Users can revoke access in Reddit settings

## 🚀 Next Steps

1. ✅ Backend is complete
2. ⏳ Update frontend to show Reddit option
3. ⏳ Test Reddit OAuth flow
4. ⏳ Test Reddit content analysis
5. ⏳ Add Reddit credentials to `.env`

## 📚 Documentation

- **Reddit API Docs**: https://www.reddit.com/dev/api
- **Reddit OAuth Guide**: https://github.com/reddit-archive/reddit/wiki/OAuth2
- **Reddit Apps**: https://www.reddit.com/prefs/apps

---

**Status**: Backend complete! Frontend updates needed to show Reddit option in UI.
