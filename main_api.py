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

class IterateResponse(BaseModel):
    iterations: List[Dict[Any, Any]]
    final_spec: Dict[Any, Any]
    success: bool
    message: str = ""

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

@app.post("/evaluate", response_model=EvaluateResponse)
async def evaluate_spec(request: EvaluateRequest):
    """Evaluate specification"""
    try:
        from schema import DesignSpec
        spec = DesignSpec(**request.spec)
        evaluation = evaluator_agent.run(spec, request.prompt)
        return EvaluateResponse(
            evaluation=evaluation.model_dump(),
            success=True,
            message="Evaluation completed successfully"
        )
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
        logs = db.get_iteration_logs(session_id)
        if not logs:
            raise HTTPException(status_code=404, detail="Session not found")
        return {
            "success": True,
            "session_id": session_id,
            "total_iterations": len(logs),
            "iterations": logs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)