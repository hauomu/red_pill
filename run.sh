#!/bin/bash

# AIAP24 ML Pipeline - Official Entrypoint
# Executes the complete ML pipeline from data loading through evaluation

set -e  # Exit on error

echo "================================================================================"
echo "AIAP24 ML PIPELINE - ENTRYPOINT"
echo "================================================================================"
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.9+"
    exit 1
fi

echo "✅ Python found: $(python --version)"
echo ""

# Check if config.yaml exists
if [ ! -f config.yaml ]; then
    echo "❌ config.yaml not found. Please create configuration file."
    exit 1
fi

echo "✅ Configuration file found: config.yaml"
echo ""

# Check if database exists
if [ ! -f ./data/delivery.db ]; then
    echo "❌ Database not found at ./data/delivery.db"
    exit 1
fi

echo "✅ Database found: ./data/delivery.db"
echo ""

# Create results directory
mkdir -p results
echo "✅ Results directory ready: ./results"
echo ""

# Execute pipeline
echo "================================================================================"
echo "Starting ML Pipeline Execution"
echo "================================================================================"
echo ""

python -c "
import sys
sys.path.insert(0, '.')
from src.pipeline import MLPipeline

try:
    pipeline = MLPipeline(config_path='config.yaml')
    results = pipeline.execute()
    sys.exit(0)
except Exception as e:
    print(f'❌ Pipeline execution failed: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
"

PIPELINE_EXIT_CODE=$?

if [ $PIPELINE_EXIT_CODE -eq 0 ]; then
    echo ""
    echo "================================================================================"
    echo "✅ ML PIPELINE EXECUTION SUCCESSFUL"
    echo "================================================================================"
    echo ""
    echo "Results saved to ./results/"
    echo ""
    exit 0
else
    echo ""
    echo "================================================================================"
    echo "❌ ML PIPELINE EXECUTION FAILED"
    echo "================================================================================"
    echo ""
    exit 1
fi
