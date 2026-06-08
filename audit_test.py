#!/usr/bin/env python3
"""Audit test script - stress test all pipeline components"""

import sys
import traceback
from src.data_loader import DataLoader
from src.preprocessing import Preprocessor
from src.model_factory import ModelFactory
from src.train import Trainer

print("="*80)
print("PIPELINE AUDIT TEST - Component Validation")
print("="*80)

try:
    # Test 1: Data Loading
    print("\n[TEST 1] Data Loading...")
    loader = DataLoader('./data/delivery.db')
    df = loader.load_data()
    print(f"  ✅ Loaded {len(df)} records")
    print(f"  Columns: {len(df.columns)}")
    print(f"  Missing values: {df.isnull().sum().sum()}")
    
    # Test 2: Data Preparation
    print("\n[TEST 2] Data Preparation...")
    required_cols = ['branch', 'delivery_priority', 'vehicle_type', 'distance_km', 'num_stops_on_route', 'driver_experience_months', 'rating']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        print(f"  ❌ Missing required columns: {missing}")
    else:
        print(f"  ✅ All required columns present")
    
    X_train, X_test, y_train, y_test = loader.prepare_dataset(df)
    print(f"  ✅ Train/test split: {len(X_train)} train, {len(X_test)} test")
    print(f"  Target distribution (train): {dict(y_train.value_counts())}")
    
    # Test 3: Preprocessing
    print("\n[TEST 3] Preprocessing...")
    preprocessor = Preprocessor()
    X_train_proc = preprocessor.fit_transform(X_train)
    print(f"  ✅ Fitted on training data")
    print(f"  Training data shape after preprocessing: {X_train_proc.shape}")
    print(f"  Training data dtypes: {X_train_proc.dtypes.unique()}")
    
    X_test_proc = preprocessor.transform(X_test)
    print(f"  ✅ Transformed test data")
    print(f"  Test data shape after preprocessing: {X_test_proc.shape}")
    
    # Validate shapes match
    if X_train_proc.shape[1] != X_test_proc.shape[1]:
        print(f"  ❌ Shape mismatch: train has {X_train_proc.shape[1]} features, test has {X_test_proc.shape[1]}")
    else:
        print(f"  ✅ Feature dimensions match")
    
    # Test 4: Model Factory
    print("\n[TEST 4] Model Factory...")
    supported = ModelFactory.get_supported_models()
    print(f"  ✅ Supported models: {supported}")
    
    model = ModelFactory.create_model('logistic_regression', {'max_iter': 1000, 'random_state': 42, 'solver': 'lbfgs'})
    print(f"  ✅ Model created: {type(model).__name__}")
    
    # Test 5: Training & Evaluation
    print("\n[TEST 5] Training & Evaluation...")
    trainer = Trainer(model)
    trainer.train(X_train_proc, y_train)
    print(f"  ✅ Model trained")
    
    results = trainer.evaluate(X_test_proc, y_test)
    print(f"  ✅ Evaluation complete")
    print(f"  Results: {results}")
    
    print("\n" + "="*80)
    print("ALL TESTS PASSED ✅")
    print("="*80)
    
except Exception as e:
    print(f"\n❌ TEST FAILED: {e}")
    traceback.print_exc()
    sys.exit(1)
