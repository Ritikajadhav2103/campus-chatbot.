@echo off
echo ========================================
echo   Multi-University Chatbot Launcher
echo ========================================
echo.
echo Supporting 5 colleges in Solapur:
echo   1. Walchand Institute of Technology
echo   2. Walchand College of Arts and Science
echo   3. KBP College of Engineering
echo   4. D.Y. Patil Institute
echo   5. Solapur University
echo.
echo ========================================

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the multi-university chatbot
echo Starting Multi-University Assistant...
echo.
echo The app will open at: http://localhost:8501
echo.
echo Press Ctrl+C to stop
echo ========================================
echo.

python -m streamlit run app_multi_university.py

pause
