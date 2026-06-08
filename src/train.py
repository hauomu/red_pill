#!/usr/bin/env python3
"""Training Module - Model training and evaluation with comprehensive metrics"""

from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                            confusion_matrix, roc_auc_score, classification_report)
from typing import Any, Dict
import json
import numpy as np


class Trainer:
    """Train ML models with robust evaluation"""
    
    def __init__(self, model: Any):
        """Initialize trainer
        
        Args:
            model: Scikit-learn model instance
            
        Raises:
            ValueError: If model is None or not a valid estimator
        """
        if model is None:
            raise ValueError("Model cannot be None")
        
        self.model = model
        self.training_results = {}
    
    def train(self, X_train, y_train) -> None:
        """Train model on training data
        
        Args:
            X_train: Training features
            y_train: Training labels
        """
        print("Training model...")
        self.model.fit(X_train, y_train)
        print("Training complete")
    
    def evaluate(self, X_test, y_test) -> Dict[str, Any]:
        """Evaluate model on test data with comprehensive metrics
        
        Args:
            X_test: Test features
            y_test: Test labels
            
        Returns:
            Dictionary of evaluation metrics
            
        Raises:
            ValueError: If evaluation fails
        """
        print("Evaluating model...")
        
        try:
            # Predictions
            y_pred = self.model.predict(X_test)
            y_pred_proba = None
            
            if hasattr(self.model, 'predict_proba'):
                y_pred_proba = self.model.predict_proba(X_test)[:, 1]
            
            # Basic metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, zero_division=0)
            recall = recall_score(y_test, y_pred, zero_division=0)
            f1 = f1_score(y_test, y_pred, zero_division=0)
            
            # Confusion matrix
            tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
            
            # Specificity
            specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
            
            # ROC-AUC (if predict_proba available)
            roc_auc = None
            if y_pred_proba is not None:
                try:
                    roc_auc = float(roc_auc_score(y_test, y_pred_proba))
                except Exception as e:
                    print(f"  ⚠️  Could not compute ROC-AUC: {e}")
            
            results = {
                'accuracy': float(accuracy),
                'precision': float(precision),
                'recall': float(recall),
                'f1': float(f1),
                'specificity': float(specificity),
                'confusion_matrix': {
                    'true_negatives': int(tn),
                    'false_positives': int(fp),
                    'false_negatives': int(fn),
                    'true_positives': int(tp),
                },
            }
            
            if roc_auc is not None:
                results['roc_auc'] = roc_auc
            
            self.training_results = results
            
            # Print results
            print(f"  Accuracy:     {accuracy:.4f}")
            print(f"  Precision:    {precision:.4f}")
            print(f"  Recall:       {recall:.4f}")
            print(f"  F1:           {f1:.4f}")
            print(f"  Specificity:  {specificity:.4f}")
            if roc_auc:
                print(f"  ROC-AUC:      {roc_auc:.4f}")
            
            return results
            
        except Exception as e:
            raise ValueError(f"Model evaluation failed: {e}")
    
    def save_results(self, output_path: str) -> None:
        """Save evaluation results to JSON
        
        Args:
            output_path: Path to save results
        """
        with open(output_path, 'w') as f:
            json.dump(self.training_results, f, indent=2)
        print(f"Results saved to {output_path}")
