"""FastAPI Backend Entry Point for Render Deployment"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from config directory
config_path = Path(__file__).parent / "config" / ".env"
load_dotenv(config_path)

# Set PYTHONPATH to include src directory
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))
os.environ['PYTHONPATH'] = str(src_path) + ':' + os.environ.get('PYTHONPATH', '')

try:
    # Import the FastAPI app from src
    from main_api import app
except ImportError as e:
    print(f"Import error: {e}")
    # Create a minimal fallback app
    from fastapi import FastAPI
    app = FastAPI(title="Prompt-to-JSON API - Fallback")
    
    @app.get("/health")
    def health():
        return {"status": "fallback_mode", "error": str(e)}

# Export for uvicorn
__all__ = ["app"]