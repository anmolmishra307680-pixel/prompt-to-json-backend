import json
from datetime import datetime
from pathlib import Path

class DailyLogger:
    def __init__(self, log_path: str = "reports/daily_log.txt"):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(exist_ok=True)
    
    def log_daily_reflection(self, honesty: str, discipline: str, gratitude: str):
        """Log daily values reflection"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        reflection = f"""
=== Daily Reflection - {timestamp} ===
Honesty: {honesty}
Discipline: {discipline}  
Gratitude: {gratitude}
{'='*50}

"""
        
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(reflection)
    
    def log_system_status(self, total_prompts: int, avg_score: float, issues_resolved: int):
        """Log system performance status"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        status = f"""
=== System Status - {timestamp} ===
Total Prompts Processed: {total_prompts}
Average Score: {avg_score:.2f}
Issues Resolved: {issues_resolved}
System Health: {'Good' if avg_score > 85 else 'Needs Attention'}
{'='*50}

"""
        
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(status)