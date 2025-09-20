"""FastAPI Backend - Render Deployment Entry Point"""

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

# Set PYTHONPATH environment variable
os.environ['PYTHONPATH'] = str(src_path) + ':' + os.environ.get('PYTHONPATH', '')

# Import the actual FastAPI app
try:
    # Change to src directory for imports
    os.chdir(src_path)
    sys.path.insert(0, str(src_path))
    
    # Import all required modules with proper path context
    from fastapi import FastAPI, HTTPException, Request, Depends, Response
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.security import APIKeyHeader, HTTPBearer
    from pydantic import BaseModel
    from typing import Dict, Any, List, Optional
    import uvicorn
    from datetime import datetime, timezone
    import secrets
    import logging
    import time
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    
    # Import agents and database with error handling
    try:
        from prompt_agent import MainAgent
        from evaluator import EvaluatorAgent
        from rl_agent import RLLoop
        from db.database import Database
        from feedback import FeedbackAgent
        from cache import cache
        from auth import create_access_token, get_current_user
        import error_handlers
        from universal_schema import UniversalDesignSpec
        
        # Initialize agents
        prompt_agent = MainAgent()
        evaluator_agent = EvaluatorAgent()
        rl_agent = RLLoop()
        feedback_agent = FeedbackAgent()
        db = Database()
        
        print("[OK] All agents initialized successfully")
    except Exception as e:
        print(f"[WARN] Agent initialization warning: {e}")
        # Create fallback objects
        class FallbackAgent:
            def run(self, *args, **kwargs):
                return {"error": "Agent not available"}
        
        prompt_agent = FallbackAgent()
        evaluator_agent = FallbackAgent()
        rl_agent = FallbackAgent()
        feedback_agent = FallbackAgent()
        
        class FallbackDB:
            def get_session(self): 
                raise RuntimeError("Database unavailable")
            def save_spec(self, *args): return "fallback_id"
            def save_eval(self, *args): return "fallback_id"
            def get_report(self, *args): return None
            def get_iteration_logs(self, *args): return []
            def save_hidg_log(self, *args): return "fallback_id"
        
        db = FallbackDB()
    
    # Create FastAPI app
    API_VERSION = "2.1.1"
    API_KEY = os.getenv("API_KEY", "bhiv-secret-key-2024")
    
    api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
    bearer_scheme = HTTPBearer(auto_error=False)
    
    def verify_api_key(api_key: str = Depends(api_key_header)):
        """Verify API key from X-API-Key header"""
        if not api_key:
            raise HTTPException(
                status_code=401, 
                detail="Invalid or missing API key. Include X-API-Key header."
            )
        
        if not secrets.compare_digest(api_key, API_KEY):
            raise HTTPException(
                status_code=401, 
                detail="Invalid or missing API key. Include X-API-Key header."
            )
        return api_key
    
    app = FastAPI(
        title="Prompt-to-JSON API", 
        version=API_VERSION,
        description="Production-Ready AI Backend with Multi-Agent Coordination"
    )
    
    # Rate limiter
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    
    # CORS middleware
    FRONTEND_URL = os.getenv("FRONTEND_URL", "*")
    allowed_origins = [FRONTEND_URL] if FRONTEND_URL != "*" else ["*"]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    
    # Request models
    class GenerateRequest(BaseModel):
        prompt: str
    
    class TokenRequest(BaseModel):
        username: str
        password: str
    
    # Basic endpoints
    @app.get("/health")
    @limiter.limit("20/minute")
    async def health_check(request: Request):
        """Public health check endpoint for monitoring"""
        return {
            "status": "healthy",
            "version": API_VERSION,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    @app.post("/token")
    @limiter.limit("10/minute")
    def token_create(request: Request, payload: TokenRequest, api_key: str = Depends(verify_api_key)):
        """Create JWT token for authentication (requires API key)"""
        username = payload.username
        password = payload.password
        
        demo_username = os.getenv("DEMO_USERNAME", "admin")
        demo_password = os.getenv("DEMO_PASSWORD", "bhiv2024")
        
        if username == demo_username and password == demo_password:
            token = create_access_token({"sub": username})
            return {"access_token": token, "token_type": "bearer"}
        
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    @app.get("/")
    @limiter.limit("20/minute")
    async def root(request: Request, api_key: str = Depends(verify_api_key), user=Depends(get_current_user)):
        """Root endpoint"""
        return {
            "message": "Prompt-to-JSON API", 
            "version": API_VERSION,
            "status": "Production Ready"
        }
    
    @app.post("/generate")
    @limiter.limit("20/minute")
    async def generate_spec(request: Request, generate_request: GenerateRequest, api_key: str = Depends(verify_api_key), user=Depends(get_current_user)):
        """Generate specification from prompt"""
        try:
            spec = prompt_agent.run(generate_request.prompt)
            return {
                "spec": spec.model_dump() if hasattr(spec, 'model_dump') else spec,
                "success": True,
                "message": "Specification generated successfully"
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    print("[OK] FastAPI app created successfully")
    
except Exception as e:
    print(f"[ERROR] Failed to create app: {e}")
    # Create minimal fallback app
    from fastapi import FastAPI
    app = FastAPI(title="Prompt-to-JSON API - Fallback")
    
    @app.get("/health")
    def health():
        return {"status": "fallback_mode", "error": str(e)}

# Change back to original directory
os.chdir(Path(__file__).parent)

# Export app
__all__ = ["app"]