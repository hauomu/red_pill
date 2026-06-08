#!/usr/bin/env python3
"""Preprocessing - Data cleaning, encoding, scaling with robustness"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler


class Preprocessor:
    """Data preprocessing and transformation with robust error handling"""
    
    def __init__(self, imputation_strategy: str = 'mean'):
        """Initialize preprocessor
        
        Args:
            imputation_strategy: Strategy for filling missing values ('mean', 'median', 'zero')
        """
        if imputation_strategy not in ['mean', 'median', 'zero']:
            raise ValueError(f"Invalid imputation_strategy: {imputation_strategy}")
        
        self.imputation_strategy = imputation_strategy
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_cols = None
        self.means = {}  # Store means for test set imputation
        self.medians = {}  # Store medians for test set imputation
    
    def fit_transform(self, X_train: pd.DataFrame) -> pd.DataFrame:
        """Fit encoders/scalers and transform training data
        
        Args:
            X_train: Training features
            
        Returns:
            Transformed training data
            
        Raises:
            ValueError: If feature validation fails
        """
        X = X_train.copy()
        # Store feature column names to enforce consistency during transform (test)
        # This prevents accidental mismatches between train and test feature sets
        self.feature_cols = X.columns
        
        # Validate features
        if X.empty:
            raise ValueError("Input DataFrame is empty")
        
        # Handle missing values
        X = self._fill_missing(X, fit=True)
        
        # Encode categorical variables
        categorical_cols = X.select_dtypes(include='object').columns
        for col in categorical_cols:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            self.label_encoders[col] = le
        
        # Scale numerical features
        numerical_cols = X.select_dtypes(include=[np.number]).columns
        X[numerical_cols] = self.scaler.fit_transform(X[numerical_cols])
        
        return X
    
    def transform(self, X_test: pd.DataFrame) -> pd.DataFrame:
        """Transform test data using fitted encoders/scalers
        
        Args:
            X_test: Test features
            
        Returns:
            Transformed test data
            
        Raises:
            ValueError: If feature validation fails
        """
        X = X_test.copy()
        
        # Validate feature columns match
        if set(X.columns) != set(self.feature_cols):
            raise ValueError(f"Feature columns mismatch. Expected {list(self.feature_cols)}, got {list(X.columns)}")
        
        # Fill missing values
        X = self._fill_missing(X, fit=False)
        
        # Encode categorical variables with unseen category handling
        for col in self.label_encoders:
            X[col] = self._safe_label_encode(col, X[col].astype(str))
        
        # Scale numerical features
        numerical_cols = X.select_dtypes(include=[np.number]).columns
        X[numerical_cols] = self.scaler.transform(X[numerical_cols])
        
        return X
    
    def _safe_label_encode(self, col: str, series: pd.Series) -> pd.Series:
        """Safely encode categorical feature, handling unseen categories
        
        Args:
            col: Column name
            series: Series to encode
            
        Returns:
            Encoded series
        """
        le = self.label_encoders[col]
        encoded = series.copy()
        
        # Find unseen categories
        known_classes = set(le.classes_)
        unseen_mask = ~series.isin(known_classes)
        
        if unseen_mask.any():
            # Fallback strategy for unseen categories in test data:
            # Use the first class (mode) from training data.
            # This is a safety mechanism for handling real-world data variations.
            unseen_count = unseen_mask.sum()
            print(f"  ⚠️  Warning: {unseen_count} unseen categories in '{col}'. Using mode for encoding.")
            encoded[unseen_mask] = le.transform([le.classes_[0]] * unseen_count)
            encoded[~unseen_mask] = le.transform(series[~unseen_mask])
        else:
            encoded = le.transform(series)
        
        return encoded
    
    def _fill_missing(self, X: pd.DataFrame, fit: bool = False) -> pd.DataFrame:
        """Fill missing values using configured strategy
        
        Args:
            X: DataFrame
            fit: If True, compute and store fill values (training mode)
                If False, use pre-computed values (test mode)
            
        Returns:
            DataFrame with filled missing values
        """
        X = X.copy()
        
        if X.isna().sum().sum() == 0:
            return X  # No missing values
        
        numerical_cols = X.select_dtypes(include=[np.number]).columns
        
        if fit:
            # Training mode: compute statistics
            for col in numerical_cols:
                if X[col].isna().any():
                    if self.imputation_strategy == 'mean':
                        self.means[col] = X[col].mean()
                        X[col].fillna(self.means[col], inplace=True)
                    elif self.imputation_strategy == 'median':
                        self.medians[col] = X[col].median()
                        X[col].fillna(self.medians[col], inplace=True)
                    elif self.imputation_strategy == 'zero':
                        X[col].fillna(0, inplace=True)
        else:
            # Test mode: use pre-computed statistics
            for col in numerical_cols:
                if X[col].isna().any():
                    if self.imputation_strategy == 'mean':
                        fill_value = self.means.get(col, X[col].mean())
                        X[col].fillna(fill_value, inplace=True)
                    elif self.imputation_strategy == 'median':
                        fill_value = self.medians.get(col, X[col].median())
                        X[col].fillna(fill_value, inplace=True)
                    elif self.imputation_strategy == 'zero':
                        X[col].fillna(0, inplace=True)
        
        # Fill categorical missing values with mode
        categorical_cols = X.select_dtypes(include='object').columns
        for col in categorical_cols:
            if X[col].isna().any():
                fill_value = X[col].mode()[0] if len(X[col].mode()) > 0 else 'UNKNOWN'
                X[col] = X[col].fillna(fill_value)
        
        return X
