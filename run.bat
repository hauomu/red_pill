@echo off
REM AIAP24 ML Pipeline - Windows Entrypoint
REM Executes the complete ML pipeline from data loading through evaluation

setlocal enabledelayedexpansion

echo ================================================================================
echo AIAP24 ML PIPELINE - ENTRYPOINT (Windows)
echo ================================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.9+
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] Python found: %PYTHON_VERSION%
echo.

REM Check if config.yaml exists
if not exist config.yaml (
    echo Error: config.yaml not found. Please create configuration file.
    exit /b 1
)

echo [OK] Configuration file found: config.yaml
echo.

REM Check if database exists
if not exist data\delivery.db (
    echo Error: Database not found at data\delivery.db
    exit /b 1
)

echo [OK] Database found: data\delivery.db
echo.

REM Create results directory
if not exist results mkdir results
echo [OK] Results directory ready: .\results
echo.

REM Execute pipeline
echo ================================================================================
echo Starting ML Pipeline Execution
echo ================================================================================
echo.

python -c "
import sys
sys.path.insert(0, '.')
from src.pipeline import MLPipeline

try:
    pipeline = MLPipeline(config_path='config.yaml')
    results = pipeline.execute()
    sys.exit(0)
except Exception as e:
    print(f'Error: Pipeline execution failed: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
"

if errorlevel 1 (
    echo.
    echo ================================================================================
    echo Error: ML PIPELINE EXECUTION FAILED
    echo ================================================================================
    echo.
    exit /b 1
)

echo.
echo ================================================================================
echo SUCCESS: ML PIPELINE EXECUTION COMPLETE
echo ================================================================================
echo.
echo Results saved to .\results\
echo.
exit /b 0
