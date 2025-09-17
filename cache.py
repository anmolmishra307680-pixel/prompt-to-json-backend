# cache.py - Redis caching for expensive operations
import redis
import json
import hashlib
import os
from typing import Optional, Any

class CacheManager:
    def __init__(self):
        self.redis_client = None
        try:
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
            self.redis_client = redis.from_url(redis_url, socket_connect_timeout=2, socket_timeout=2)
            # Test connection
            self.redis_client.ping()
            print("✅ Redis connected successfully")
        except Exception as e:
            print(f"⚠️ Redis not available: {e}")
            print("📝 Using in-memory cache fallback")
            self.redis_client = None
            self._memory_cache = {}
    
    def get_cache_key(self, prompt: str, operation: str = "generate") -> str:
        """Generate cache key from prompt"""
        key_data = f"{operation}:{prompt}"
        return hashlib.sha256(key_data.encode()).hexdigest()[:16]
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached result"""
        if self.redis_client:
            try:
                cached = self.redis_client.get(f"prompt:{key}")
                if cached:
                    return json.loads(cached)
            except Exception:
                pass
        elif hasattr(self, '_memory_cache'):
            return self._memory_cache.get(key)
        return None
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Cache result with TTL (default 1 hour)"""
        if self.redis_client:
            try:
                self.redis_client.setex(
                    f"prompt:{key}", 
                    ttl, 
                    json.dumps(value, default=str)
                )
                return True
            except Exception:
                pass
        elif hasattr(self, '_memory_cache'):
            self._memory_cache[key] = value
            return True
        return False
    
    def cached_generate(self, prompt: str, generator_func):
        """Cache wrapper for generate operations"""
        cache_key = self.get_cache_key(prompt, "generate")
        
        # Try cache first
        cached_result = self.get(cache_key)
        if cached_result:
            return cached_result
        
        # Generate and cache
        result = generator_func(prompt)
        self.set(cache_key, result)
        return result

# Global cache instance
cache = CacheManager()