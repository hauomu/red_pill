#!/usr/bin/env python3
"""Pipeline Orchestrator - Main ML pipeline workflow with robust error handling"""

from src.config_loader import ConfigLoader
from src.data_loader import DataLoader
from src.preprocessing import Preprocessor
from src.model_factory import ModelFactory
from src.train import Trainer
from src.database_registry import initialize_registry, get_database_path
from src.session_cache import initialize_cache, get_cache_stats
import os
import logging
from datetime import datetime


class MLPipeline:
    """Complete ML pipeline orchestrator with comprehensive error handling"""
    
    def __init__(self, config_path: str = 'config.yaml'):
        """Initialize pipeline
        
        Args:
            config_path: Path to config.yaml
            
        Raises:
            ValueError: If configuration loading fails
            FileNotFoundError: If required files not found
        """
        try:
            self.config = ConfigLoader(config_path).get_all()
        except (FileNotFoundError, ValueError) as e:
            raise ValueError(f"Configuration error: {e}")
        
        # Setup logging
        self.log_file = None
        self._setup_logging()
        
        self.model = None
        self.trainer = None
    
    def _setup_logging(self) -> None:
        """Setup logging to file and console"""
        log_dir = self.config.get('output', {}).get('results_dir', 'results')
        os.makedirs(log_dir, exist_ok=True)
        
        log_path = os.path.join(log_dir, 'pipeline.log')
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_path),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.log_file = log_path
    
    def execute(self) -> dict:
        """Execute complete ML pipeline with error handling
        
        Returns:
            Dictionary of evaluation results
            
        Raises:
            ValueError: If any pipeline step fails
        """
        print("\n" + "="*80)
        print("AIAP24 ML PIPELINE - EXECUTION START")
        print(f"Start time: {datetime.now().isoformat()}")
        print("="*80 + "\n")
        
        try:
            # Pre-initialization: Initialize database registry & cache
            # Step [0/5]: Run before data loading to set up centralized path management.
            # If initialization fails, pipeline continues with direct database access.
            print("[0/5] Initializing database registry and cache...")
            try:
                initialize_registry()  # Register primary database with protection flags
                initialize_cache()     # Create session-scoped cache (lazy population)
                print(f"  ✅ Database registry initialized")
                print(f"  ✅ Session cache initialized")
            except Exception as e:
                print(f"  ⚠️  Could not initialize registry/cache: {e}")
                print(f"  ℹ️  Pipeline will continue with direct database access")
            
            print()
            
            # Step 1: Load data
            print("[1/5] Loading data from SQLite database...")
            db_path = self.config['database']['path']
            
            # Validate database exists
            if not os.path.exists(db_path):
                raise FileNotFoundError(f"Database not found: {db_path}")
            
            # Get feature configuration
            feature_config = self.config.get('features', {})
            feature_cols = feature_config.get('feature_cols')
            target_col = feature_config.get('target_col', 'rating')
            target_threshold = feature_config.get('target_threshold', 4.0)
            imputation_strategy = feature_config.get('imputation_strategy', 'mean')
            
            loader = DataLoader(db_path, feature_cols=feature_cols,
                              target_col=target_col,
                              target_threshold=target_threshold)
            df = loader.load_data()
            print(f"  ✅ Loaded {len(df)} delivery records with feedback")
            
            # Step 2: Prepare dataset
            print("\n[2/5] Preparing train/test split...")
            X_train, X_test, y_train, y_test = loader.prepare_dataset(
                df,
                test_size=self.config['data']['test_size'],
                random_state=self.config['data']['random_state']
            )
            print(f"  ✅ Train: {len(X_train)} | Test: {len(X_test)}")
            print(f"  Target distribution (train): {dict(y_train.value_counts())}")
            
            # Step 3: Preprocessing
            print("\n[3/5] Preprocessing data (encoding, scaling)...")
            preprocessor = Preprocessor(imputation_strategy=imputation_strategy)
            X_train_processed = preprocessor.fit_transform(X_train)
            X_test_processed = preprocessor.transform(X_test)
            print(f"  ✅ Preprocessing complete")
            print(f"  Features: {X_train_processed.shape[1]} | Train: {X_train_processed.shape[0]} | Test: {X_test_processed.shape[0]}")
            
            # Step 4: Create & Train model
            print("\n[4/5] Creating and training model...")
            model_type = self.config['model']['type']
            hyperparams = self.config['model']['hyperparams']
            print(f"  Model type: {model_type}")
            print(f"  Hyperparameters: {hyperparams}")
            
            self.model = ModelFactory.create_model(model_type, hyperparams)
            self.trainer = Trainer(self.model)
            self.trainer.train(X_train_processed, y_train)
            
            # Step 5: Evaluate
            print("\n[5/5] Evaluating model...")
            results = self.trainer.evaluate(X_test_processed, y_test)
            
            # Save results
            output_dir = self.config.get('output', {}).get('results_dir', 'results')
            os.makedirs(output_dir, exist_ok=True)
            results_path = os.path.join(output_dir, 'evaluation_results.json')
            self.trainer.save_results(results_path)
            print(f"  ✅ Results saved to {results_path}")
            
            # Report cache statistics
            print("\n[Cache Statistics]")
            cache_stats = get_cache_stats()
            if cache_stats.get('status') != 'not_initialized':
                print(f"  Cache Status: Enabled")
                print(f"  Cached Items: {cache_stats.get('cached_items', 0)}")
                print(f"  Cache Hits: {cache_stats.get('hits', 0)}")
                print(f"  Cache Misses: {cache_stats.get('misses', 0)}")
                print(f"  Hit Rate: {cache_stats.get('hit_rate', 'N/A')}")
            else:
                print(f"  Cache Status: Not initialized")
            
            print("\n" + "="*80)
            print(f"PIPELINE EXECUTION COMPLETE ✅")
            print(f"End time: {datetime.now().isoformat()}")
            print("="*80 + "\n")
            
            return results
        
        except Exception as e:
            print("\n" + "="*80)
            print(f"❌ PIPELINE EXECUTION FAILED")
            print(f"Error: {e}")
            print("="*80 + "\n")
            raise
