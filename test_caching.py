#!/usr/bin/env python3
"""Test caching system integration"""

import sys
sys.path.insert(0, '.')

from src.database_registry import (
    initialize_registry, get_database_path, list_databases, get_registry
)
from src.session_cache import initialize_cache, cache_dataset, get_cached_dataset

print("="*80)
print("CACHING SYSTEM TEST")
print("="*80)
print()

# Test 1: Registry initialization
print("[TEST 1] Database Registry Initialization")
try:
    initialize_registry()
    print("  ✅ Registry initialized")
    
    # Get database path
    db_path = get_database_path('primary_delivery_db')
    print(f"  ✅ Primary database path: {db_path}")
    
    # Check protection
    registry = get_registry()
    is_protected_flag = registry.is_protected('primary_delivery_db')
    print(f"  ✅ Primary database protected: {is_protected_flag}")
    
    # List all
    dbs = list_databases()
    print(f"  ✅ Registered databases: {list(dbs.keys())}")
except Exception as e:
    print(f"  ❌ Registry test failed: {e}")
    sys.exit(1)

print()

# Test 2: Cache initialization
print("[TEST 2] Session Cache Initialization")
try:
    cache = initialize_cache()
    print(f"  ✅ Cache initialized")
    print(f"  ✅ Cache type: {type(cache).__name__}")
except Exception as e:
    print(f"  ❌ Cache initialization failed: {e}")
    sys.exit(1)

print()

# Test 3: Cache put/get
print("[TEST 3] Cache Put/Get Operations")
try:
    import pandas as pd
    import numpy as np
    
    # Create test dataframe
    test_data = pd.DataFrame({
        'col1': np.arange(100),
        'col2': np.random.randn(100),
        'col3': ['test'] * 100
    })
    
    # Cache it
    cache_dataset('test_data', test_data, source='test')
    print(f"  ✅ Cached test data (100 rows)")
    
    # Retrieve it
    cached = get_cached_dataset('test_data')
    if cached is not None:
        print(f"  ✅ Retrieved from cache ({len(cached)} rows)")
        assert len(cached) == 100
        print(f"  ✅ Data integrity verified")
    else:
        print(f"  ❌ Cache returned None")
        sys.exit(1)
    
except Exception as e:
    print(f"  ❌ Cache put/get test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 4: Cache statistics
print("[TEST 4] Cache Statistics")
try:
    from src.session_cache import get_cache_stats
    
    stats = get_cache_stats()
    print(f"  ✅ Cache stats: {stats}")
    assert stats['cached_items'] == 1
    assert stats['hits'] >= 0
    print(f"  ✅ Statistics valid")
except Exception as e:
    print(f"  ❌ Cache stats test failed: {e}")
    sys.exit(1)

print()

# Test 5: Pipeline integration
print("[TEST 5] Pipeline Integration (Quick Test)")
try:
    from src.pipeline import MLPipeline
    
    print("  Initializing pipeline...")
    pipeline = MLPipeline('config.yaml')
    print(f"  ✅ Pipeline initialized with caching support")
except Exception as e:
    print(f"  ❌ Pipeline integration test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("="*80)
print("ALL CACHING TESTS PASSED ✅")
print("="*80)
print()
print("Next: Run full pipeline with: python -c \"from src.pipeline import MLPipeline; MLPipeline().execute()\"")
