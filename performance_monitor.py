"""Performance monitoring and analytics"""

import time
import psutil
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

@dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""
    timestamp: str
    mode: str
    prompt_length: int
    execution_time: float
    memory_usage: float
    cpu_usage: float
    score: float
    success: bool
    error_type: str = None

class PerformanceMonitor:
    """Real-time performance monitoring and analytics"""
    
    def __init__(self):
        self.metrics_file = Path("logs/performance_metrics.json")
        self.metrics_file.parent.mkdir(exist_ok=True)
        self.current_session = []
    
    def start_monitoring(self, mode: str, prompt: str) -> Dict[str, Any]:
        """Start monitoring a session"""
        try:
            return {
                'start_time': time.time(),
                'start_memory': psutil.virtual_memory().percent,
                'start_cpu': psutil.cpu_percent(),
                'mode': mode,
                'prompt_length': len(prompt)
            }
        except Exception as e:
            # Fallback monitoring data
            return {
                'start_time': time.time(),
                'start_memory': 0,
                'start_cpu': 0,
                'mode': mode,
                'prompt_length': len(prompt),
                'monitoring_error': str(e)
            }
    
    def end_monitoring(self, session_data: Dict[str, Any], score: float = 0, 
                      success: bool = True, error_type: str = None) -> PerformanceMetrics:
        """End monitoring and record metrics"""
        end_time = time.time()
        end_memory = psutil.virtual_memory().percent
        end_cpu = psutil.cpu_percent()
        
        metrics = PerformanceMetrics(
            timestamp=datetime.now().isoformat(),
            mode=session_data['mode'],
            prompt_length=session_data['prompt_length'],
            execution_time=end_time - session_data['start_time'],
            memory_usage=end_memory - session_data['start_memory'],
            cpu_usage=end_cpu - session_data['start_cpu'],
            score=score,
            success=success,
            error_type=error_type
        )
        
        self.current_session.append(metrics)
        self.save_metrics(metrics)
        return metrics
    
    def save_metrics(self, metrics: PerformanceMetrics):
        """Save metrics to file"""
        try:
            existing_metrics = []
            if self.metrics_file.exists():
                with open(self.metrics_file, 'r') as f:
                    existing_metrics = json.load(f)
            
            existing_metrics.append(asdict(metrics))
            
            with open(self.metrics_file, 'w') as f:
                json.dump(existing_metrics, f, indent=2, default=str)
        except Exception as e:
            print(f"Warning: Failed to save performance metrics: {e}")
    
    def get_analytics(self) -> Dict[str, Any]:
        """Generate performance analytics"""
        try:
            if not self.metrics_file.exists():
                return {"message": "No performance data available"}
            
            with open(self.metrics_file, 'r') as f:
                all_metrics = json.load(f)
            
            if not all_metrics:
                return {"message": "No performance data available"}
            
            # Calculate analytics
            total_runs = len(all_metrics)
            successful_runs = sum(1 for m in all_metrics if m['success'])
            avg_execution_time = sum(m['execution_time'] for m in all_metrics) / total_runs
            avg_score = sum(m['score'] for m in all_metrics) / total_runs
            
            mode_stats = {}
            for metrics in all_metrics:
                mode = metrics['mode']
                if mode not in mode_stats:
                    mode_stats[mode] = {'count': 0, 'avg_time': 0, 'avg_score': 0}
                mode_stats[mode]['count'] += 1
                mode_stats[mode]['avg_time'] += metrics['execution_time']
                mode_stats[mode]['avg_score'] += metrics['score']
            
            # Calculate averages
            for mode in mode_stats:
                count = mode_stats[mode]['count']
                mode_stats[mode]['avg_time'] /= count
                mode_stats[mode]['avg_score'] /= count
            
            return {
                "total_runs": total_runs,
                "success_rate": (successful_runs / total_runs) * 100,
                "avg_execution_time": round(avg_execution_time, 3),
                "avg_score": round(avg_score, 2),
                "mode_statistics": mode_stats,
                "last_updated": datetime.now().isoformat()
            }
        
        except Exception as e:
            return {"error": f"Failed to generate analytics: {e}"}
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get current system health metrics"""
        try:
            return {
                "cpu_usage": psutil.cpu_percent(interval=0.1),
                "memory_usage": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('C:\\' if os.name == 'nt' else '/').percent,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "cpu_usage": 0,
                "memory_usage": 0,
                "disk_usage": 0,
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }

# Global monitor instance
monitor = PerformanceMonitor()