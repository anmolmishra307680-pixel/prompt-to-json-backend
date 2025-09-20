#!/usr/bin/env python3
"""Startup script for Render deployment"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from config directory
config_path = Path(__file__).parent / "config" / ".env"
load_dotenv(config_path)

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set environment for proper imports
os.environ['PYTHONPATH'] = str(project_root)

if __name__ == "__main__":
    import uvicorn
    from src.main_api import app
    
    port = int(os.getenv("PORT", 8000))
    
    if os.getenv("PRODUCTION_MODE") == "true":
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            workers=int(os.getenv("MAX_WORKERS", 1)),
            timeout_keep_alive=30
        )
    else:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            reload=False
        )