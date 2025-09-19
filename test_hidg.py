#!/usr/bin/env python3
"""Test HIDG logging functionality"""

from hidg import append_hidg_entry, log_pipeline_completion, log_generation_completion
import os
from pathlib import Path

def test_hidg_logging():
    """Test HIDG daily logging"""
    
    # Set environment variables for testing
    os.environ['GIT_BRANCH'] = 'main'
    os.environ['GIT_COMMIT'] = 'abc123def456'
    
    print("Testing HIDG Daily Logging")
    print("-" * 40)
    
    # Test basic logging
    append_hidg_entry('SYSTEM_START', 'API server initialization')
    
    # Test generation logging
    log_generation_completion('Modern office building design', True)
    
    # Test pipeline logging
    log_pipeline_completion('Smart building with IoT', 3, 8.5)
    
    # Test evaluation logging
    from hidg import log_evaluation_completion
    log_evaluation_completion('Residential complex design', 7.8)
    
    # Check log file
    log_path = Path('reports/daily_log.txt')
    if log_path.exists():
        print(f"Log file created: {log_path}")
        print("\nLog Contents:")
        print("-" * 40)
        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
    else:
        print("Log file not found")
    
    print("HIDG logging test completed")

if __name__ == "__main__":
    test_hidg_logging()