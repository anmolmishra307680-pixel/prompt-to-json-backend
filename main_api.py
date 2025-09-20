"""FastAPI Backend for Prompt-to-JSON System - Render Deployment Entry Point"""

import sys
from pathlib import Path

# Add src directory to Python path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import the actual app from src
from main_api import app

# Export app for uvicorn
__all__ = ["app"]