"""REST API server for production deployment"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
from datetime import datetime
from main_agent import MainAgent
from universal_agent import UniversalAgent
from evaluator_agent import EvaluatorAgent
from universal_evaluator import UniversalEvaluator
from rl_loop import RLLoop
from performance_monitor import monitor
from config import config

app = Flask(__name__)

# Enable CORS if configured
if config.ENABLE_CORS:
    CORS(app)

# Rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[f"{config.RATE_LIMIT} per hour"]
)

# Initialize agents
main_agent = MainAgent()
universal_agent = UniversalAgent()
evaluator_agent = EvaluatorAgent()
universal_evaluator = UniversalEvaluator()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "system_health": monitor.get_system_health()
    })

@app.route('/api/generate', methods=['POST'])
@limiter.limit("10 per minute")
def generate_specification():
    """Generate specification from prompt"""
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({"error": "Prompt is required"}), 400
        
        prompt = data['prompt']
        mode = data.get('mode', 'universal')
        
        # Validate prompt length
        if len(prompt) > config.MAX_PROMPT_LENGTH:
            return jsonify({"error": f"Prompt too long. Max {config.MAX_PROMPT_LENGTH} characters"}), 400
        
        # Start monitoring
        session = monitor.start_monitoring(mode, prompt)
        
        try:
            if mode == 'universal':
                spec = universal_agent.generate_spec(prompt)
                evaluation = universal_evaluator.evaluate_spec(spec, prompt)
                
                result = {
                    "specification": spec.model_dump(),
                    "evaluation": evaluation.model_dump(),
                    "prompt_type": spec.prompt_type,
                    "confidence": spec.metadata.get('confidence', 1.0)
                }
            else:
                spec = main_agent.generate_spec(prompt)
                evaluation = evaluator_agent.evaluate_spec(spec, prompt)
                
                result = {
                    "specification": spec.model_dump(),
                    "evaluation": evaluation.model_dump()
                }
            
            # End monitoring
            monitor.end_monitoring(session, evaluation.score, True)
            
            return jsonify({
                "success": True,
                "data": result,
                "timestamp": datetime.now().isoformat()
            })
        
        except Exception as e:
            monitor.end_monitoring(session, 0, False, str(e))
            return jsonify({"error": f"Generation failed: {str(e)}"}), 500
    
    except Exception as e:
        return jsonify({"error": f"Request processing failed: {str(e)}"}), 500

@app.route('/api/train', methods=['POST'])
@limiter.limit("5 per minute")
def train_rl():
    """Run RL training"""
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({"error": "Prompt is required"}), 400
        
        prompt = data['prompt']
        iterations = min(data.get('iterations', 3), config.MAX_ITERATIONS)
        
        session = monitor.start_monitoring('rl', prompt)
        
        try:
            rl_loop = RLLoop(max_iterations=iterations)
            results = rl_loop.run_training_loop(prompt)
            
            final_score = results['iterations'][-1]['evaluation']['score'] if results['iterations'] else 0
            monitor.end_monitoring(session, final_score, True)
            
            return jsonify({
                "success": True,
                "data": {
                    "iterations": len(results['iterations']),
                    "final_score": final_score,
                    "improvement": final_score - results['iterations'][0]['evaluation']['score'] if len(results['iterations']) > 1 else 0,
                    "learning_insights": results['learning_insights']
                },
                "timestamp": datetime.now().isoformat()
            })
        
        except Exception as e:
            monitor.end_monitoring(session, 0, False, str(e))
            return jsonify({"error": f"Training failed: {str(e)}"}), 500
    
    except Exception as e:
        return jsonify({"error": f"Request processing failed: {str(e)}"}), 500

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get performance analytics"""
    try:
        analytics = monitor.get_analytics()
        return jsonify({
            "success": True,
            "data": analytics,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": f"Analytics failed: {str(e)}"}), 500

@app.route('/api/formats', methods=['GET'])
def get_supported_formats():
    """Get supported formats and capabilities"""
    return jsonify({
        "success": True,
        "data": config.get_supported_formats(),
        "timestamp": datetime.now().isoformat()
    })

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429

@app.errorhandler(404)
def not_found_handler(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error_handler(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    import signal
    import sys
    
    def signal_handler(sig, frame):
        print('\nAPI server stopped by user.')
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    print(f"Starting API server on port {config.WEB_PORT}")
    print(f"Analytics enabled: {config.ENABLE_ANALYTICS}")
    print(f"Rate limit: {config.RATE_LIMIT} requests/hour")
    print(f"Server running at: http://localhost:{config.WEB_PORT}")
    print("Press Ctrl+C to stop")
    
    try:
        app.run(
            host='0.0.0.0',
            port=config.WEB_PORT,
            debug=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print('\nAPI server stopped by user.')
        sys.exit(0)