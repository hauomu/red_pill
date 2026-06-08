#!/usr/bin/env python3
"""Data Loader - Extract and prepare training data from SQLite with caching"""

import pandas as pd
from sklearn.model_selection import train_test_split
from src.database import Database
from src.database_registry import get_database_path
from src.session_cache import get_cached_dataset, cache_dataset


class DataLoader:
    """Load and prepare data from SQLite database"""
    
    def __init__(self, db_path: str, feature_cols: list = None, target_col: str = 'rating',
                 target_threshold: float = 4.0):
        """Initialize data loader
        
        Args:
            db_path: Path to SQLite database
            feature_cols: List of feature columns to use (if None, uses defaults)
            target_col: Target column name
            target_threshold: Threshold for binary classification
        """
        self.db_path = db_path
        self.feature_cols = feature_cols or [
            'branch', 'delivery_priority', 'vehicle_type',
            'distance_km', 'num_stops_on_route',
            'driver_experience_months'
        ]
        self.target_col = target_col
        self.target_threshold = target_threshold
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
    
    def load_data(self) -> pd.DataFrame:
        """Load deliveries with feedback ratings from database
        
        Uses session cache if available (populated after validation).
        Falls back to direct database access if cache miss.
        
        Returns:
            DataFrame with deliveries and ratings
            
        Raises:
            ValueError: If data loading fails or validation fails
        """
        cache_key = 'deliveries_with_feedback'
        
        # Check cache first
        cached_data = get_cached_dataset(cache_key)
        if cached_data is not None:
            print(f"  📦 Using cached dataset ({len(cached_data)} records)")
            return cached_data
        
        try:
            with Database(self.db_path) as db:
                df = db.get_deliveries_with_feedback()
        except Exception as e:
            raise ValueError(f"Failed to load data from database: {e}")
        
        # Validate loaded data
        self._validate_data(df)
        
        # Cache validated data
        try:
            cache_dataset(cache_key, df, source=f"database:{self.db_path}")
        except Exception as e:
            # Cache failure doesn't affect pipeline
            print(f"  ⚠️  Could not cache dataset: {e}")
        
        return df
    
    def _validate_data(self, df: pd.DataFrame) -> None:
        """Validate loaded data
        
        Args:
            df: DataFrame to validate
            
        Raises:
            ValueError: If data validation fails
        """
        if df is None or df.empty:
            raise ValueError("Loaded dataset is empty")
        
        # Check required columns
        required_cols = ['branch', 'delivery_priority', 'vehicle_type',
                        'distance_km', 'num_stops_on_route',
                        'driver_experience_months', 'rating']
        
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Check for target column
        if df['rating'].isna().all():
            raise ValueError("Target column 'rating' has all missing values")
    
    def prepare_dataset(self, df: pd.DataFrame, test_size: float = 0.2,
                       random_state: int = 42) -> tuple:
        """Prepare train/test split using configured features and target
        
        Args:
            df: Input DataFrame
            test_size: Test set proportion
            random_state: Random seed
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
            
        Raises:
            ValueError: If data validation fails
        """
        # Create binary target
        # Using rating >= threshold as proxy for satisfied customer
        if self.target_col not in df.columns:
            raise ValueError(f"Target column '{self.target_col}' not found in data")
        
        # Create binary target: 1 if satisfied (rating >= threshold), 0 otherwise
        y = (df[self.target_col] >= self.target_threshold).astype(int)
        
        # Select features
        X = df[self.feature_cols].copy()
        
        # Validate features exist
        missing_features = [col for col in self.feature_cols if col not in X.columns]
        if missing_features:
            raise ValueError(f"Missing feature columns: {missing_features}")
        
        # Train/test split with stratification to maintain class distribution
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Validate splits
        if len(X_train) == 0 or len(X_test) == 0:
            raise ValueError(f"Train/test split produced empty sets: train={len(X_train)}, test={len(X_test)}")
        
        if len(y_train) == 0 or len(y_test) == 0:
            raise ValueError(f"Target split produced empty sets: train={len(y_train)}, test={len(y_test)}")
        
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        
        return X_train, X_test, y_train, y_test
