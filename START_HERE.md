# 🎓 WIT Campus Chatbot - START HERE

## 🚀 Three Ways to Run

### ⚡ Method 1: Double-Click (Easiest)
1. Find `RUN_CHATBOT.bat` in your project folder
2. Double-click it
3. Wait for browser to open automatically
4. Start chatting!

### 💻 Method 2: Command Line
```bash
# Step 1: Open Command Prompt
# Press Windows + R, type "cmd", press Enter

# Step 2: Go to project folder
cd C:\Users\ritik\OneDrive\Desktop\Campus_info_chatbot

# Step 3: Activate virtual environment
venv\Scripts\activate

# Step 4: Run the app
python -m streamlit run app_history.py
```

### 🌐 Method 3: Already Running
If the app is already running, just open your browser and go to:
**http://localhost:8501**

## 📱 What You'll See

```
┌─────────────────────────────────────────────────────────┐
│  🎓 WIT Campus Assistant              [🌙 Dark Mode]    │
├──────────────────────┬──────────────────────────────────┤
│                      │                                  │
│  📚 Chat History     │  📚 Welcome Screen               │
│  ─────────────       │  Campus Assistant with History   │
│  Today               │                                  │
│  💬 Placement...     │  💾 Auto-Save                    │
│  💬 Hostel fees...   │  📅 Date Grouped                 │
│                      │  🔍 Searchable                   │
│  Yesterday           │                                  │
│  💬 Exam dates...    │  👇 Start your first            │
│                      │     conversation!                │
│  🆕 New Chat         │                                  │
│                      ├──────────────────────────────────┤
│  📊 Campus Stats     │  💡 Quick Suggestions            │
│  2000+ Students      │  [Where is placement cell?]      │
│  150+ Faculty        │  [What are its timings?]         │
│  85% Placement       │  [Tell me about hostel fees]     │
│                      │  [What facilities does it have?] │
│  🏆 Achievements     │                                  │
│  🥇 Best College     │                                  │
│  🎯 100% Placement   │                                  │
│                      │                                  │
│  🏛️ Departments      │                                  │
│  💻 Computer Science │                                  │
│  ⚡ Electronics      │                                  │
│  ⚙️ Mechanical       │                                  │
│                      │                                  │
└──────────────────────┴──────────────────────────────────┘
```

## 💬 Try These Questions

1. **"Where is the placement cell?"**
   - Bot will tell you the location

2. **"What are its timings?"** (Follow-up)
   - Bot remembers you're asking about placement cell

3. **"Tell me about hostel fees"**
   - Get fee structure information

4. **"How to join coding club?"**
   - Learn about club registration

## ✨ Features to Explore

### 🌙 Dark Mode
- Click the button in top-right corner
- Toggle between light and dark themes
- Smooth color transitions

### 👍👎 Feedback
- After each bot response, you'll see:
  - [👍 Helpful] [👎 Not Helpful]
- Click to rate the response
- See thank you message

### 📚 Chat History
- All conversations auto-saved
- Grouped by date (Today, Yesterday, etc.)
- Click any conversation to reload it
- Use "New Chat" to start fresh

### 🧠 Smart Memory
- Bot remembers previous messages
- Understands "it", "its", "there"
- Gives context-aware answers

## 🛑 How to Stop

Press `Ctrl + C` in the terminal window

## 📊 View Your Feedback Data

```bash
python view_feedback.py
```

Shows:
- Total feedback count
- Helpful vs Not Helpful
- Satisfaction rate
- Recent feedback entries

## 🔧 If Something Goes Wrong

### App won't start?
```bash
# Reinstall packages
pip install -r requirements.txt
```

### Port already in use?
```bash
# Use different port
python -m streamlit run app_history.py --server.port 8502
```

### Virtual environment issues?
```bash
# Recreate virtual environment
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 📁 Project Files

```
Campus_info_chatbot/
│
├── 🚀 RUN_CHATBOT.bat        ← Double-click this!
├── 📱 app_history.py          ← Main app
├── 📋 requirements.txt        ← Required packages
├── 📖 HOW_TO_RUN.md          ← Detailed guide
├── 📝 README_SIMPLE.txt      ← Quick reference
│
├── data/
│   ├── handbook.txt          ← Campus info
│   └── wit_college.jpg       ← College photo
│
├── venv/                     ← Virtual environment
├── feedback.csv              ← Feedback data
└── chat_history.json         ← Chat history
```

## 🎯 Quick Commands

| Command | What it does |
|---------|-------------|
| `RUN_CHATBOT.bat` | Start the app (easiest) |
| `python -m streamlit run app_history.py` | Start manually |
| `python view_feedback.py` | View feedback stats |
| `python test_all_features.py` | Test everything |
| `Ctrl + C` | Stop the app |

## 🎉 You're All Set!

1. Run the app using any method above
2. Open http://localhost:8501 in your browser
3. Start asking questions
4. Explore all the features

**Enjoy your WIT Campus Assistant!** 🎓✨

---

Need help? Check:
- `HOW_TO_RUN.md` - Detailed instructions
- `README_SIMPLE.txt` - Quick reference
- `FEEDBACK_FEATURE.md` - Feedback system guide
- `FEATURES_RESTORED.md` - All features list
