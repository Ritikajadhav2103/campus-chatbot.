@echo off
echo ========================================
echo   Solapur Colleges Chatbot - OPTIMIZED
echo ========================================
echo.
echo Features:
echo   ✅ Lightning fast responses (under 0.5s)
echo   ✅ Modern chat bubbles with animations
echo   ✅ Typing indicator
echo   ✅ Quick reply buttons
echo   ✅ Beautiful college cards
echo   ✅ Smart search
echo   ✅ Chat history
echo   ✅ Mobile-friendly design
echo.
echo ========================================

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the optimized chatbot
echo Starting Optimized Chatbot...
echo.
echo Access at: http://localhost:8501
echo.
echo Press Ctrl+C to stop
echo ========================================
echo.

python -m streamlit run app_solapur_optimized.py

pause
