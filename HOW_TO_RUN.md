# 🚀 How to Run the Campus Chatbot Project

## 📋 Prerequisites

Before running the project, make sure you have:
- ✅ Python 3.12 installed (NOT 3.14)
- ✅ Internet connection (for downloading packages)

## 🔧 Step-by-Step Setup

### Step 1: Open Command Prompt or PowerShell
- Press `Windows + R`
- Type `cmd` or `powershell`
- Press Enter

### Step 2: Navigate to Project Folder
```bash
cd C:\Users\ritik\OneDrive\Desktop\Campus_info_chatbot
```

### Step 3: Create Virtual Environment (First Time Only)
```bash
python -m venv venv
```

### Step 4: Activate Virtual Environment
```bash
# For Command Prompt:
venv\Scripts\activate

# For PowerShell:
venv\Scripts\Activate.ps1
```

You should see `(venv)` at the beginning of your command line.

### Step 5: Install Required Packages (First Time Only)
```bash
pip install -r requirements.txt
```

This will install:
- streamlit
- langchain
- langchain-community
- langchain-huggingface
- sentence-transformers
- chromadb
- pypdf
- beautifulsoup4
- requests
- pandas

### Step 6: Run the Chatbot
```bash
python -m streamlit run app_history.py
```

### Step 7: Open in Browser
The terminal will show:
```
Local URL: http://localhost:8501
Network URL: http://10.x.x.x:8501
```

Click on the **Local URL** or open your browser and go to:
**http://localhost:8501**

## 🎯 Quick Commands

### Run the App
```bash
python -m streamlit run app_history.py
```

### View Feedback Data
```bash
python view_feedback.py
```

### Test All Features
```bash
python test_all_features.py
```

### Validate App Structure
```bash
python validate_app.py
```

## 🛑 How to Stop the App

Press `Ctrl + C` in the terminal where Streamlit is running.

## 🔄 Running Again (After First Setup)

1. Open Command Prompt/PowerShell
2. Navigate to project folder:
   ```bash
   cd C:\Users\ritik\OneDrive\Desktop\Campus_info_chatbot
   ```
3. Activate virtual environment:
   ```bash
   venv\Scripts\activate
   ```
4. Run the app:
   ```bash
   python -m streamlit run app_history.py
   ```

## 📁 Project Structure

```
Campus_info_chatbot/
├── app_history.py          # Main chatbot app (RUN THIS)
├── requirements.txt        # Required packages
├── data/
│   ├── handbook.txt       # Campus information
│   └── wit_college.jpg    # College photo (optional)
├── loaders/               # Data loaders
├── utils/                 # Utility functions
├── venv/                  # Virtual environment
├── feedback.csv           # Feedback data (auto-created)
└── chat_history.json      # Chat history (auto-created)
```

## ✨ Features Available

1. **💬 Chat Interface** - Ask questions about campus
2. **🧠 Conversation Memory** - Remembers context
3. **📚 Chat History** - Saves all conversations
4. **🌙 Dark Mode** - Toggle light/dark theme
5. **👍👎 Feedback** - Rate bot responses
6. **📊 Campus Stats** - View statistics
7. **🏆 Achievements** - Recent accomplishments
8. **🏛️ Departments** - List of departments
9. **📅 Events** - Upcoming events

## 🐛 Troubleshooting

### Error: "Python not found"
- Install Python 3.12 from python.org
- Make sure to check "Add Python to PATH" during installation

### Error: "streamlit not found"
- Make sure virtual environment is activated (you should see `(venv)`)
- Run: `pip install -r requirements.txt`

### Error: "Port already in use"
- Stop any other Streamlit apps running
- Or use a different port:
  ```bash
  python -m streamlit run app_history.py --server.port 8502
  ```

### Error: "Module not found"
- Activate virtual environment: `venv\Scripts\activate`
- Reinstall packages: `pip install -r requirements.txt`

### App is slow or not responding
- Check if handbook.txt exists in data folder
- Restart the app (Ctrl+C, then run again)

## 💡 Tips

### For Development
- Keep terminal open while using the app
- App auto-reloads when you save code changes
- Check terminal for error messages

### For Testing
- Try asking: "Where is placement cell?"
- Test follow-up: "What are its timings?"
- Toggle dark mode with 🌙/☀️ button
- Give feedback with 👍/👎 buttons

### For Production
- Use a stable internet connection
- Don't close the terminal while app is running
- Save important conversations (auto-saved)

## 📞 Need Help?

If you encounter issues:
1. Check the terminal for error messages
2. Make sure all files are in correct locations
3. Verify Python version: `python --version`
4. Verify packages installed: `pip list`
5. Try restarting the app

## 🎉 You're Ready!

Follow the steps above and your chatbot will be running at:
**http://localhost:8501**

Enjoy your WIT Campus Assistant! 🎓✨
