"""
Helper script to create a .env file template with placeholders.
"""
import os

def create_env_template():
    """Create .env file template if it doesn't exist"""
    env_file = '.env'
    
    if os.path.exists(env_file):
        response = input(f"{env_file} already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled. Existing .env file preserved.")
            return
    
    template = """# Flask Configuration
FLASK_ENV=development
PORT=5000
SECRET_KEY=your-secret-key-here-change-in-production

# Database Configuration
DATABASE_URL=sqlite:///detect_stress.db

# Twitter/X OAuth Configuration
# Get these from: https://developer.twitter.com/en/portal/dashboard
# Go to: Your App → Keys and tokens → OAuth 2.0 Client ID and Client Secret
TWITTER_CLIENT_ID=PASTE_YOUR_CLIENT_ID_HERE
TWITTER_CLIENT_SECRET=PASTE_YOUR_CLIENT_SECRET_HERE
TWITTER_REDIRECT_URI=http://localhost:5173/auth/callback

# Twitter API Bearer Token (Optional - for manual entry without OAuth)
# Get from: Your App → Keys and tokens → Bearer Token
TWITTER_API_BEARER_TOKEN=PASTE_YOUR_BEARER_TOKEN_HERE

# CORS Configuration
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Analysis Configuration
MAX_TWEETS_TO_ANALYZE=100
TWEET_LOOKBACK_DAYS=30

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# Logging
LOG_LEVEL=INFO

# Optional: Seed resources on startup
SEED_RESOURCES=false
"""
    
    with open(env_file, 'w') as f:
        f.write(template)
    
    print(f"✅ Created {env_file} file")
    print("\nNext steps:")
    print("1. Open .env file")
    print("2. Replace PASTE_YOUR_CLIENT_ID_HERE with your actual Client ID")
    print("3. Replace PASTE_YOUR_CLIENT_SECRET_HERE with your actual Client Secret")
    print("4. Replace PASTE_YOUR_BEARER_TOKEN_HERE with your actual Bearer Token (optional)")
    print("5. Save the file")
    print("\nGet your credentials from:")
    print("https://developer.twitter.com/en/portal/dashboard")
    print("→ Your App → Keys and tokens")

if __name__ == '__main__':
    create_env_template()
