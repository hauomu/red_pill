#!/usr/bin/env python3
"""
Configuration Loader

Loads pipeline configuration from config.yaml
Supports environment variable overrides
Validates configuration schema and values
"""

import yaml
import os
from typing import Dict, Any


class ConfigLoader:
    """Load and manage pipeline configuration"""
    
    # Required configuration schema
    REQUIRED_KEYS = {
        'database': ['path'],
        'data': ['test_size', 'random_state'],
        'model': ['type', 'hyperparams'],
        'output': ['results_dir'],
    }
    
    SUPPORTED_MODELS = ['logistic_regression', 'random_forest', 'gradient_boosting']
    
    def __init__(self, config_path: str = 'config.yaml'):
        """Initialize config loader
        
        Args:
            config_path: Path to config.yaml
            
        Raises:
            FileNotFoundError: If config file not found
            ValueError: If config validation fails
        """
        self.config_path = config_path
        self.config = self._load_config()
        self._validate_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file
        
        Returns:
            Configuration dictionary
            
        Raises:
            FileNotFoundError: If config file not found
            ValueError: If YAML is malformed
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in config file: {e}")
        
        if config is None:
            raise ValueError("Config file is empty")
        
        # Override with environment variables if present
        self._apply_env_overrides(config)
        
        return config
    
    def _validate_config(self) -> None:
        """Validate configuration schema and values
        
        Raises:
            ValueError: If configuration is invalid
        """
        # Check required keys
        for section, keys in self.REQUIRED_KEYS.items():
            if section not in self.config:
                raise ValueError(f"Missing required config section: '{section}'")
            
            if not isinstance(self.config[section], dict):
                raise ValueError(f"Config section '{section}' must be a dictionary")
            
            for key in keys:
                if key not in self.config[section]:
                    raise ValueError(f"Missing required config key: '{section}.{key}'")
        
        # Validate data values
        self._validate_data_config()
        self._validate_model_config()
        self._validate_database_config()
    
    def _validate_database_config(self) -> None:
        """Validate database configuration"""
        db_path = self.config['database']['path']
        if not isinstance(db_path, str) or not db_path.strip():
            raise ValueError("database.path must be a non-empty string")
    
    def _validate_data_config(self) -> None:
        """Validate data configuration"""
        test_size = self.config['data']['test_size']
        if not isinstance(test_size, (int, float)):
            raise ValueError("data.test_size must be a number (0.0-1.0)")
        if not (0 < test_size < 1):
            raise ValueError("data.test_size must be between 0 and 1")
        
        random_state = self.config['data'].get('random_state')
        if random_state is not None and not isinstance(random_state, int):
            raise ValueError("data.random_state must be an integer or null")
    
    def _validate_model_config(self) -> None:
        """Validate model configuration"""
        model_type = self.config['model']['type']
        if model_type not in self.SUPPORTED_MODELS:
            raise ValueError(f"model.type '{model_type}' not supported. Supported: {self.SUPPORTED_MODELS}")
        
        hyperparams = self.config['model'].get('hyperparams', {})
        if not isinstance(hyperparams, dict):
            raise ValueError("model.hyperparams must be a dictionary")
    
    def _apply_env_overrides(self, config: Dict[str, Any]) -> None:
        """Apply environment variable overrides to config
        
        Args:
            config: Configuration dictionary to update
            
        Raises:
            ValueError: If environment variable has invalid value
        """
        # Database path
        if os.getenv('DB_PATH'):
            config['database']['path'] = os.getenv('DB_PATH')
        
        # Model type
        if os.getenv('MODEL_TYPE'):
            model_type = os.getenv('MODEL_TYPE')
            if model_type not in self.SUPPORTED_MODELS:
                raise ValueError(f"Invalid MODEL_TYPE env var: '{model_type}'. Supported: {self.SUPPORTED_MODELS}")
            config['model']['type'] = model_type
        
        # Train/test split
        if os.getenv('TEST_SIZE'):
            try:
                test_size = float(os.getenv('TEST_SIZE'))
                if not (0 < test_size < 1):
                    raise ValueError("TEST_SIZE must be between 0 and 1")
                config['data']['test_size'] = test_size
            except ValueError as e:
                raise ValueError(f"Invalid TEST_SIZE env var: {e}")
        
        # Random state
        if os.getenv('RANDOM_STATE'):
            try:
                config['data']['random_state'] = int(os.getenv('RANDOM_STATE'))
            except ValueError:
                raise ValueError(f"Invalid RANDOM_STATE env var: must be an integer")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key
        
        Args:
            key: Configuration key (e.g., 'model.type', 'data.test_size')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        
        return value
    
    def get_all(self) -> Dict[str, Any]:
        """Get entire configuration dictionary
        
        Returns:
            Complete configuration
        """
        return self.config
