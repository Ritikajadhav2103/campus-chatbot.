@echo off
echo ========================================
echo   Solapur Colleges Chatbot
echo ========================================
echo.
echo Chat with AI to get detailed information
echo about colleges in Solapur including:
echo   • College Photos
echo   • History
echo   • Courses Offered
echo   • Location & Contact
echo   • Official Website
echo.
echo ========================================

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the chatbot
echo Starting Solapur Colleges Chatbot...
echo.
echo Access at: http://localhost:8501
echo.
echo Press Ctrl+C to stop
echo ========================================
echo.

python -m streamlit run app_solapur_chat.py

pause
