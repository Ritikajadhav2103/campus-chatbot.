@echo off
echo ========================================
echo   WIT Campus Chatbot Launcher
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Check if packages are installed
echo Checking packages...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    echo.
)

REM Run the chatbot
echo ========================================
echo   Starting WIT Campus Chatbot...
echo ========================================
echo.
echo The app will open in your browser at:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the app
echo ========================================
echo.

python -m streamlit run app_history.py

pause
