import streamlit as st
import time
from datetime import datetime

# Page config
st.set_page_config(
    page_title="WIT Campus Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #4A90E2;
        --secondary-color: #7B68EE;
        --bg-color: #F8F9FA;
        --user-msg-bg: #4A90E2;
        --bot-msg-bg: #E9ECEF;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
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
    
    /* Chat container */
    .chat-container {
        background: transparent;
        border-radius: 15px;
        padding: 1.5rem;
        height: 600px;
        overflow-y: auto;
        margin-bottom: 1rem;
    }
    
    /* Message bubbles */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0 1rem auto;
        max-width: 70%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        animation: slideInRight 0.3s ease;
    }
    
    .bot-message {
        background: #F1F3F5;
        color: #212529;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem auto 1rem 0;
        max-width: 75%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
        animation: slideInLeft 0.3s ease;
    }
    
    .timestamp {
        font-size: 0.75rem;
        color: #868e96;
        margin-top: 0.3rem;
    }
    
    /* Quick suggestions */
    .suggestion-btn {
        background: white;
        border: 2px solid #667eea;
        color: #667eea;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        margin: 0.3rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
        font-weight: 500;
    }
    
    .suggestion-btn:hover {
        background: #667eea;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(102,126,234,0.3);
    }
    
    /* Sidebar styling */
    .sidebar-section {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .sidebar-section h3 {
        color: #667eea;
        margin-bottom: 1rem;
        font-size: 1.2rem;
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
    
    /* Typing indicator */
    .typing-indicator {
        display: inline-block;
        padding: 1rem;
    }
    
    .typing-indicator span {
        height: 10px;
        width: 10px;
        background: #667eea;
        border-radius: 50%;
        display: inline-block;
        margin: 0 2px;
        animation: typing 1.4s infinite;
    }
    
    .typing-indicator span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-indicator span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes typing {
        0%, 60%, 100% {
            transform: translateY(0);
        }
        30% {
            transform: translateY(-10px);
        }
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1rem;
        color: #868e96;
        font-size: 0.9rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "handbook" not in st.session_state:
    try:
        with open("data/handbook.txt", "r", encoding="utf-8") as f:
            st.session_state.handbook = f.read()
    except:
        st.session_state.handbook = ""

# Header
st.markdown("""
<div class="main-header">
    <h1>🎓 WIT Campus Assistant</h1>
    <p>Walchand Institute of Technology, Solapur</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
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
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 🎭 Clubs & Activities")
    st.markdown("""
    - Computer Society (CSI)
    - IEEE Student Branch
    - Robotics Club
    - Cultural Club (Kalarang)
    - Sports Committee
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 📞 Emergency Contacts")
    st.markdown("""
    - **Security**: 0217-2320599
    - **Ambulance**: 108
    - **College Emergency**: 9876543210
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Chat display
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
                    Welcome to WIT Campus Assistant
                </h2>
                <p style='font-size: 1.3rem; margin-bottom: 2rem; text-align: center; max-width: 600px;'>
                    Your 24/7 AI-powered guide to campus life, academics, and everything WIT!
                </p>
                <div style='display: flex; flex-wrap: wrap; justify-content: center; gap: 1rem; margin-top: 1rem;'>
                    <span style='background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); 
                                 padding: 0.8rem 1.5rem; border-radius: 25px; border: 2px solid white;
                                 font-weight: 600; font-size: 1.1rem;'>📚 Academics</span>
                    <span style='background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); 
                                 padding: 0.8rem 1.5rem; border-radius: 25px; border: 2px solid white;
                                 font-weight: 600; font-size: 1.1rem;'>💰 Fees</span>
                    <span style='background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); 
                                 padding: 0.8rem 1.5rem; border-radius: 25px; border: 2px solid white;
                                 font-weight: 600; font-size: 1.1rem;'>🎯 Placements</span>
                    <span style='background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); 
                                 padding: 0.8rem 1.5rem; border-radius: 25px; border: 2px solid white;
                                 font-weight: 600; font-size: 1.1rem;'>🏠 Hostel</span>
                    <span style='background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); 
                                 padding: 0.8rem 1.5rem; border-radius: 25px; border: 2px solid white;
                                 font-weight: 600; font-size: 1.1rem;'>🎭 Clubs</span>
                </div>
                <p style='margin-top: 3rem; font-size: 1.1rem; animation: pulse 2s infinite;'>
                    👇 Start chatting below or click a quick suggestion
                </p>
            </div>
        </div>
        <style>
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-20px); }
            }
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.6; }
            }
        </style>
        """, unsafe_allow_html=True)
    
    for msg in st.session_state.messages:
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
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick suggestions
    st.markdown("### 💡 Quick Suggestions")
    suggestions = [
        "What is the attendance policy?",
        "How do I join clubs?",
        "Where is the library?",
        "Tell me about exam pattern"
    ]
    
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
                st.session_state.quick_query = suggestion

with col2:
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
    <div style='padding: 0.5rem; margin: 0.5rem 0; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                border-radius: 10px; color: white;'>
        <strong>⭐ NAAC A+ Grade</strong><br/>
        <small>Accredited 2023</small>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 🎓 Departments")
    departments = [
        ("💻", "Computer Science"),
        ("📱", "Information Technology"),
        ("📡", "Electronics & Telecom"),
        ("⚙️", "Mechanical Engineering"),
        ("🏗️", "Civil Engineering"),
        ("⚡", "Electrical Engineering")
    ]
    for icon, dept in departments:
        st.markdown(f"""
        <div style='padding: 0.7rem; margin: 0.4rem 0; background: white; 
                    border-left: 4px solid #667eea; border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <span style='font-size: 1.3rem; margin-right: 0.5rem;'>{icon}</span>
            <span style='font-weight: 600; color: #212529; font-size: 1rem;'>{dept}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 📅 Upcoming Events")
    st.markdown("""
    <div style='padding: 0.8rem; margin: 0.5rem 0; background: #fff3cd; 
                border-radius: 8px; border-left: 4px solid #ffc107;'>
        <strong>🎪 Tech Fest 2024</strong><br/>
        <small>📅 March 15-17</small>
    </div>
    <div style='padding: 0.8rem; margin: 0.5rem 0; background: #d1ecf1; 
                border-radius: 8px; border-left: 4px solid #17a2b8;'>
        <strong>🎭 Cultural Night</strong><br/>
        <small>📅 March 20</small>
    </div>
    <div style='padding: 0.8rem; margin: 0.5rem 0; background: #d4edda; 
                border-radius: 8px; border-left: 4px solid #28a745;'>
        <strong>💼 Job Fair</strong><br/>
        <small>📅 March 25</small>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Search functions (same as before)
def search_handbook(query):
    """Fast and accurate search"""
    query_lower = query.lower()
    full_text = st.session_state.handbook
    
    search_patterns = {
        'club': ['7. CLUBS AND SOCIETIES', 'registration process:'],
        'fee': ['5. FEE STRUCTURE', 'annual tuition fee:'],
        'attendance': ['3. ATTENDANCE POLICY', '75% attendance'],
        'placement': ['6. PLACEMENT CELL', 'average package:'],
        'hostel': ['hostel facilities:', 'hostel fee:'],
        'library': ['library:', 'location: central building'],
        'exam': ['4. EXAMINATION SYSTEM', 'internal assessment'],
        'grade': ['grading system:', 'sgpa'],
        'cbcs': ['2. ACADEMIC REGULATIONS', 'cbcs'],
    }
    
    relevant_patterns = []
    for topic, patterns in search_patterns.items():
        if topic in query_lower:
            relevant_patterns.extend(patterns)
    
    if not relevant_patterns:
        relevant_patterns = [word for word in query_lower.split() if len(word) > 3]
    
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

def format_answer(query, sections):
    """Format answer"""
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

# Chat input
if "quick_query" in st.session_state:
    prompt = st.session_state.quick_query
    del st.session_state.quick_query
else:
    prompt = st.chat_input("💬 Ask me anything about campus...")

if prompt:
    timestamp = datetime.now().strftime("%I:%M %p")
    
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": timestamp
    })
    
    # Show typing indicator
    with st.spinner(""):
        time.sleep(0.5)  # Simulate thinking
        sections = search_handbook(prompt)
        response = format_answer(prompt, sections)
    
    # Add bot message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "timestamp": timestamp
    })
    
    st.rerun()

# Footer
st.markdown("""
<div class="footer">
    <p>🤖 Powered by AI Campus Assistant | © 2024 Walchand Institute of Technology</p>
    <p>Made with ❤️ for WIT Students</p>
</div>
""", unsafe_allow_html=True)

# Handbook status
if st.session_state.handbook:
    st.sidebar.success(f"✅ Database: {len(st.session_state.handbook):,} chars loaded")
