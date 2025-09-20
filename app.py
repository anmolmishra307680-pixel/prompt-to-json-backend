"""FastAPI Backend Entry Point for Render Deployment"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from config directory
config_path = Path(__file__).parent / "config" / ".env"
load_dotenv(config_path)

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import the FastAPI app from src
from main_api import app

# Export for uvicorn
__all__ = ["app"]