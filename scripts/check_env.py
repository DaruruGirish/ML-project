"""
Quick script to check if .env file has Twitter credentials configured.
"""
import os
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has required credentials"""
    env_file = Path('.env')
    
    print("=" * 60)
    print("Checking .env Configuration")
    print("=" * 60)
    print()
    
    # Check if .env exists
    if not env_file.exists():
        print("❌ .env file not found!")
        print("\nCreate it by running:")
        print("  python scripts/create_env_template.py")
        return False
    
    print("✅ .env file exists")
    print()
    
    # Load and check variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = {
        'TWITTER_CLIENT_ID': 'Twitter Client ID',
        'TWITTER_CLIENT_SECRET': 'Twitter Client Secret',
        'TWITTER_REDIRECT_URI': 'Twitter Redirect URI',
    }
    
    optional_vars = {
        'TWITTER_API_BEARER_TOKEN': 'Twitter Bearer Token (optional)',
    }
    
    all_good = True
    
    print("Required Variables:")
    print("-" * 60)
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value and value not in ['', 'PASTE_YOUR_CLIENT_ID_HERE', 'PASTE_YOUR_CLIENT_SECRET_HERE']:
            # Mask sensitive values
            if 'SECRET' in var or 'TOKEN' in var:
                masked = value[:8] + '...' + value[-4:] if len(value) > 12 else '***'
                print(f"✅ {description}: {masked}")
            else:
                print(f"✅ {description}: {value[:30]}..." if len(value) > 30 else f"✅ {description}: {value}")
        else:
            print(f"❌ {description}: NOT SET")
            all_good = False
    
    print()
    print("Optional Variables:")
    print("-" * 60)
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value and value not in ['', 'PASTE_YOUR_BEARER_TOKEN_HERE']:
            masked = value[:8] + '...' + value[-4:] if len(value) > 12 else '***'
            print(f"✅ {description}: {masked}")
        else:
            print(f"⚠️  {description}: NOT SET (optional)")
    
    print()
    print("=" * 60)
    
    if all_good:
        print("✅ All required credentials are configured!")
        print("\nNext steps:")
        print("1. Test with: python scripts/test_twitter_api.py")
        print("2. Start backend: python app.py")
    else:
        print("❌ Missing required credentials")
        print("\nTo get your credentials:")
        print("1. Go to: https://developer.twitter.com/en/portal/dashboard")
        print("2. Click: Apps → Your App → Keys and tokens")
        print("3. Find: OAuth 2.0 Client ID and Client Secret")
        print("4. Copy them to your .env file")
        print("\nSee: HOW_TO_GET_CLIENT_ID.md for detailed instructions")
    
    return all_good

if __name__ == '__main__':
    try:
        check_env_file()
    except ImportError:
        print("❌ python-dotenv not installed")
        print("Install it with: pip install python-dotenv")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
