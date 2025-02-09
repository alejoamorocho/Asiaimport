from typing import Any, Optional
from django.core.cache import cache
from functools import wraps
import hashlib
import json

class CacheService:
    """Service for handling caching operations."""
    
    def __init__(self, timeout: int = 300):
        self.default_timeout = timeout
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache."""
        return cache.get(key)
    
    def set(self, key: str, value: Any, timeout: Optional[int] = None) -> None:
        """Set a value in cache."""
        cache.set(key, value, timeout or self.default_timeout)
    
    def delete(self, key: str) -> None:
        """Delete a value from cache."""
        cache.delete(key)
    
    def clear_model_cache(self, model_name: str) -> None:
        """Clear all cache entries for a specific model."""
        cache.delete_pattern(f"{model_name}:*")

def cache_response(timeout: int = 300):
    """Decorator for caching view responses."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate a unique cache key based on function arguments
            key_parts = [
                func.__name__,
                str(args),
                str(sorted(kwargs.items()))
            ]
            cache_key = hashlib.md5(json.dumps(key_parts).encode()).hexdigest()
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # If not in cache, execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result
        return wrapper
    return decorator
