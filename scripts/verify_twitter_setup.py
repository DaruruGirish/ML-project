"""
Script to help verify Twitter OAuth setup and provide guidance.
"""
import os
import sys
from pathlib import Path

def check_env_file():
    """Check if .env file exists and what's configured"""
    env_file = Path('.env')
    
    print("=" * 60)
    print("Twitter OAuth Setup Checker")
    print("=" * 60)
    print()
    
    if not env_file.exists():
        print("❌ .env file not found")
        print("\nCreate it with:")
        print("  python scripts/create_env_template.py")
        return False
    
    print("✅ .env file exists")
    
    # Try to load it
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("⚠️  python-dotenv not installed")
        print("Install with: pip install python-dotenv")
        return False
    
    # Check credentials
    client_id = os.getenv('TWITTER_CLIENT_ID', '')
    client_secret = os.getenv('TWITTER_CLIENT_SECRET', '')
    redirect_uri = os.getenv('TWITTER_REDIRECT_URI', '')
    
    print("\nCurrent Configuration:")
    print("-" * 60)
    
    if client_id and client_id not in ['', 'PASTE_YOUR_CLIENT_ID_HERE']:
        print(f"✅ TWITTER_CLIENT_ID: {client_id[:20]}...")
    else:
        print("❌ TWITTER_CLIENT_ID: NOT SET")
    
    if client_secret and client_secret not in ['', 'PASTE_YOUR_CLIENT_SECRET_HERE']:
        print(f"✅ TWITTER_CLIENT_SECRET: {client_secret[:20]}...")
    else:
        print("❌ TWITTER_CLIENT_SECRET: NOT SET")
    
    if redirect_uri:
        print(f"✅ TWITTER_REDIRECT_URI: {redirect_uri}")
    else:
        print("❌ TWITTER_REDIRECT_URI: NOT SET")
    
    print()
    print("=" * 60)
    
    if not client_id or not client_secret:
        print("\n⚠️  OAuth credentials not configured yet")
        print("\nTo get your credentials:")
        print("1. Go to: https://developer.twitter.com/en/portal/dashboard")
        print("2. Click: Apps → Your App")
        print("3. Click: 'Set up' in 'User authentication settings'")
        print("4. Fill the form:")
        print("   - Type: Web App, Automated App or Bot")
        print("   - Permissions: Read")
        print("   - Callback: http://localhost:5173/auth/callback")
        print("   - Website: http://localhost:5173")
        print("5. Click Save")
        print("6. Go to: Keys and tokens tab")
        print("7. Find: OAuth 2.0 Client ID and Client Secret")
        print("8. Copy to .env file")
        print("\nIf settings won't save, see: SAVE_SETTINGS_FIX.md")
        return False
    
    print("✅ All credentials are configured!")
    print("\nNext steps:")
    print("1. Test with: python scripts/test_twitter_api.py")
    print("2. Start backend: python app.py")
    return True

if __name__ == '__main__':
    try:
        success = check_env_file()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)
