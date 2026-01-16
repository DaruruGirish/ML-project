"""
Setup script for the backend - installs dependencies and initializes database.
"""
import subprocess
import sys
import os

def install_requirements():
    """Install Python requirements"""
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False

def initialize_database():
    """Initialize database and seed resources"""
    print("\nInitializing database...")
    try:
        from backend import create_app
        from backend.utils.seed_resources import seed_resources
        
        app = create_app()
        with app.app_context():
            seed_resources()
        print("✓ Database initialized and resources seeded")
        return True
    except Exception as e:
        print(f"✗ Failed to initialize database: {e}")
        print("Note: This is okay if database already exists")
        return True  # Not critical

def main():
    """Main setup function"""
    print("=" * 50)
    print("Detect The Stress - Backend Setup")
    print("=" * 50)
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("\n⚠ Warning: .env file not found!")
        print("Please create a .env file with your configuration.")
        print("See backend/README.md for required variables.")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Install requirements
    if not install_requirements():
        print("\n✗ Setup failed at dependency installation")
        return
    
    # Initialize database
    initialize_database()
    
    print("\n" + "=" * 50)
    print("✓ Setup complete!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Make sure your .env file is configured")
    print("2. Run: python app.py")
    print("3. Backend will be available at http://localhost:5000")

if __name__ == '__main__':
    main()
