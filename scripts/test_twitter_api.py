"""
Test script to verify Twitter API credentials are working correctly.
"""
import os
import sys
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

def test_bearer_token():
    """Test Bearer Token authentication"""
    bearer_token = os.getenv('TWITTER_API_BEARER_TOKEN')
    
    if not bearer_token:
        print("❌ TWITTER_API_BEARER_TOKEN not found in .env")
        return False
    
    print("Testing Bearer Token...")
    
    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }
    
    # Test endpoint: Get user by username
    test_username = 'twitter'  # Twitter's official account
    url = f'https://api.twitter.com/2/users/by/username/{test_username}'
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Bearer Token is valid!")
            print(f"   Test user: @{data.get('data', {}).get('username', 'N/A')}")
            return True
        elif response.status_code == 401:
            print("❌ Bearer Token is invalid or expired")
            print(f"   Response: {response.text}")
            return False
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Bearer Token: {str(e)}")
        return False

def test_oauth_credentials():
    """Test OAuth credentials"""
    client_id = os.getenv('TWITTER_CLIENT_ID')
    client_secret = os.getenv('TWITTER_CLIENT_SECRET')
    redirect_uri = os.getenv('TWITTER_REDIRECT_URI')
    
    if not client_id:
        print("❌ TWITTER_CLIENT_ID not found in .env")
        return False
    
    if not client_secret:
        print("❌ TWITTER_CLIENT_SECRET not found in .env")
        return False
    
    if not redirect_uri:
        print("❌ TWITTER_REDIRECT_URI not found in .env")
        return False
    
    print("Testing OAuth Credentials...")
    print(f"   Client ID: {client_id[:10]}... (first 10 chars)")
    print(f"   Redirect URI: {redirect_uri}")
    
    # OAuth credentials can't be directly tested without going through the flow
    # But we can verify they're set
    print("✅ OAuth credentials are configured")
    print("   Note: Full OAuth flow requires user interaction")
    return True

def test_backend_integration():
    """Test if backend can be reached"""
    print("\nTesting Backend Integration...")
    
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
            return True
        else:
            print(f"⚠️  Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running")
        print("   Start it with: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error connecting to backend: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Twitter API Credentials Test")
    print("=" * 60)
    print()
    
    results = []
    
    # Test OAuth credentials
    results.append(("OAuth Credentials", test_oauth_credentials()))
    print()
    
    # Test Bearer Token (optional)
    bearer_token = os.getenv('TWITTER_API_BEARER_TOKEN')
    if bearer_token:
        results.append(("Bearer Token", test_bearer_token()))
    else:
        print("⚠️  Bearer Token not configured (optional for manual entry)")
    print()
    
    # Test backend
    results.append(("Backend Integration", test_backend_integration()))
    print()
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result for _, result in results)
    
    print()
    if all_passed:
        print("✅ All tests passed! Your Twitter API setup is correct.")
    else:
        print("❌ Some tests failed. Please check your configuration.")
        print("\nNext steps:")
        print("1. Verify your .env file has all required credentials")
        print("2. Check TWITTER_API_SETUP.md for setup instructions")
        print("3. Ensure backend is running: python app.py")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
