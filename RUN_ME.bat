@echo off
cd /d "C:\Users\ritik\OneDrive\Desktop\Campus_info_chatbot"
echo Starting Solapur Colleges Chatbot...
start "" "http://localhost:8501"
python -m streamlit run app_authenticated.py --server.headless false
pause
