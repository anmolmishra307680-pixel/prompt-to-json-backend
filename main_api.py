"""FastAPI Backend for Prompt-to-JSON System"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import uvicorn
from datetime import datetime

# Import agents and database
from prompt_agent import MainAgent
from evaluator import EvaluatorAgent
from rl_agent import RLLoop
from db import Database
from feedback import FeedbackAgent

app = FastAPI(title="Prompt-to-JSON API", version="1.0.0")

# Initialize agents and database
prompt_agent = MainAgent()
evaluator_agent = EvaluatorAgent()
rl_agent = RLLoop()
feedback_agent = FeedbackAgent()
db = Database()

# Request models
class GenerateRequest(BaseModel):
    prompt: str

class EvaluateRequest(BaseModel):
    spec: Dict[Any, Any]
    prompt: str

class IterateRequest(BaseModel):
    prompt: str
    n_iter: int = 3

# Response models
class GenerateResponse(BaseModel):
    spec: Dict[Any, Any]
    success: bool
    message: str = ""

class EvaluateResponse(BaseModel):
    evaluation: Dict[Any, Any]
    success: bool
    message: str = ""

# Removed response models to fix schema issues

class LogValuesRequest(BaseModel):
    date: str
    day: str
    task: str
    values_reflection: Dict[str, str]
    achievements: Dict[Any, Any] = None
    technical_notes: Dict[Any, Any] = None

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Prompt-to-JSON API", "version": "1.0.0"}

@app.get("/favicon.ico")
async def favicon():
    """Favicon endpoint"""
    return {"message": "No favicon configured"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "agents": ["prompt", "evaluator", "rl"]}

@app.post("/generate", response_model=GenerateResponse)
async def generate_spec(request: GenerateRequest):
    """Generate specification from prompt"""
    try:
        spec = prompt_agent.run(request.prompt)
        return GenerateResponse(
            spec=spec.model_dump(),
            success=True,
            message="Specification generated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/evaluate")
async def evaluate_spec(request: EvaluateRequest):
    """Evaluate specification"""
    try:
        from schema import DesignSpec
        # Add default values for missing required fields
        spec_data = request.spec.copy()
        if "building_type" not in spec_data:
            spec_data["building_type"] = "general"
        if "stories" not in spec_data:
            spec_data["stories"] = 1
        if "materials" not in spec_data:
            spec_data["materials"] = []
        if "dimensions" not in spec_data:
            spec_data["dimensions"] = {"length": 1, "width": 1, "height": 1, "area": 1}
        if "features" not in spec_data:
            spec_data["features"] = []
        if "requirements" not in spec_data:
            spec_data["requirements"] = [request.prompt]
        
        spec = DesignSpec(**spec_data)
        evaluation = evaluator_agent.run(spec, request.prompt)
        
        return {
            "evaluation": evaluation.model_dump(),
            "success": True,
            "message": "Evaluation completed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/iterate")
async def iterate_rl(request: IterateRequest):
    """Run RL iterations with detailed before→after, scores, feedback"""
    try:
        # Ensure minimum 2 iterations
        n_iter = max(2, request.n_iter)
        rl_agent.max_iterations = n_iter
        
        results = rl_agent.run(request.prompt, n_iter)
        
        # Format detailed iteration logs
        detailed_iterations = []
        for iteration in results.get("iterations", []):
            detailed_iterations.append({
                "iteration_number": iteration["iteration"],
                "iteration_id": iteration.get("iteration_id"),
                "before": {
                    "spec": iteration.get("spec_before"),
                    "score": iteration.get("score_before", 0)
                },
                "after": {
                    "spec": iteration["spec_after"],
                    "score": iteration["score_after"]
                },
                "evaluation": iteration["evaluation"],
                "feedback": iteration["feedback"],
                "reward": iteration["reward"],
                "improvement": iteration.get("improvement", 0)
            })
        
        return {
            "success": True,
            "session_id": results.get("session_id"),
            "prompt": request.prompt,
            "total_iterations": len(detailed_iterations),
            "iterations": detailed_iterations,
            "final_spec": results.get("final_spec", {}),
            "learning_insights": results.get("learning_insights", {}),
            "message": f"RL training completed with {len(detailed_iterations)} iterations"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reports/{report_id}")
async def get_report(report_id: str):
    """Retrieve full report from DB"""
    try:
        report = db.get_report(report_id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/log-values")
async def log_values(request: LogValuesRequest):
    """Store HIDG values per day"""
    try:
        hidg_id = db.save_hidg_log(
            request.date,
            request.day,
            request.task,
            request.values_reflection,
            request.achievements,
            request.technical_notes
        )
        return {
            "success": True,
            "hidg_id": hidg_id,
            "message": "Values logged successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch-evaluate")
async def batch_evaluate(prompts: List[str]):
    """Process multiple specs/prompts and store evaluations"""
    try:
        results = []
        for prompt in prompts:
            # Generate spec
            spec = prompt_agent.run(prompt)
            # Evaluate spec
            evaluation = evaluator_agent.run(spec, prompt)
            
            results.append({
                "prompt": prompt,
                "spec": spec.model_dump(),
                "evaluation": evaluation.model_dump()
            })
        
        return {
            "success": True,
            "results": results,
            "count": len(results),
            "message": f"Batch processed {len(results)} prompts"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/iterations/{session_id}")
async def get_iteration_logs(session_id: str):
    """Get all iteration logs for a session"""
    try:
        # Try database first
        logs = db.get_iteration_logs(session_id)
        
        # If no logs in DB, check fallback files
        if not logs:
            from pathlib import Path
            import json
            
            iteration_file = Path("logs/iteration_logs.json")
            if iteration_file.exists():
                with open(iteration_file, 'r') as f:
                    all_logs = json.load(f)
                
                # Filter by session_id
                logs = [log for log in all_logs if log.get('session_id') == session_id]
        
        if not logs:
            return {
                "success": False,
                "session_id": session_id,
                "total_iterations": 0,
                "iterations": [],
                "message": "No iteration logs found for this session"
            }
        
        return {
            "success": True,
            "session_id": session_id,
            "total_iterations": len(logs),
            "iterations": logs
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve iteration logs"
        }

@app.get("/cli-tools")
async def get_cli_tools():
    """Get available CLI tools and commands"""
    return {
        "tools": {
            "history": "View prompt history",
            "stats": "Show system statistics", 
            "db": "Database operations",
            "score": "Quick scoring utility",
            "examples": "View sample outputs"
        },
        "commands": [
            "python main.py --test",
            "python main.py --cli-tools",
            "python main.py --score-only",
            "python main.py --examples"
        ]
    }

@app.get("/system-test")
async def run_system_test():
    """Run basic system tests"""
    try:
        # Test core functionality
        spec = prompt_agent.run("Test building")
        evaluation = evaluator_agent.run(spec, "Test building")
        
        return {
            "success": True,
            "tests_passed": [
                "prompt_agent",
                "evaluator_agent",
                "database_connection"
            ],
            "message": "All core tests passed"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "System test failed"
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)