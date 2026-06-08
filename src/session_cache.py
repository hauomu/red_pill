#!/usr/bin/env python3
"""
Session Cache Module

In-memory session-scoped caching for pipeline optimization.
Cache is created only after validation succeeds.
Cache failures do not affect pipeline execution.
"""

import pandas as pd
from typing import Optional, Dict, Any
from datetime import datetime
import hashlib


class SessionCache:
    """In-memory session-scoped cache for dataframes and datasets"""
    
    def __init__(self, max_size_mb: int = 500):
        """Initialize session cache
        
        Args:
            max_size_mb: Maximum cache size in MB (for future quota tracking)
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._max_size_mb = max_size_mb
        self._created_at = datetime.now()
        self._hit_count = 0
        self._miss_count = 0
        self._enabled = True
    
    def put(self, key: str, value: pd.DataFrame, source: str = "") -> None:
        """Store item in cache
        
        Args:
            key: Cache key
            value: DataFrame to cache
            source: Description of data source
            
        Raises:
            TypeError: If value is not DataFrame
        """
        if not isinstance(value, pd.DataFrame):
            raise TypeError(f"Can only cache DataFrames, got {type(value).__name__}")
        
        if not self._enabled:
            return
        
        try:
            self._cache[key] = {
                'data': value.copy(),
                'source': source,
                'cached_at': datetime.now().isoformat(),
                'shape': value.shape,
                'dtypes': value.dtypes.to_dict(),
            }
        except Exception as e:
            # Cache failures don't affect pipeline
            print(f"⚠️  Cache put failed for key '{key}': {e}")
    
    def get(self, key: str) -> Optional[pd.DataFrame]:
        """Retrieve item from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached DataFrame or None if not cached
        """
        if not self._enabled:
            return None
        
        if key not in self._cache:
            self._miss_count += 1
            return None
        
        try:
            self._hit_count += 1
            # Return copy to prevent accidental mutations of cached data
            return self._cache[key]['data'].copy()
        except Exception as e:
            # Cache failures don't affect pipeline
            print(f"⚠️  Cache get failed for key '{key}': {e}")
            return None
    
    def exists(self, key: str) -> bool:
        """Check if key is cached
        
        Args:
            key: Cache key
            
        Returns:
            True if cached
        """
        return key in self._cache if self._enabled else False
    
    def invalidate(self, key: str = None) -> None:
        """Invalidate cache entry or entire cache
        
        Args:
            key: Specific key to invalidate, or None for entire cache
        """
        try:
            if key is None:
                self._cache.clear()
            elif key in self._cache:
                del self._cache[key]
        except Exception as e:
            print(f"⚠️  Cache invalidation failed: {e}")
    
    def refresh(self, key: str, refresh_func) -> pd.DataFrame:
        """Refresh cached item or fetch if not cached
        
        Args:
            key: Cache key
            refresh_func: Function to call to get fresh data
            
        Returns:
            Fresh DataFrame from refresh_func
        """
        try:
            # Remove from cache to force refresh
            if key in self._cache:
                del self._cache[key]
            
            # Call refresh function
            data = refresh_func()
            
            # Cache result
            self.put(key, data, source="refresh")
            
            return data
        except Exception as e:
            print(f"⚠️  Cache refresh failed for key '{key}': {e}")
            # Return fresh data without caching
            return refresh_func()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics
        
        Returns:
            Dictionary with cache stats
        """
        total_requests = self._hit_count + self._miss_count
        hit_rate = (self._hit_count / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'enabled': self._enabled,
            'created_at': self._created_at.isoformat(),
            'cached_items': len(self._cache),
            'hits': self._hit_count,
            'misses': self._miss_count,
            'hit_rate': f"{hit_rate:.1f}%",
            'uptime_seconds': (datetime.now() - self._created_at).total_seconds(),
        }
    
    def disable(self) -> None:
        """Disable cache (for testing or recovery)"""
        self._enabled = False
        self._cache.clear()
    
    def enable(self) -> None:
        """Enable cache"""
        self._enabled = True
    
    def list_cached_keys(self) -> list:
        """List all cached keys
        
        Returns:
            List of cached keys
        """
        return list(self._cache.keys())
    
    def get_info(self, key: str) -> Optional[Dict[str, Any]]:
        """Get metadata about cached item
        
        Args:
            key: Cache key
            
        Returns:
            Metadata dict or None
        """
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        return {
            'source': entry['source'],
            'cached_at': entry['cached_at'],
            'shape': entry['shape'],
            'dtypes': entry['dtypes'],
        }


# Global session cache
_global_cache: Optional[SessionCache] = None


def initialize_cache() -> SessionCache:
    """Initialize global session cache
    
    Returns:
        Global SessionCache instance
    """
    global _global_cache
    _global_cache = SessionCache()
    return _global_cache


def get_cache() -> Optional[SessionCache]:
    """Get global session cache
    
    Returns:
        Global SessionCache instance or None if not initialized
    """
    return _global_cache


def cache_dataset(key: str, data: pd.DataFrame, source: str = "") -> None:
    """Cache a dataset
    
    Args:
        key: Cache key
        data: DataFrame to cache
        source: Description of data source
    """
    if _global_cache is not None:
        _global_cache.put(key, data, source)


def get_cached_dataset(key: str) -> Optional[pd.DataFrame]:
    """Retrieve cached dataset
    
    Args:
        key: Cache key
        
    Returns:
        Cached DataFrame or None
    """
    if _global_cache is not None:
        return _global_cache.get(key)
    return None


def invalidate_cache(key: str = None) -> None:
    """Invalidate cache entry or entire cache
    
    Args:
        key: Specific key to invalidate, or None for entire cache
    """
    if _global_cache is not None:
        _global_cache.invalidate(key)


def refresh_cached_dataset(key: str, refresh_func) -> pd.DataFrame:
    """Refresh cached dataset
    
    Args:
        key: Cache key
        refresh_func: Function to call to get fresh data
        
    Returns:
        Fresh DataFrame
    """
    if _global_cache is not None:
        return _global_cache.refresh(key, refresh_func)
    return refresh_func()


def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics
    
    Returns:
        Cache statistics dictionary
    """
    if _global_cache is None:
        return {'status': 'not_initialized'}
    return _global_cache.get_stats()


def is_cached(key: str) -> bool:
    """Check if key is cached
    
    Args:
        key: Cache key
        
    Returns:
        True if cached
    """
    if _global_cache is None:
        return False
    return _global_cache.exists(key)
