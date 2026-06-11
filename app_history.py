import streamlit as st
import time
import json
import os
from datetime import datetime, date
import uuid

# Page config
st.set_page_config(
    page_title="WIT Campus Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state FIRST (before using it)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_memory" not in st.session_state:
    st.session_state.conversation_memory = []
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = {}
if "handbook" not in st.session_state:
    try:
        with open("data/handbook.txt", "r", encoding="utf-8") as f:
            st.session_state.handbook = f.read()
    except:
        st.session_state.handbook = ""

# Dynamic CSS based on theme
def get_theme_css(dark_mode):
    if dark_mode:
        return """
<style>
    /* Dark Mode Colors */
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
    
    /* Dark mode body */
    .stApp {
        background-color: var(--bg-color);
        color: var(--text-color);
        transition: all 0.3s ease;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Sidebar dark mode */
    [data-testid="stSidebar"] {
        background-color: var(--card-bg);
        border-right: 1px solid var(--border-color);
    }
    
    /* Input fields dark mode */
    .stTextInput input, .stChatInput input {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
        border-color: var(--border-color) !important;
    }
    
    /* Buttons dark mode */
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
    /* Light Mode Colors */
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
    
    /* Light mode body */
    .stApp {
        background-color: var(--bg-color);
        color: var(--text-color);
        transition: all 0.3s ease;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Sidebar light mode */
    [data-testid="stSidebar"] {
        background-color: var(--card-bg);
        border-right: 1px solid var(--border-color);
    }
"""

# Apply theme CSS
st.markdown(get_theme_css(st.session_state.dark_mode), unsafe_allow_html=True)

# Common CSS (works for both themes)
st.markdown("""
<style>
    
    /* Header styling */
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
    
    /* Theme toggle button */
    .theme-toggle {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 50px;
        padding: 0.5rem 1.2rem;
        cursor: pointer;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        color: white;
        font-weight: 600;
    }
    
    .theme-toggle:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: scale(1.05);
    }
    
    /* Chat container */
    .chat-container {
        background: transparent;
        border-radius: 15px;
        padding: 1.5rem;
        height: 600px;
        overflow-y: auto;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    /* Message bubbles */
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
    
    /* History cards */
    .history-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px var(--shadow);
    }
    
    .history-card:hover {
        border-color: var(--primary-color);
        box-shadow: 0 4px 8px var(--shadow);
        transform: translateY(-2px);
        background: var(--hover-bg);
    }
    
    .history-card.active {
        border-color: var(--primary-color);
        background: var(--hover-bg);
    }
    
    .history-title {
        font-weight: 600;
        color: var(--text-color);
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
        transition: all 0.3s ease;
    }
    
    .history-date {
        font-size: 0.75rem;
        color: var(--text-secondary);
        transition: all 0.3s ease;
    }
    
    .history-preview {
        font-size: 0.8rem;
        color: var(--text-secondary);
        margin-top: 0.3rem;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        transition: all 0.3s ease;
    }
    
    /* Sidebar styling */
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
    
    /* Animations */
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1rem;
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-top: 2rem;
        transition: all 0.3s ease;
    }
    
    /* Feedback buttons */
    .feedback-container {
        display: flex;
        gap: 0.5rem;
        align-items: center;
        margin-top: 0.5rem;
        padding-top: 0.5rem;
        border-top: 1px solid var(--border-color);
    }
    
    .feedback-btn {
        background: transparent;
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 0.3rem 0.8rem;
        cursor: pointer;
        font-size: 0.85rem;
        transition: all 0.2s ease;
        color: var(--text-secondary);
    }
    
    .feedback-btn:hover {
        background: var(--hover-bg);
        border-color: var(--primary-color);
        transform: scale(1.05);
    }
    
    .feedback-btn.selected {
        background: var(--primary-color);
        color: white;
        border-color: var(--primary-color);
    }
    
    .feedback-thanks {
        color: var(--primary-color);
        font-size: 0.8rem;
        font-style: italic;
        margin-left: 0.5rem;
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Info boxes */
    .stAlert {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
        border-color: var(--border-color) !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: var(--text-color) !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
    }
</style>
""", unsafe_allow_html=True)

# Chat History Management
HISTORY_FILE = "chat_history.json"
FEEDBACK_FILE = "feedback.csv"

def save_feedback(message_index, feedback_type, question, answer):
    """Save feedback to CSV file"""
    import csv
    from datetime import datetime
    
    # Create CSV if it doesn't exist
    file_exists = os.path.exists(FEEDBACK_FILE)
    
    with open(FEEDBACK_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header if new file
        if not file_exists:
            writer.writerow(['Timestamp', 'Message_Index', 'Feedback', 'Question', 'Answer'])
        
        # Write feedback
        writer.writerow([
            datetime.now().isoformat(),
            message_index,
            feedback_type,
            question[:100],  # Limit length
            answer[:200]     # Limit length
        ])

def load_chat_history():
    """Load chat history from JSON file"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_chat_history(history):
    """Save chat history to JSON file"""
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Error saving chat history: {e}")

def save_current_conversation():
    """Save current conversation to history"""
    if len(st.session_state.messages) > 0:
        history = load_chat_history()
        
        # Create conversation ID if not exists
        if "conversation_id" not in st.session_state:
            st.session_state.conversation_id = str(uuid.uuid4())
        
        # Get first user message as title
        first_message = next((msg for msg in st.session_state.messages if msg["role"] == "user"), None)
        title = first_message["content"][:50] + "..." if first_message and len(first_message["content"]) > 50 else first_message["content"] if first_message else "New Chat"
        
        # Save conversation
        conversation_data = {
            "id": st.session_state.conversation_id,
            "title": title,
            "date": datetime.now().isoformat(),
            "messages": st.session_state.messages
        }
        
        history[st.session_state.conversation_id] = conversation_data
        save_chat_history(history)

def load_conversation(conversation_id):
    """Load a specific conversation"""
    history = load_chat_history()
    if conversation_id in history:
        conversation = history[conversation_id]
        st.session_state.messages = conversation["messages"]
        st.session_state.conversation_id = conversation_id
        st.rerun()

def delete_chat_history():
    """Delete all chat history"""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    st.session_state.messages = []
    st.session_state.conversation_memory = []
    if "conversation_id" in st.session_state:
        del st.session_state.conversation_id

def group_conversations_by_date(history):
    """Group conversations by date"""
    grouped = {}
    for conv_id, conv_data in history.items():
        conv_date = datetime.fromisoformat(conv_data["date"]).date()
        date_str = conv_date.strftime("%Y-%m-%d")
        
        if date_str not in grouped:
            grouped[date_str] = []
        grouped[date_str].append((conv_id, conv_data))
    
    # Sort by date (newest first)
    return dict(sorted(grouped.items(), key=lambda x: x[0], reverse=True))

# Header with theme toggle
header_col1, header_col2 = st.columns([6, 1])

with header_col1:
    st.markdown("""
    <div class="main-header">
        <h1>🎓 WIT Campus Assistant</h1>
        <p>Walchand Institute of Technology, Solapur - With Chat History</p>
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
    st.markdown("### 📚 Chat History")
    
    # Load and display chat history
    history = load_chat_history()
    
    if history:
        grouped_history = group_conversations_by_date(history)
        
        # Scrollable container for history
        with st.container():
            for date_str, conversations in grouped_history.items():
                # Date header
                conv_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                if conv_date == date.today():
                    date_display = "Today"
                elif conv_date == date.today().replace(day=date.today().day-1):
                    date_display = "Yesterday"
                else:
                    date_display = conv_date.strftime("%B %d, %Y")
                
                st.markdown(f"**{date_display}**")
                
                # Conversations for this date
                for conv_id, conv_data in conversations:
                    # Create clickable history card
                    is_active = st.session_state.get("conversation_id") == conv_id
                    card_class = "history-card active" if is_active else "history-card"
                    
                    if st.button(
                        f"💬 {conv_data['title'][:30]}...",
                        key=f"hist_{conv_id}",
                        help=f"Click to load conversation from {datetime.fromisoformat(conv_data['date']).strftime('%I:%M %p')}",
                        use_container_width=True
                    ):
                        load_conversation(conv_id)
                
                st.markdown("---")
        
        # Clear history button with confirmation
        if st.button("🗑️ Clear All History", use_container_width=True, type="secondary"):
            if st.session_state.get("confirm_delete", False):
                delete_chat_history()
                st.session_state.confirm_delete = False
                st.success("Chat history cleared!")
                st.rerun()
            else:
                st.session_state.confirm_delete = True
                st.warning("Click again to confirm deletion")
    else:
        st.info("No chat history yet. Start a conversation!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 🏛️ About Campus")
    st.info("""
    **Walchand Institute of Technology**
    
    📍 Ashok Chowk, Solapur - 413006
    
    📞 0217-2320567
    
    📧 principal@witsolapur.org
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 🧠 Memory Status")
    memory_count = len(st.session_state.conversation_memory)
    if memory_count > 0:
        st.success(f"💭 Remembering {memory_count} conversation turns")
    else:
        st.info("🆕 Start a conversation to enable memory")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 📅 Quick Links")
    if st.button("📚 Academic Regulations", use_container_width=True):
        st.session_state.quick_query = "Tell me about CBCS system"
    if st.button("💰 Fee Structure", use_container_width=True):
        st.session_state.quick_query = "What is the fee structure?"
    if st.button("🎯 Placements", use_container_width=True):
        st.session_state.quick_query = "Tell me about placements"
    if st.button("🏠 Hostel Info", use_container_width=True):
        st.session_state.quick_query = "What are hostel facilities?"
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🆕 New Chat", use_container_width=True, type="primary"):
        # Save current conversation before starting new one
        if len(st.session_state.messages) > 0:
            save_current_conversation()
        
        # Start new conversation
        st.session_state.messages = []
        st.session_state.conversation_memory = []
        if "conversation_id" in st.session_state:
            del st.session_state.conversation_id
        st.rerun()

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Chat display
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if not st.session_state.messages:
        # Interactive Welcome Dashboard
        st.markdown("""
        <div style='text-align: center; padding: 2rem 0 1rem 0;'>
            <h1 style='font-size: 3rem; margin-bottom: 0.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;'>
                👋 Welcome to WIT Campus Assistant
            </h1>
            <p style='font-size: 1.2rem; color: var(--text-secondary); margin-bottom: 2rem;'>
                Ask me anything about Walchand Institute of Technology
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Popular Questions Section
        st.markdown("### 🔥 Popular Questions")
        
        popular_questions = [
            ("📍 Where is the placement cell located?", "Where is placement cell?"),
            ("💰 What is the fee structure?", "What is the fee structure?"),
            ("🏠 Tell me about hostel facilities", "Tell me about hostel facilities"),
            ("📚 What is the CBCS system?", "Tell me about CBCS system"),
            ("🎯 What are the placement statistics?", "What are placement statistics?"),
            ("🎭 How to join clubs?", "How to join clubs?"),
        ]
        
        # Display in 2 columns
        pop_col1, pop_col2 = st.columns(2)
        
        for i, (display_text, query) in enumerate(popular_questions):
            col = pop_col1 if i % 2 == 0 else pop_col2
            with col:
                if st.button(display_text, key=f"pop_q_{i}", use_container_width=True):
                    st.session_state.quick_query = query
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Features Overview
        st.markdown("### ✨ Features")
        
        feat_col1, feat_col2, feat_col3 = st.columns(3)
        
        with feat_col1:
            st.markdown("""
            <div style='text-align: center; padding: 1.5rem; background: var(--card-bg); 
                        border-radius: 15px; border: 2px solid var(--border-color); height: 180px;'>
                <div style='font-size: 3rem; margin-bottom: 0.5rem;'>💾</div>
                <h4 style='color: var(--primary-color); margin-bottom: 0.5rem;'>Auto-Save</h4>
                <p style='font-size: 0.9rem; color: var(--text-secondary);'>
                    All conversations automatically saved
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with feat_col2:
            st.markdown("""
            <div style='text-align: center; padding: 1.5rem; background: var(--card-bg); 
                        border-radius: 15px; border: 2px solid var(--border-color); height: 180px;'>
                <div style='font-size: 3rem; margin-bottom: 0.5rem;'>🧠</div>
                <h4 style='color: var(--primary-color); margin-bottom: 0.5rem;'>Smart Memory</h4>
                <p style='font-size: 0.9rem; color: var(--text-secondary);'>
                    Remembers context for follow-up questions
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with feat_col3:
            st.markdown("""
            <div style='text-align: center; padding: 1.5rem; background: var(--card-bg); 
                        border-radius: 15px; border: 2px solid var(--border-color); height: 180px;'>
                <div style='font-size: 3rem; margin-bottom: 0.5rem;'>👍</div>
                <h4 style='color: var(--primary-color); margin-bottom: 0.5rem;'>Feedback</h4>
                <p style='font-size: 0.9rem; color: var(--text-secondary);'>
                    Rate responses to help us improve
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Quick Stats
        st.markdown("### 📊 Quick Stats")
        
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.markdown("""
            <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        border-radius: 10px; color: white;'>
                <div style='font-size: 2rem; font-weight: 700;'>2000+</div>
                <div style='font-size: 0.8rem;'>Students</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stat_col2:
            st.markdown("""
            <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        border-radius: 10px; color: white;'>
                <div style='font-size: 2rem; font-weight: 700;'>150+</div>
                <div style='font-size: 0.8rem;'>Faculty</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stat_col3:
            st.markdown("""
            <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        border-radius: 10px; color: white;'>
                <div style='font-size: 2rem; font-weight: 700;'>85%</div>
                <div style='font-size: 0.8rem;'>Placement</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stat_col4:
            st.markdown("""
            <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                        border-radius: 10px; color: white;'>
                <div style='font-size: 2rem; font-weight: 700;'>6</div>
                <div style='font-size: 0.8rem;'>Departments</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Call to Action
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%); 
                    border-radius: 15px; border: 2px dashed var(--primary-color);'>
            <div style='font-size: 2rem; margin-bottom: 1rem;'>💬</div>
            <h3 style='color: var(--primary-color); margin-bottom: 0.5rem;'>Ready to get started?</h3>
            <p style='color: var(--text-secondary); font-size: 1.1rem;'>
                Type your question below or click any popular question above!
            </p>
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
            # Bot message with feedback
            st.markdown(f"""
            <div class="bot-message">
                {msg["content"]}
                <div class="timestamp">{timestamp}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Feedback buttons for bot messages
            feedback_key = f"feedback_{idx}"
            
            # Create columns for feedback buttons
            fb_col1, fb_col2, fb_col3 = st.columns([1, 1, 8])
            
            with fb_col1:
                if st.button("👍 Helpful", key=f"helpful_{idx}", use_container_width=True):
                    # Get the previous user message
                    user_msg = st.session_state.messages[idx-1]["content"] if idx > 0 else ""
                    save_feedback(idx, "helpful", user_msg, msg["content"])
                    st.session_state.feedback_given[feedback_key] = "helpful"
                    st.rerun()
            
            with fb_col2:
                if st.button("👎 Not Helpful", key=f"not_helpful_{idx}", use_container_width=True):
                    # Get the previous user message
                    user_msg = st.session_state.messages[idx-1]["content"] if idx > 0 else ""
                    save_feedback(idx, "not_helpful", user_msg, msg["content"])
                    st.session_state.feedback_given[feedback_key] = "not_helpful"
                    st.rerun()
            
            with fb_col3:
                # Show thank you message if feedback given
                if feedback_key in st.session_state.feedback_given:
                    feedback_type = st.session_state.feedback_given[feedback_key]
                    if feedback_type == "helpful":
                        st.markdown('<span class="feedback-thanks">✨ Thank you for your feedback!</span>', unsafe_allow_html=True)
                    else:
                        st.markdown('<span class="feedback-thanks">📝 Thank you! We\'ll improve.</span>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick suggestions
    st.markdown("### 💡 Quick Suggestions")
    suggestions = [
        "Where is the placement cell?",
        "What are its timings?",
        "Tell me about hostel fees",
        "What facilities does it have?"
    ]
    
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
                st.session_state.quick_query = suggestion

with col2:
    # College Photo Section
    st.markdown('<div class="sidebar-section" style="padding: 0; overflow: hidden;">', unsafe_allow_html=True)
    
    # Try to load local image, fallback to placeholder
    import base64
    from pathlib import Path
    
    college_image_path = Path("data/wit_college.jpg")
    
    if college_image_path.exists():
        # Use local image
        with open(college_image_path, "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode()
            img_src = f"data:image/jpeg;base64,{img_data}"
    else:
        # Fallback to placeholder
        img_src = "https://images.unsplash.com/photo-1562774053-701939374585?w=800"
    
    st.markdown(f"""
    <div style='position: relative; width: 100%; height: 250px; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px var(--shadow);'>
        <img src='{img_src}' 
             style='width: 100%; height: 100%; object-fit: cover;'/>
        <div style='position: absolute; bottom: 0; left: 0; right: 0; 
                    background: linear-gradient(to top, rgba(0,0,0,0.8) 0%, transparent 100%);
                    padding: 1rem; color: white;'>
            <h3 style='margin: 0; font-size: 1.2rem; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);'>🎓 WIT Campus</h3>
            <p style='margin: 0.3rem 0 0 0; font-size: 0.9rem; opacity: 0.95; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);'>Walchand Institute of Technology</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Interactive Quick Actions Panel
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### ⚡ Quick Actions")
    
    # Action buttons in a grid
    action_col1, action_col2 = st.columns(2)
    
    with action_col1:
        if st.button("📚 Academics", key="quick_academics", use_container_width=True):
            st.session_state.quick_query = "Tell me about CBCS system and academic regulations"
        
        if st.button("💰 Fees", key="quick_fees", use_container_width=True):
            st.session_state.quick_query = "What is the complete fee structure?"
        
        if st.button("🏠 Hostel", key="quick_hostel", use_container_width=True):
            st.session_state.quick_query = "Tell me about hostel facilities and fees"
    
    with action_col2:
        if st.button("🎯 Placements", key="quick_placements", use_container_width=True):
            st.session_state.quick_query = "Tell me about placement statistics and companies"
        
        if st.button("🎭 Clubs", key="quick_clubs", use_container_width=True):
            st.session_state.quick_query = "What clubs are available and how to join?"
        
        if st.button("📖 Library", key="quick_library", use_container_width=True):
            st.session_state.quick_query = "Where is the library and what are its timings?"
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Live Stats Counter
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 📊 Live Stats")
    
    # Calculate some live stats
    total_messages = len(st.session_state.messages)
    total_conversations = len(st.session_state.conversation_memory)
    
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 10px; color: white;'>
            <div style='font-size: 2rem; font-weight: 700;'>{total_messages}</div>
            <div style='font-size: 0.8rem; opacity: 0.9;'>Messages</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    border-radius: 10px; color: white;'>
            <div style='font-size: 2rem; font-weight: 700;'>{total_conversations}</div>
            <div style='font-size: 0.8rem; opacity: 0.9;'>In Memory</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Campus stats and info (same as before)
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 📊 Campus Stats")
    st.metric("Total Students", "2000+", delta="↑ 150 this year")
    st.metric("Faculty Members", "150+", delta="Experienced")
    st.metric("Placement Rate", "85%", delta="↑ 5% from last year")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 🏆 Recent Achievements")
    st.markdown("""
    <div style='padding: 0.5rem; margin: 0.5rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 10px; color: white;'>
        <strong>🥇 Best Engineering College</strong><br/>
        <small>Maharashtra Region 2024</small>
    </div>
    <div style='padding: 0.5rem; margin: 0.5rem 0; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                border-radius: 10px; color: white;'>
        <strong>🎯 100% Placement</strong><br/>
        <small>CSE & IT Departments</small>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 🏛️ Departments")
    departments = [
        "💻 Computer Science",
        "⚡ Electronics & Telecom",
        "⚙️ Mechanical Engineering",
        "🏗️ Civil Engineering",
        "🔌 Electrical Engineering",
        "🧪 Information Technology"
    ]
    for dept in departments:
        st.markdown(f"• {dept}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 📅 Upcoming Events")
    st.markdown("""
    <div style='padding: 0.5rem; margin: 0.5rem 0; background: var(--card-bg); 
                border-left: 3px solid #667eea; border-radius: 5px;'>
        <strong>🎓 Tech Fest 2024</strong><br/>
        <small>March 15-17, 2024</small>
    </div>
    <div style='padding: 0.5rem; margin: 0.5rem 0; background: var(--card-bg); 
                border-left: 3px solid #f093fb; border-radius: 5px;'>
        <strong>🎭 Cultural Night</strong><br/>
        <small>March 20, 2024</small>
    </div>
    <div style='padding: 0.5rem; margin: 0.5rem 0; background: var(--card-bg); 
                border-left: 3px solid #764ba2; border-radius: 5px;'>
        <strong>💼 Placement Drive</strong><br/>
        <small>March 25-30, 2024</small>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Search functions (same as memory version)
def search_handbook_with_memory(query, conversation_history):
    """Enhanced search that considers conversation context"""
    query_lower = query.lower()
    
    # Resolve pronouns using conversation history
    resolved_query = resolve_pronouns(query, conversation_history)
    
    # Use resolved query for search
    full_text = st.session_state.handbook
    
    search_patterns = {
        'club': ['7. CLUBS AND SOCIETIES', 'registration process:', 'technical clubs:', 'cultural clubs:'],
        'fee': ['5. FEE STRUCTURE', 'annual tuition fee:', 'payment schedule:'],
        'attendance': ['3. ATTENDANCE POLICY', '75% attendance', 'condonation'],
        'placement': ['6. PLACEMENT CELL', 'average package:', 'training and placement', 'eligibility criteria'],
        'hostel': ['hostel facilities:', 'hostel fee:', 'boys hostel:', 'girls hostel:'],
        'library': ['library:', 'location: central building', 'timing:', 'books:'],
        'exam': ['4. EXAMINATION SYSTEM', 'internal assessment', 'external examination'],
        'grade': ['grading system:', 'sgpa', 'cgpa'],
        'cbcs': ['2. ACADEMIC REGULATIONS', 'cbcs', 'credit structure:'],
        'timing': ['timing:', 'hours:', 'schedule:', 'time:'],
        'location': ['location:', 'building:', 'floor:', 'address:'],
        'contact': ['contact:', 'phone:', 'email:', 'coordinator:'],
    }
    
    # Find relevant patterns
    relevant_patterns = []
    for topic, patterns in search_patterns.items():
        if topic in resolved_query.lower():
            relevant_patterns.extend(patterns)
    
    if not relevant_patterns:
        relevant_patterns = [word for word in resolved_query.split() if len(word) > 3]
    
    # Search sections
    sections = full_text.split('=' * 80)
    best_section = None
    best_score = 0
    
    for section in sections:
        if len(section.strip()) < 100 or 'table of contents' in section.lower()[:300]:
            continue
        
        score = sum(10 for pattern in relevant_patterns if pattern in section.lower())
        
        if score > best_score:
            best_score = score
            best_section = section
    
    return [best_section.strip()] if best_section and best_score >= 10 else []

def resolve_pronouns(query, conversation_history):
    """Resolve pronouns like 'it', 'its', 'there' using conversation context"""
    query_lower = query.lower()
    
    # Common pronouns to resolve
    pronouns = ['it', 'its', 'there', 'that', 'this', 'they', 'them']
    
    if any(pronoun in query_lower for pronoun in pronouns):
        # Look at recent conversation for context
        if len(conversation_history) >= 2:
            last_user_msg = conversation_history[-2].get('content', '').lower()
            last_bot_msg = conversation_history[-1].get('content', '').lower()
            
            # Extract likely subjects from previous messages
            subjects = []
            for keyword in ['placement', 'hostel', 'library', 'club', 'fee', 'exam', 'attendance']:
                if keyword in last_user_msg or keyword in last_bot_msg:
                    subjects.append(keyword)
            
            # Replace pronouns with most likely subject
            if subjects:
                resolved_query = query_lower
                for pronoun in pronouns:
                    if pronoun in resolved_query:
                        resolved_query = resolved_query.replace(pronoun, subjects[0])
                return resolved_query
    
    return query

def format_answer_with_memory(query, sections, conversation_history):
    """Format answer considering conversation context"""
    if not sections:
        return """❌ **Information Not Available**

This information is not in the current campus database.

**Contact:**
• College Office: 0217-2320567
• Email: principal@witsolapur.org"""
    
    section = sections[0]
    lines = [l.strip() for l in section.split('\n') if l.strip()]
    
    content_lines = []
    found_content = False
    
    for line in lines:
        if '=' * 10 in line or len(line) < 3:
            continue
        if line[:2].replace('.', '').replace(' ', '').isdigit() and line.isupper():
            found_content = True
            continue
        if found_content and len(line) > 10:
            content_lines.append(line)
    
    if not content_lines:
        content_lines = [l for l in lines if len(l) > 15 and '=' not in l]
    
    answer = "📖 **Official Information:**\n\n"
    for line in content_lines[:25]:
        answer += line + "\n\n"
    
    return answer

# Chat input with history saving
if "quick_query" in st.session_state:
    prompt = st.session_state.quick_query
    del st.session_state.quick_query
else:
    prompt = st.chat_input("💬 Ask me anything (conversations auto-saved)...")

if prompt:
    timestamp = datetime.now().strftime("%I:%M %p")
    
    # Add user message
    user_msg = {"role": "user", "content": prompt, "timestamp": timestamp}
    st.session_state.messages.append(user_msg)
    
    # Add to conversation memory (limit to last 10 turns)
    st.session_state.conversation_memory.append(user_msg)
    if len(st.session_state.conversation_memory) > 10:
        st.session_state.conversation_memory = st.session_state.conversation_memory[-10:]
    
    # Show typing indicator
    with st.spinner(""):
        time.sleep(0.5)
        sections = search_handbook_with_memory(prompt, st.session_state.conversation_memory)
        response = format_answer_with_memory(prompt, sections, st.session_state.conversation_memory)
    
    # Add bot message
    bot_msg = {"role": "assistant", "content": response, "timestamp": timestamp}
    st.session_state.messages.append(bot_msg)
    st.session_state.conversation_memory.append(bot_msg)
    
    # Limit memory
    if len(st.session_state.conversation_memory) > 10:
        st.session_state.conversation_memory = st.session_state.conversation_memory[-10:]
    
    # Auto-save conversation after each exchange
    save_current_conversation()
    
    st.rerun()

# Footer
st.markdown("""
<div class="footer">
    <p>📚 Powered by AI Campus Assistant with History | © 2024 Walchand Institute of Technology</p>
    <p>Made with ❤️ for WIT Students</p>
</div>
""", unsafe_allow_html=True)

# Status
if st.session_state.handbook:
    st.sidebar.success(f"✅ Database: {len(st.session_state.handbook):,} chars loaded")