"""
Main application entry point for Detect The Stress backend.
"""
from backend import create_app
from backend.utils.seed_resources import seed_resources
import os

# Create the Flask app
app = create_app()

# Seed resources on first run (optional - can be run manually)
if os.getenv('SEED_RESOURCES', 'false').lower() == 'true':
    with app.app_context():
        try:
            seed_resources()
        except Exception as e:
            print(f"Note: Could not seed resources: {e}")

if __name__ == '__main__':
    # Run the application
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    app.run(debug=debug, host='0.0.0.0', port=port)
