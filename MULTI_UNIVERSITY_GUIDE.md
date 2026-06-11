# 🎓 Multi-University Chatbot Guide

## 🌟 What's New

Your chatbot has been upgraded from a single-college assistant to a **Multi-University Assistant** supporting **5 colleges in Solapur**!

## 🏛️ Supported Universities

1. **Walchand Institute of Technology (WIT)**
   - Engineering College
   - B.Tech programs in CS, IT, Mechanical, Civil, etc.

2. **Walchand College of Arts and Science**
   - Arts and Science College
   - B.A., B.Sc., B.Com, M.A., M.Sc., M.Com

3. **KBP College of Engineering**
   - Engineering College
   - B.Tech programs + MBA

4. **D.Y. Patil Institute of Engineering and Technology**
   - Engineering College
   - B.Tech and M.Tech programs

5. **Punyashlok Ahilyadevi Holkar Solapur University**
   - Main University
   - Various UG, PG, and Ph.D. programs

## 🚀 How to Run

```bash
python -m streamlit run app_multi_university.py
```

## 💬 How to Use

### Method 1: Select University First
1. Open the app
2. Click on a university name in the sidebar
3. Ask your question
4. Get specific information about that university

### Method 2: Mention University in Question
Just mention the university name in your question:
- "What are the fees at WIT?"
- "Tell me about placements at KBP"
- "Which courses does DYP offer?"
- "How to apply to Walchand College?"

### Method 3: Compare Universities
Ask comparative questions:
- "Compare fees of all engineering colleges"
- "Which college has best placements?"
- "Show me all universities in Solapur"

## 📊 Information Available

For each university, you can ask about:

### 💰 Fees
- Annual tuition fees
- Hostel fees
- Total approximate cost

### 🎯 Placements
- Placement rate
- Average package
- Highest package
- Top recruiters
- Placement cell location

### 📚 Courses
- All programs offered
- Degree types
- Specializations

### 📝 Admission
- Admission process
- Entrance exams required
- Eligibility criteria

### 🏠 Hostel
- Hostel availability
- Facilities provided
- Amenities

### 📞 Contact
- Address
- Phone number
- Email
- Website

### 🏛️ Facilities
- Library
- Labs
- Sports
- Infrastructure

### 🎭 Clubs & Activities
- Technical clubs
- Cultural clubs
- Sports clubs

## 💡 Sample Questions

### General Questions
```
"Tell me about WIT"
"What is Walchand College?"
"Show me all engineering colleges"
```

### Specific Questions
```
"What are the fees at KBP Engineering?"
"Tell me about placements at DYP"
"Which courses does Solapur University offer?"
"How to get admission in WIT?"
"Does Walchand College have hostel?"
"What is the contact number of KBP?"
```

### Comparative Questions
```
"Compare fees of WIT and KBP"
"Which college has better placements?"
"Show me all colleges with hostel facility"
```

## 🎨 Features

### ✅ Smart University Detection
- Automatically detects which university you're asking about
- Recognizes short names (WIT, KBP, DYP)
- Understands full names

### ✅ University Selection
- Select university from sidebar
- Visual indication of selected university
- Clear selection option

### ✅ Comprehensive Database
- All information stored in JSON format
- Easy to update and maintain
- Structured data for each university

### ✅ User-Friendly Interface
- Clean and modern design
- Dark mode support
- Feedback system
- Quick suggestion buttons

### ✅ Conversation Memory
- Remembers selected university
- Context-aware responses
- Follow-up questions supported

## 📁 Files Created

### Main Files
- `app_multi_university.py` - Multi-university chatbot
- `universities_database.json` - University database
- `MULTI_UNIVERSITY_GUIDE.md` - This guide

### Data Files (Auto-created)
- `chat_history_multi.json` - Chat history
- `feedback_multi.csv` - User feedback

## 🔧 Database Structure

```json
{
  "universities": [
    {
      "id": "unique_id",
      "university_name": "Full Name",
      "short_name": "Short Name",
      "city": "Solapur",
      "type": "College Type",
      "courses_offered": [...],
      "admission_process": "...",
      "fees": {...},
      "hostel_facility": "...",
      "contact_number": "...",
      "email": "...",
      "website": "...",
      "address": "...",
      "placement_information": {...},
      "facilities": [...],
      "clubs": [...]
    }
  ]
}
```

## 📝 Adding New Universities

To add more universities, edit `universities_database.json`:

```json
{
  "id": "new_college",
  "university_name": "New College Name",
  "short_name": "NCN",
  "city": "Solapur",
  "type": "Engineering College",
  "courses_offered": ["Course 1", "Course 2"],
  "admission_process": "Admission details...",
  "fees": {
    "annual_tuition": "₹XX,XXX",
    "hostel_fee": "₹XX,XXX",
    "total_approximate": "₹XX,XXX"
  },
  "hostel_facility": "Yes/No with details",
  "contact_number": "Phone",
  "email": "email@college.edu",
  "website": "https://college.edu",
  "address": "Full address",
  "placement_information": {
    "placement_rate": "XX%",
    "average_package": "₹X LPA",
    "highest_package": "₹X LPA",
    "top_recruiters": ["Company1", "Company2"],
    "placement_cell_location": "Location"
  },
  "facilities": ["Facility1", "Facility2"],
  "clubs": ["Club1", "Club2"]
}
```

## 🎯 Benefits

### For Students
- ✅ Compare multiple colleges easily
- ✅ Get accurate information quickly
- ✅ Make informed decisions
- ✅ Access all details in one place

### For Administrators
- ✅ Centralized information system
- ✅ Easy to update data
- ✅ Track user queries
- ✅ Collect feedback

### For Developers
- ✅ Clean code structure
- ✅ JSON-based database
- ✅ Easy to extend
- ✅ Modular design

## 🔄 Migration from Single College

### What Changed
- ❌ Single college focus → ✅ Multi-university support
- ❌ Fixed handbook → ✅ Dynamic JSON database
- ❌ One data source → ✅ Multiple university records
- ✅ All original features retained

### What Stayed Same
- ✅ Dark mode toggle
- ✅ Feedback system
- ✅ Chat history
- ✅ Modern UI
- ✅ Conversation memory

## 🐛 Troubleshooting

### University not detected?
- Make sure to mention the university name clearly
- Use short names: WIT, KBP, DYP
- Or select from sidebar first

### Information not found?
- Check if the question is specific enough
- Try rephrasing the question
- Select the university from sidebar

### Database not loading?
- Verify `universities_database.json` exists
- Check JSON syntax is valid
- Restart the app

## 🎉 You're Ready!

Run the multi-university chatbot:
```bash
python -m streamlit run app_multi_university.py
```

Open: **http://localhost:8501**

Start exploring colleges in Solapur! 🎓✨
