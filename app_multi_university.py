import streamlit as st
import time
import json
import os
from datetime import datetime, date
import uuid

# Page config
st.set_page_config(
    page_title="Solapur Multi-University Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state FIRST
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_memory" not in st.session_state:
    st.session_state.conversation_memory = []
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = {}
if "selected_university" not in st.session_state:
    st.session_state.selected_university = None
if "universities_data" not in st.session_state:
    # Load universities database
    try:
        with open("universities_database.json", "r", encoding="utf-8") as f:
            st.session_state.universities_data = json.load(f)["universities"]
    except:
        st.session_state.universities_data = []

# Dynamic CSS based on theme
def get_theme_css(dark_mode):
    if dark_mode:
        return """
<style>
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --bg-color: #1a1a2e;
        --card-bg: #16213e;
        --text-color: #eaeaea;
        --text-secondary: #a0a0a0;
        --user-msg-bg: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --bot-msg-bg: #2d3748;
        --border-color: #3a3a52;
        --hover-bg: #252541;
        --shadow: rgba(0, 0, 0, 0.4);
    }
    .stApp {
        background-color: var(--bg-color);
        color: var(--text-color);
        transition: all 0.3s ease;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] {
        background-color: var(--card-bg);
        border-right: 1px solid var(--border-color);
    }
    .stTextInput input, .stChatInput input {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
        border-color: var(--border-color) !important;
    }
    .stButton button {
        background-color: var(--card-bg);
        color: var(--text-color);
        border: 1px solid var(--border-color);
    }
    .stButton button:hover {
        background-color: var(--hover-bg);
        border-color: var(--primary-color);
    }
"""
    else:
        return """
<style>
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --bg-color: #f8f9fa;
        --card-bg: #ffffff;
        --text-color: #212529;
        --text-secondary: #6c757d;
        --user-msg-bg: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --bot-msg-bg: #f1f3f5;
        --border-color: #e9ecef;
        --hover-bg: #f8f9ff;
        --shadow: rgba(0, 0, 0, 0.1);
    }
    .stApp {
        background-color: var(--bg-color);
        color: var(--text-color);
        transition: all 0.3s ease;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] {
        background-color: var(--card-bg);
        border-right: 1px solid var(--border-color);
    }
"""

# Apply theme CSS
st.markdown(get_theme_css(st.session_state.dark_mode), unsafe_allow_html=True)

# Common CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px var(--shadow);
        position: relative;
        transition: all 0.3s ease;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    .chat-container {
        background: transparent;
        border-radius: 15px;
        padding: 1.5rem;
        height: 600px;
        overflow-y: auto;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    .user-message {
        background: var(--user-msg-bg);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0 1rem auto;
        max-width: 70%;
        box-shadow: 0 2px 5px var(--shadow);
        animation: slideInRight 0.3s ease;
        transition: all 0.3s ease;
    }
    .bot-message {
        background: var(--bot-msg-bg);
        color: var(--text-color);
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem auto 1rem 0;
        max-width: 75%;
        box-shadow: 0 2px 5px var(--shadow);
        animation: slideInLeft 0.3s ease;
        transition: all 0.3s ease;
    }
    .timestamp {
        font-size: 0.75rem;
        color: var(--text-secondary);
        margin-top: 0.3rem;
        transition: all 0.3s ease;
    }
    .university-card {
        background: var(--card-bg);
        border: 2px solid var(--border-color);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px var(--shadow);
    }
    .university-card:hover {
        border-color: var(--primary-color);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px var(--shadow);
    }
    .university-card.selected {
        border-color: var(--primary-color);
        background: var(--hover-bg);
        border-width: 3px;
    }
    .sidebar-section {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px var(--shadow);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }
    .sidebar-section h3 {
        color: var(--primary-color);
        margin-bottom: 1rem;
        font-size: 1.2rem;
        transition: all 0.3s ease;
    }
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    .footer {
        text-align: center;
        padding: 1rem;
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-top: 2rem;
        transition: all 0.3s ease;
    }
    .stAlert {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
        border-color: var(--border-color) !important;
    }
    [data-testid="stMetricValue"] {
        color: var(--text-color) !important;
    }
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
    }
</style>
""", unsafe_allow_html=True)

# Feedback and Chat History Management
HISTORY_FILE = "chat_history_multi.json"
FEEDBACK_FILE = "feedback_multi.csv"

def save_feedback(message_index, feedback_type, question, answer, university):
    """Save feedback to CSV file"""
    import csv
    file_exists = os.path.exists(FEEDBACK_FILE)
    with open(FEEDBACK_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Timestamp', 'University', 'Message_Index', 'Feedback', 'Question', 'Answer'])
        writer.writerow([
            datetime.now().isoformat(),
            university if university else "Not specified",
            message_index,
            feedback_type,
            question[:100],
            answer[:200]
        ])

def detect_university(query):
    """Detect which university the user is asking about"""
    query_lower = query.lower()
    
    # Check for university mentions
    for uni in st.session_state.universities_data:
        if uni['short_name'].lower() in query_lower or uni['university_name'].lower() in query_lower:
            return uni['id']
        # Check for unique identifiers
        if uni['id'] == 'wit' and ('walchand institute' in query_lower or 'wit' in query_lower):
            return 'wit'
        elif uni['id'] == 'walchand_college' and 'walchand college' in query_lower and 'arts' in query_lower:
            return 'walchand_college'
        elif uni['id'] == 'kbp_college' and 'kbp' in query_lower:
            return 'kbp_college'
        elif uni['id'] == 'dypiet' and ('dyp' in query_lower or 'd.y. patil' in query_lower):
            return 'dypiet'
        elif uni['id'] == 'solapur_university' and 'solapur university' in query_lower:
            return 'solapur_university'
    
    return None

def search_university_info(query, university_id):
    """Search for information in the selected university's data"""
    # Find the university
    university = next((u for u in st.session_state.universities_data if u['id'] == university_id), None)
    
    if not university:
        return "University not found in database."
    
    query_lower = query.lower()
    response_parts = []
    
    # Search patterns
    if any(word in query_lower for word in ['fee', 'fees', 'cost', 'tuition', 'charges']):
        response_parts.append(f"**💰 Fee Structure at {university['short_name']}:**\n")
        response_parts.append(f"• Annual Tuition: {university['fees']['annual_tuition']}\n")
        if 'hostel_fee' in university['fees']:
            response_parts.append(f"• Hostel Fee: {university['fees']['hostel_fee']}\n")
        response_parts.append(f"• Total Approximate: {university['fees']['total_approximate']}\n")
    
    elif any(word in query_lower for word in ['placement', 'job', 'package', 'salary', 'recruiter']):
        response_parts.append(f"**🎯 Placement Information at {university['short_name']}:**\n")
        placement = university['placement_information']
        response_parts.append(f"• Placement Rate: {placement['placement_rate']}\n")
        response_parts.append(f"• Average Package: {placement['average_package']}\n")
        response_parts.append(f"• Highest Package: {placement['highest_package']}\n")
        response_parts.append(f"• Top Recruiters: {', '.join(placement['top_recruiters'][:3])}\n")
        response_parts.append(f"• Placement Cell: {placement['placement_cell_location']}\n")
    
    elif any(word in query_lower for word in ['course', 'program', 'degree', 'branch', 'stream']):
        response_parts.append(f"**📚 Courses Offered at {university['short_name']}:**\n")
        for course in university['courses_offered'][:6]:
            response_parts.append(f"• {course}\n")
    
    elif any(word in query_lower for word in ['admission', 'apply', 'entrance', 'eligibility']):
        response_parts.append(f"**📝 Admission Process at {university['short_name']}:**\n")
        response_parts.append(f"{university['admission_process']}\n")
    
    elif any(word in query_lower for word in ['hostel', 'accommodation', 'residence']):
        response_parts.append(f"**🏠 Hostel Facility at {university['short_name']}:**\n")
        response_parts.append(f"{university['hostel_facility']}\n")
    
    elif any(word in query_lower for word in ['contact', 'phone', 'email', 'address', 'location']):
        response_parts.append(f"**📞 Contact Information for {university['short_name']}:**\n")
        response_parts.append(f"• Address: {university['address']}\n")
        response_parts.append(f"• Phone: {university['contact_number']}\n")
        response_parts.append(f"• Email: {university['email']}\n")
        response_parts.append(f"• Website: {university['website']}\n")
    
    elif any(word in query_lower for word in ['facility', 'facilities', 'infrastructure']):
        response_parts.append(f"**🏛️ Facilities at {university['short_name']}:**\n")
        for facility in university['facilities']:
            response_parts.append(f"• {facility}\n")
    
    elif any(word in query_lower for word in ['club', 'clubs', 'activity', 'activities']):
        response_parts.append(f"**🎭 Clubs and Activities at {university['short_name']}:**\n")
        for club in university['clubs']:
            response_parts.append(f"• {club}\n")
    
    else:
        # General information
        response_parts.append(f"**🎓 About {university['university_name']}:**\n\n")
        response_parts.append(f"**Type:** {university['type']}\n")
        response_parts.append(f"**Location:** {university['city']}, Maharashtra\n")
        response_parts.append(f"**Contact:** {university['contact_number']}\n")
        response_parts.append(f"**Website:** {university['website']}\n\n")
        response_parts.append(f"**Quick Info:**\n")
        response_parts.append(f"• Courses: {len(university['courses_offered'])} programs offered\n")
        response_parts.append(f"• Placement Rate: {university['placement_information']['placement_rate']}\n")
        response_parts.append(f"• Annual Fee: {university['fees']['annual_tuition']}\n")
    
    if response_parts:
        return "".join(response_parts)
    else:
        return f"I found information about {university['short_name']}, but I need more specific details about what you're looking for. You can ask about fees, placements, courses, admission, hostel, or facilities."

# Header with theme toggle
header_col1, header_col2 = st.columns([6, 1])

with header_col1:
    st.markdown("""
    <div class="main-header">
        <h1>🎓 Solapur Multi-University Assistant</h1>
        <p>Get information about colleges in Solapur</p>
    </div>
    """, unsafe_allow_html=True)

with header_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
    theme_label = "Dark" if not st.session_state.dark_mode else "Light"
    
    if st.button(f"{theme_icon} {theme_label}", key="theme_toggle", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 🏛️ Select University")
    
    # University selection
    for uni in st.session_state.universities_data:
        is_selected = st.session_state.selected_university == uni['id']
        if st.button(
            f"{'✅ ' if is_selected else ''}{uni['short_name']}",
            key=f"uni_{uni['id']}",
            use_container_width=True
        ):
            st.session_state.selected_university = uni['id']
            st.rerun()
    
    if st.button("🔄 Clear Selection", use_container_width=True, type="secondary"):
        st.session_state.selected_university = None
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show selected university info
    if st.session_state.selected_university:
        selected_uni = next((u for u in st.session_state.universities_data if u['id'] == st.session_state.selected_university), None)
        if selected_uni:
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.markdown(f"### 📍 {selected_uni['short_name']}")
            st.info(f"""
            **Type:** {selected_uni['type']}
            
            **Location:** {selected_uni['city']}
            
            **Contact:** {selected_uni['contact_number']}
            """)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 📊 Quick Stats")
    st.metric("Total Universities", len(st.session_state.universities_data))
    st.metric("City", "Solapur")
    st.markdown('</div>', unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if not st.session_state.messages:
        st.markdown("""
        <div style='position: relative; height: 600px; border-radius: 15px; overflow: hidden;'>
            <img src='https://images.unsplash.com/photo-1562774053-701939374585?w=1200' 
                 style='width: 100%; height: 100%; object-fit: cover; filter: brightness(0.7);'/>
            <div style='position: absolute; top: 0; left: 0; right: 0; bottom: 0; 
                        background: linear-gradient(135deg, rgba(102,126,234,0.85) 0%, rgba(118,75,162,0.85) 100%);
                        display: flex; flex-direction: column; justify-content: center; align-items: center;
                        color: white; padding: 2rem;'>
                <div style='font-size: 5rem; margin-bottom: 1rem; animation: bounce 2s infinite;'>🎓</div>
                <h2 style='font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                    Multi-University Assistant
                </h2>
                <p style='font-size: 1.3rem; margin-bottom: 2rem; text-align: center; max-width: 600px;'>
                    Ask about any college in Solapur!
                </p>
                <div style='display: flex; flex-wrap: wrap; justify-content: center; gap: 1rem; margin-top: 1rem;'>
                    <span style='background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); 
                                 padding: 0.8rem 1.5rem; border-radius: 25px; border: 2px solid white;
                                 font-weight: 600; font-size: 1.1rem;'>🏛️ 5 Universities</span>
                    <span style='background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); 
                                 padding: 0.8rem 1.5rem; border-radius: 25px; border: 2px solid white;
                                 font-weight: 600; font-size: 1.1rem;'>📍 Solapur City</span>
                    <span style='background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); 
                                 padding: 0.8rem 1.5rem; border-radius: 25px; border: 2px solid white;
                                 font-weight: 600; font-size: 1.1rem;'>💬 Smart Search</span>
                </div>
                <p style='margin-top: 3rem; font-size: 1.1rem; animation: pulse 2s infinite;'>
                    👇 Select a university or start asking!
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    for idx, msg in enumerate(st.session_state.messages):
        timestamp = msg.get("timestamp", "")
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                {msg["content"]}
                <div class="timestamp">{timestamp}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bot-message">
                {msg["content"]}
                <div class="timestamp">{timestamp}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Feedback buttons
            feedback_key = f"feedback_{idx}"
            fb_col1, fb_col2, fb_col3 = st.columns([1, 1, 8])
            
            with fb_col1:
                if st.button("👍", key=f"helpful_{idx}", use_container_width=True):
                    user_msg = st.session_state.messages[idx-1]["content"] if idx > 0 else ""
                    save_feedback(idx, "helpful", user_msg, msg["content"], st.session_state.selected_university)
                    st.session_state.feedback_given[feedback_key] = "helpful"
                    st.rerun()
            
            with fb_col2:
                if st.button("👎", key=f"not_helpful_{idx}", use_container_width=True):
                    user_msg = st.session_state.messages[idx-1]["content"] if idx > 0 else ""
                    save_feedback(idx, "not_helpful", user_msg, msg["content"], st.session_state.selected_university)
                    st.session_state.feedback_given[feedback_key] = "not_helpful"
                    st.rerun()
            
            with fb_col3:
                if feedback_key in st.session_state.feedback_given:
                    st.markdown('<span style="color: var(--primary-color); font-size: 0.8rem;">✨ Thank you!</span>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick suggestions
    st.markdown("### 💡 Quick Questions")
    suggestions = [
        "What are the fees at WIT?",
        "Tell me about placements at KBP",
        "Which courses does DYP offer?",
        "Compare all engineering colleges"
    ]
    
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
                st.session_state.quick_query = suggestion

with col2:
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 🏛️ Universities")
    for uni in st.session_state.universities_data:
        st.markdown(f"**{uni['short_name']}**")
        st.caption(uni['type'])
        st.markdown("---")
    st.markdown('</div>', unsafe_allow_html=True)

# Chat input
if "quick_query" in st.session_state:
    prompt = st.session_state.quick_query
    del st.session_state.quick_query
else:
    prompt = st.chat_input("💬 Ask about any college in Solapur...")

if prompt:
    timestamp = datetime.now().strftime("%I:%M %p")
    
    # Add user message
    user_msg = {"role": "user", "content": prompt, "timestamp": timestamp}
    st.session_state.messages.append(user_msg)
    
    # Detect university
    detected_uni = detect_university(prompt)
    
    # If no university detected and none selected, ask user to select
    if not detected_uni and not st.session_state.selected_university:
        response = """**🏛️ Please select a university first!**

I can help you with information about these colleges in Solapur:

• **WIT** - Walchand Institute of Technology
• **Walchand College** - Arts and Science
• **KBP Engineering** - KBP College of Engineering
• **DYP Engineering** - D.Y. Patil Institute
• **Solapur University** - Main University

Please select one from the sidebar, or mention it in your question!"""
    else:
        # Use detected or selected university
        university_id = detected_uni if detected_uni else st.session_state.selected_university
        
        # Search for information
        with st.spinner(""):
            time.sleep(0.5)
            response = search_university_info(prompt, university_id)
    
    # Add bot message
    bot_msg = {"role": "assistant", "content": response, "timestamp": timestamp}
    st.session_state.messages.append(bot_msg)
    
    st.rerun()

# Footer
st.markdown("""
<div class="footer">
    <p>🎓 Solapur Multi-University Assistant | © 2024</p>
    <p>Covering 5 major institutions in Solapur</p>
</div>
""", unsafe_allow_html=True)
