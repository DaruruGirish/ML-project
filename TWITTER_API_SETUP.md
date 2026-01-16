# Twitter/X API Setup Guide

Complete guide to get Twitter API credentials for Detect The Stress application.

## Step 1: Create Twitter Developer Account

1. **Go to Twitter Developer Portal:**
   - Visit: https://developer.twitter.com/en/portal/dashboard
   - Sign in with your Twitter/X account

2. **Apply for Developer Access (if needed):**
   - Click "Sign up" or "Apply"
   - Fill out the application form
   - Select "Making a bot" or "Exploring the API" as your use case
   - Wait for approval (usually instant or within a few hours)

## Step 2: Create a Project and App

1. **Create a Project:**
   - Once logged in, click "Create Project"
   - Enter project name: "Detect The Stress"
   - Select use case: "Making a bot" or "Exploring the API"
   - Add a description: "Analyzing Twitter posts for stress detection and mental health awareness"
   - Click "Next"

2. **Create an App:**
   - Enter app name: "Detect The Stress App"
   - Click "Next"
   - Review and create

## Step 3: Configure OAuth 2.0 Settings

1. **Navigate to your App:**
   - Go to the "Keys and tokens" tab
   - Scroll to "OAuth 2.0 Client ID and Client Secret"

2. **Set App Permissions:**
   - Go to "App settings" → "User authentication settings"
   - Click "Set up" or "Edit"
   - Select:
     - **App permissions**: "Read" (to read tweets)
     - **Type of App**: "Web App"
     - **App info**:
       - App name: "Detect The Stress"
       - Website URL: `http://localhost:5173` (or your domain)
       - Callback URI / Redirect URL: `http://localhost:5173/auth/callback`
       - (Important: This must match exactly!)
   - Click "Save"

3. **Get OAuth Credentials:**
   - Go back to "Keys and tokens" tab
   - Under "OAuth 2.0 Client ID and Client Secret":
     - Click "Generate" if not already generated
     - **Copy the Client ID** → This is your `TWITTER_CLIENT_ID`
     - **Copy the Client Secret** → This is your `TWITTER_CLIENT_SECRET`
     - ⚠️ **Important**: Save these immediately! The Client Secret is only shown once.

## Step 4: Get Bearer Token (Optional - for Manual Entry)

The Bearer Token allows you to access public tweets without OAuth. This is useful for the "Manual Username Entry" feature.

1. **Navigate to Keys and Tokens:**
   - In your app dashboard, go to "Keys and tokens" tab

2. **Generate Bearer Token:**
   - Scroll to "Bearer Token"
   - Click "Generate" or "Regenerate"
   - **Copy the Bearer Token** → This is your `TWITTER_API_BEARER_TOKEN`
   - ⚠️ **Important**: Save this immediately! It's only shown once.

## Step 5: Add Credentials to Your .env File

Create or update your `.env` file in the project root:

```env
# Twitter/X OAuth Configuration
TWITTER_CLIENT_ID=your_client_id_here
TWITTER_CLIENT_SECRET=your_client_secret_here
TWITTER_REDIRECT_URI=http://localhost:5173/auth/callback

# Twitter API Bearer Token (Optional - for manual entry)
TWITTER_API_BEARER_TOKEN=your_bearer_token_here
```

**Replace:**
- `your_client_id_here` with your actual Client ID
- `your_client_secret_here` with your actual Client Secret
- `your_bearer_token_here` with your actual Bearer Token (if using manual entry)

## Step 6: Verify Your Setup

### Test OAuth Flow:

1. Start your backend:
   ```bash
   python app.py
   ```

2. Test the authorization endpoint:
   ```bash
   curl http://localhost:5000/api/auth/twitter/authorize
   ```
   
   Should return a JSON with `auth_url` that you can open in a browser.

### Test Bearer Token (if using):

```bash
curl -H "Authorization: Bearer YOUR_BEARER_TOKEN" \
  "https://api.twitter.com/2/tweets/search/recent?query=hello&max_results=10"
```

## Important Notes

### OAuth 2.0 Requirements:

- ✅ **Callback URL must match exactly** - `http://localhost:5173/auth/callback`
- ✅ **App must have "Read" permissions** to access tweets
- ✅ **Type must be "Web App"** for OAuth 2.0
- ✅ **Client ID and Secret are required** for OAuth flow

### Bearer Token:

- ✅ **Bearer Token is optional** - Only needed for manual username entry without OAuth
- ✅ **Bearer Token can access public tweets** without user authentication
- ✅ **Rate limits apply** - Free tier has limited requests per 15 minutes

### Rate Limits:

- **OAuth 2.0**: 300 requests per 15 minutes per user
- **Bearer Token**: Varies by endpoint (check Twitter API docs)
- **Tweet lookup**: 300 requests per 15 minutes

### Production Deployment:

When deploying to production:

1. **Update Callback URL:**
   - Change in Twitter Developer Portal to your production domain
   - Example: `https://yourdomain.com/auth/callback`
   - Update `TWITTER_REDIRECT_URI` in production `.env`

2. **Security:**
   - Never commit `.env` file to git
   - Use environment variables in your hosting platform
   - Rotate credentials if exposed

## Troubleshooting

### "Invalid redirect URI" Error:

- Check that callback URL in Twitter Developer Portal matches exactly
- Check that `TWITTER_REDIRECT_URI` in `.env` matches
- URLs are case-sensitive and must include protocol (http/https)

### "Invalid client credentials" Error:

- Verify Client ID and Secret are correct
- Make sure there are no extra spaces in `.env` file
- Regenerate credentials if needed

### "Forbidden" or "Unauthorized" Errors:

- Check that app has "Read" permissions
- Verify Bearer Token is valid (if using)
- Check rate limits haven't been exceeded

### OAuth Flow Not Working:

- Ensure OAuth 2.0 is enabled in app settings
- Verify app type is set to "Web App"
- Check that all scopes are properly configured

## Quick Reference

### Where to Find Credentials:

1. **Client ID & Secret:**
   - Twitter Developer Portal → Your App → "Keys and tokens" → "OAuth 2.0 Client ID and Client Secret"

2. **Bearer Token:**
   - Twitter Developer Portal → Your App → "Keys and tokens" → "Bearer Token"

3. **App Settings:**
   - Twitter Developer Portal → Your App → "Settings" → "User authentication settings"

### Required Scopes:

- `tweet.read` - Read tweets
- `users.read` - Read user information
- `offline.access` - Refresh token (for OAuth)

## Next Steps

Once you have your credentials:

1. ✅ Add them to `.env` file
2. ✅ Restart your backend server
3. ✅ Test the OAuth flow
4. ✅ Test manual username entry (if using Bearer Token)

## Support

- **Twitter Developer Documentation**: https://developer.twitter.com/en/docs
- **Twitter API Status**: https://api.twitterstat.us/
- **Twitter Developer Forums**: https://twittercommunity.com/c/twitter-api

---

**Security Reminder**: Never share your API credentials publicly. Keep your `.env` file secure and never commit it to version control.
