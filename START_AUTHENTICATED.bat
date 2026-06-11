@echo off
title Solapur Colleges Chatbot - Authenticated
color 0A
echo.
echo ========================================
echo   Solapur Colleges Chatbot
echo   With User Authentication
echo ========================================
echo.
echo Starting chatbot...
echo.
echo The chatbot will open in your browser automatically.
echo.
echo Press Ctrl+C to stop the chatbot.
echo.
streamlit run app_authenticated.py --server.headless true
pause
