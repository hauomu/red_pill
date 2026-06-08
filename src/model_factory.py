#!/usr/bin/env python3
"""Model Factory - Create swappable model instances"""

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from typing import Any, Dict


class ModelFactory:
    """Create ML model instances based on configuration"""
    
    SUPPORTED_MODELS = {
        'logistic_regression': LogisticRegression,
        'random_forest': RandomForestClassifier,
        'gradient_boosting': GradientBoostingClassifier,
    }
    
    @staticmethod
    def create_model(model_type: str, hyperparams: Dict[str, Any]) -> Any:
        """Create a model instance
        
        Args:
            model_type: Type of model ('logistic_regression', 'random_forest', etc.)
            hyperparams: Model hyperparameters
            
        Returns:
            Model instance
        """
        if model_type not in ModelFactory.SUPPORTED_MODELS:
            raise ValueError(f"Unsupported model type: {model_type}")
        
        model_class = ModelFactory.SUPPORTED_MODELS[model_type]
        return model_class(**hyperparams)
    
    @staticmethod
    def get_supported_models() -> list:
        """Get list of supported model types
        
        Returns:
            List of supported model type names
        """
        return list(ModelFactory.SUPPORTED_MODELS.keys())
