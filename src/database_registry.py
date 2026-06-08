#!/usr/bin/env python3
"""
Database Registry Module

Centralizes database path management and protection.
Provides single source of truth for all database locations.
Supports multiple databases with protection flags.
"""

import os
from typing import Dict, Any, Optional
from datetime import datetime


class DatabaseRegistry:
    """Centralized database path management with protection"""
    
    def __init__(self):
        """Initialize empty registry"""
        self._registry: Dict[str, Dict[str, Any]] = {}
        self._initialized = False
    
    def register(self, name: str, path: str, protected: bool = False,
                description: str = "") -> None:
        """Register a database
        
        Args:
            name: Unique database identifier
            path: Path to database file
            protected: If True, prevent accidental modifications
            description: Human-readable description
            
        Raises:
            ValueError: If name already registered (unless overwriting protected)
            FileNotFoundError: If path doesn't exist
        """
        # Validate path exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"Database path not found: {path}")
        
        # Check if already registered
        if name in self._registry:
            existing = self._registry[name]
            if existing.get('protected', False):
                raise ValueError(
                    f"Cannot overwrite protected database '{name}'. "
                    f"Use update() with force=True to override."
                )
        
        # Register database
        self._registry[name] = {
            'path': path,
            'protected': protected,
            'description': description,
            'registered_at': datetime.now().isoformat(),
            'access_count': 0,
        }
    
    def get(self, name: str) -> str:
        """Get database path by name
        
        Args:
            name: Database identifier
            
        Returns:
            Path to database
            
        Raises:
            KeyError: If database not registered
        """
        if name not in self._registry:
            raise KeyError(
                f"Database '{name}' not registered. "
                f"Available: {list(self._registry.keys())}"
            )
        
        entry = self._registry[name]
        # Increment access count
        entry['access_count'] += 1
        return entry['path']
    
    def exists(self, name: str) -> bool:
        """Check if database is registered
        
        Args:
            name: Database identifier
            
        Returns:
            True if registered
        """
        return name in self._registry
    
    def update(self, name: str, path: str, force: bool = False) -> None:
        """Update database path
        
        Args:
            name: Database identifier
            path: New path
            force: If True, override protected databases
            
        Raises:
            ValueError: If database protected and force=False
            KeyError: If database not registered
            FileNotFoundError: If path doesn't exist
        """
        if name not in self._registry:
            raise KeyError(f"Database '{name}' not registered")
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Database path not found: {path}")
        
        entry = self._registry[name]
        if entry.get('protected', False) and not force:
            raise ValueError(
                f"Cannot update protected database '{name}'. "
                f"Use force=True to override."
            )
        
        entry['path'] = path
        entry['updated_at'] = datetime.now().isoformat()
    
    def list_all(self) -> Dict[str, Dict[str, Any]]:
        """List all registered databases
        
        Returns:
            Dictionary of all registered databases with metadata
        """
        return {name: entry.copy() for name, entry in self._registry.items()}
    
    def get_info(self, name: str) -> Dict[str, Any]:
        """Get detailed info about a database
        
        Args:
            name: Database identifier
            
        Returns:
            Dictionary with database metadata
        """
        if name not in self._registry:
            raise KeyError(f"Database '{name}' not registered")
        
        return self._registry[name].copy()
    
    def is_protected(self, name: str) -> bool:
        """Check if database is protected
        
        Args:
            name: Database identifier
            
        Returns:
            True if protected
        """
        if name not in self._registry:
            return False
        return self._registry[name].get('protected', False)
    
    def clear(self, force: bool = False) -> None:
        """Clear all registered databases
        
        Args:
            force: If False, raises error if any protected databases exist
            
        Raises:
            ValueError: If protected databases exist and force=False
        """
        # Check for protected databases
        if not force:
            protected = [name for name, entry in self._registry.items()
                        if entry.get('protected', False)]
            if protected:
                raise ValueError(
                    f"Cannot clear registry with protected databases: {protected}. "
                    f"Use force=True to override."
                )
        
        self._registry.clear()


# Global registry instance
_global_registry = DatabaseRegistry()


def initialize_registry() -> None:
    """Initialize global database registry with default databases"""
    # Register primary delivery database
    _global_registry.register(
        name='primary_delivery_db',
        path='./data/delivery.db',
        protected=True,
        description='Primary SQLite database for delivery and feedback data'
    )


def register_database(name: str, path: str, protected: bool = False,
                     description: str = "") -> None:
    """Register a database in global registry
    
    Args:
        name: Unique database identifier
        path: Path to database file
        protected: If True, prevent accidental modifications
        description: Human-readable description
    """
    _global_registry.register(name, path, protected, description)


def get_database_path(name: str) -> str:
    """Get database path from global registry
    
    Args:
        name: Database identifier
        
    Returns:
        Path to database
        
    Raises:
        KeyError: If database not registered
    """
    return _global_registry.get(name)


def database_exists(name: str) -> bool:
    """Check if database is registered
    
    Args:
        name: Database identifier
        
    Returns:
        True if registered
    """
    return _global_registry.exists(name)


def update_database_path(name: str, path: str, force: bool = False) -> None:
    """Update database path in global registry
    
    Args:
        name: Database identifier
        path: New path
        force: If True, override protected databases
    """
    _global_registry.update(name, path, force)


def list_databases() -> Dict[str, Dict[str, Any]]:
    """List all registered databases
    
    Returns:
        Dictionary of all registered databases
    """
    return _global_registry.list_all()


def get_registry() -> DatabaseRegistry:
    """Get global registry instance (for testing/advanced use)
    
    Returns:
        Global DatabaseRegistry instance
    """
    return _global_registry
