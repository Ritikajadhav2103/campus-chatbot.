@echo off
echo ========================================
echo   Solapur Colleges Guide Launcher
echo ========================================
echo.
echo Comprehensive guide to 35+ colleges
echo in Solapur across 6 categories:
echo   • Universities
echo   • Engineering Colleges
echo   • Medical & Health Colleges
echo   • Commerce / Management Colleges
echo   • Arts / Science Colleges
echo   • Other Colleges
echo.
echo ========================================

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the app
echo Starting Solapur Colleges Guide...
echo.
echo Access at: http://localhost:8501
echo.
echo Press Ctrl+C to stop
echo ========================================
echo.

python -m streamlit run app_solapur_enhanced.py

pause
