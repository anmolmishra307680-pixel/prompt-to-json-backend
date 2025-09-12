"""Configuration management for production deployment"""

import os
from pathlib import Path
from typing import Dict, Any

class Config:
    """Production-ready configuration management"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.load_config()
    
    def load_config(self):
        """Load configuration from environment and defaults"""
        self.DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///prompt_to_json.db')
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        self.MAX_PROMPT_LENGTH = int(os.getenv('MAX_PROMPT_LENGTH', '2000'))
        self.MAX_ITERATIONS = int(os.getenv('MAX_RL_ITERATIONS', '10'))
        self.WEB_PORT = int(os.getenv('WEB_PORT', '8501'))
        self.ENABLE_ANALYTICS = os.getenv('ENABLE_ANALYTICS', 'true').lower() == 'true'
        
        # Performance settings
        self.BATCH_SIZE = int(os.getenv('BATCH_SIZE', '32'))
        self.CACHE_SIZE = int(os.getenv('CACHE_SIZE', '1000'))
        self.TIMEOUT_SECONDS = int(os.getenv('TIMEOUT_SECONDS', '30'))
        
        # Security settings
        self.RATE_LIMIT = int(os.getenv('RATE_LIMIT', '100'))
        self.ENABLE_CORS = os.getenv('ENABLE_CORS', 'false').lower() == 'true'
    
    def get_output_dirs(self) -> Dict[str, Path]:
        """Get all output directories"""
        dirs = {
            'logs': self.base_dir / 'logs',
            'specs': self.base_dir / 'spec_outputs',
            'reports': self.base_dir / 'reports',
            'cache': self.base_dir / '.cache',
            'backups': self.base_dir / 'backups'
        }
        
        # Create directories if they don't exist
        for dir_path in dirs.values():
            dir_path.mkdir(exist_ok=True)
        
        return dirs
    
    def get_supported_formats(self) -> Dict[str, Any]:
        """Get supported input/output formats"""
        return {
            'input_formats': ['text', 'json', 'yaml'],
            'output_formats': ['json', 'yaml', 'xml'],
            'prompt_types': ['building', 'software', 'product', 'email', 'task', 'general'],
            'languages': ['en', 'es', 'fr', 'de', 'zh', 'ja']
        }

# Global config instance
config = Config()