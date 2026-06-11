import streamlit as st
import json
from datetime import datetime

# Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="Solapur Colleges Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load handbook content
@st.cache_data
def load_handbook():
    """Load handbook content"""
    try:
        with open("data/solapur_colleges_handbook.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

@st.cache_data
def load_colleges_data():
    """Load and cache college data for fast access"""
    try:
        with open("solapur_colleges_database.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # Flatten colleges for faster search
            all_colleges = []
            for category in data.get('categories', {}).values():
                all_colleges.extend(category['colleges'])
            return data, all_colleges
    except:
        return {}, []

# Load data once
handbook_content = load_handbook()
colleges_data, all_colleges = load_colleges_data()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Modern CSS with animations
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 0.5rem 0 0.5rem auto;
        max-width: 70%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        animation: slideInRight 0.3s ease;
        word-wrap: break-word;
    }
    
    .bot-bubble {
        background: white;
        color: #333;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.5rem auto 0.5rem 0;
        max-width: 75%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        animation: slideInLeft 0.3s ease;
        word-wrap: break-word;
    }
    
    .college-card {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .college-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
    }
    
    .college-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
    }
    
    .college-content {
        padding: 1.5rem;
    }
    
    .college-name {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .college-type {
        color: #6c757d;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    .section-title {
        font-weight: 600;
        color: #333;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .course-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        margin: 0.2rem;
        font-size: 0.85rem;
    }
    
    .website-btn {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.7rem 1.5rem;
        border-radius: 25px;
        text-decoration: none;
        margin-top: 1rem;
        transition: all 0.3s ease;
    }
    
    .website-btn:hover {
        background: #764ba2;
        transform: scale(1.05);
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .timestamp {
        font-size: 0.7rem;
        color: #999;
        margin-top: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

def detect_category(query):
    """Fast category detection using keyword matching"""
    query_lower = query.lower()
    
    keywords = {
        'engineering': ['engineering', 'engineer', 'b.tech', 'btech', 'polytechnic', 'technical'],
        'medical': ['medical', 'mbbs', 'doctor', 'health', 'nursing', 'dental', 'medicine'],
        'commerce': ['commerce', 'b.com', 'bcom', 'management', 'mba', 'bba', 'business'],
        'arts_science': ['arts', 'science', 'b.a', 'b.sc', 'bsc', 'humanities'],
        'universities': ['university', 'universities'],
        'all': ['all', 'list', 'show all', 'complete']
    }
    
    for category, words in keywords.items():
        if any(word in query_lower for word in words):
            return category
    
    return None

def find_college_fast(query):
    """Optimized college search"""
    query_lower = query.lower()
    
    for college in all_colleges:
        if college['name'].lower() == query_lower:
            return college
    
    for college in all_colleges:
        if college['short_name'].lower() == query_lower:
            return college
    
    for college in all_colleges:
        if query_lower in college['name'].lower() or college['name'].lower() in query_lower:
            return college
    
    query_words = set(query_lower.split())
    for college in all_colleges:
        name_words = set(college['name'].lower().split())
        if len(query_words & name_words) >= 2:
            return college
    
    return None

def get_colleges_by_category(category):
    """Fast category-based college retrieval"""
    if category == 'all':
        return all_colleges
    
    category_map = {
        'engineering': 'engineering',
        'medical': 'medical',
        'commerce': 'commerce_management',
        'arts_science': 'arts_science',
        'universities': 'universities'
    }
    
    cat_key = category_map.get(category)
    if cat_key and cat_key in colleges_data.get('categories', {}):
        return colleges_data['categories'][cat_key]['colleges']
    
    return []

def display_college_card(college):
    """Display college as a beautiful card"""
    photo_url = college.get('photo_url', 'https://images.unsplash.com/photo-1562774053-701939374585?w=800')
    history = college.get('history', college.get('description', 'Information not available.'))
    
    card_html = f"""
    <div class="college-card">
        <img src="{photo_url}" class="college-image" alt="{college['name']}">
        <div class="college-content">
            <div class="college-name">{college['name']}</div>
            <div class="college-type">{college['type']} | Est. {college['established']}</div>
            
            <div class="section-title">📖 About</div>
            <p style="line-height: 1.6; color: #555;">{history[:300]}...</p>
            
            <div class="section-title">📚 Courses Offered</div>
            <div>
    """
    
    for course in college['courses'][:6]:
        card_html += f'<span class="course-badge">{course}</span>'
    
    card_html += f"""
            </div>
            
            <div class="section-title">📍 Contact</div>
            <p style="color: #555;">
                📍 {college['location']}<br>
                📞 {college['contact']}<br>
                📧 {college['email']}
            </p>
            
            <a href="{college['website']}" target="_blank" class="website-btn">
                🌐 Visit Website
            </a>
        </div>
    </div>
    """
    
    return card_html

def search_handbook(query):
    """Simple keyword search in handbook"""
    if not handbook_content:
        return None
    
    query_lower = query.lower()
    lines = handbook_content.split('\n')
    
    # Find relevant sections
    relevant_lines = []
    for i, line in enumerate(lines):
        if any(word in line.lower() for word in query_lower.split()):
            # Get context (5 lines before and after)
            start = max(0, i - 5)
            end = min(len(lines), i + 6)
            relevant_lines.extend(lines[start:end])
    
    if relevant_lines:
        # Remove duplicates and join
        result = '\n'.join(dict.fromkeys(relevant_lines))
        # Limit to 500 characters
        if len(result) > 500:
            result = result[:500] + "..."
        return result
    
    return None

def is_detailed_question(query):
    """Check if query is asking for detailed information"""
    detailed_keywords = [
        'admission', 'fees', 'fee', 'placement', 'eligibility', 'criteria', 'process',
        'requirement', 'facility', 'facilities', 'hostel', 'scholarship', 'exam',
        'faculty', 'course', 'duration', 'how to', 'what is', 'what are',
        'when', 'where', 'why', 'explain', 'describe', 'tell me about',
        'information about', 'details', 'rules', 'regulations', 'timings',
        'apply', 'application', 'documents', 'needed', 'required'
    ]
    
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in detailed_keywords)

def generate_response(query):
    """Generate response using college database or handbook search"""
    
    # Check if asking about specific college
    college = find_college_fast(query)
    
    # If detailed question, search handbook
    if is_detailed_question(query):
        handbook_result = search_handbook(query)
        if handbook_result:
            return {
                'type': 'handbook_answer',
                'text': handbook_result,
                'college': college
            }
    
    # If specific college found, show card
    if college:
        return {
            'type': 'college',
            'college': college,
            'text': f"Here's information about {college['name']}:"
        }
    
    # Check for category
    category = detect_category(query)
    if category:
        colleges = get_colleges_by_category(category)
        if colleges:
            return {
                'type': 'list',
                'colleges': colleges,
                'text': f"Found {len(colleges)} colleges:"
            }
    
    # Try handbook search as fallback
    handbook_result = search_handbook(query)
    if handbook_result:
        return {
            'type': 'handbook_answer',
            'text': handbook_result
        }
    
    # Default response
    return {
        'type': 'help',
        'text': "I couldn't find specific information. You can ask about:\n• Specific colleges (e.g., 'Tell me about WIT')\n• College categories (e.g., 'Engineering colleges')\n• Detailed questions (e.g., 'What are the admission requirements?', 'Tell me about fees')"
    }

# Header
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 2rem; border-radius: 15px; text-align: center; color: white; 
            box-shadow: 0 8px 16px rgba(0,0,0,0.2); margin-bottom: 2rem;'>
    <h1 style='margin: 0; font-size: 2.5rem;'>🎓 Solapur Colleges Chatbot</h1>
    <p style='margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;'>
        Smart Assistant - Ask anything about colleges!
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 💬 Chat History")
    
    if st.session_state.messages:
        st.markdown(f"**{len(st.session_state.messages)} messages**")
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    else:
        st.info("No messages yet")
    
    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    
    quick_actions = {
        "🏛️ Universities": "Universities in Solapur",
        "⚙️ Engineering": "Engineering colleges",
        "🏥 Medical": "Medical colleges",
        "💼 Commerce": "Commerce colleges",
        "📋 All Colleges": "Show all colleges"
    }
    
    for label, query in quick_actions.items():
        if st.button(label, key=f"qa_{label}", use_container_width=True):
            st.session_state.quick_query = query
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Statistics")
    st.metric("Total Colleges", len(all_colleges))
    st.metric("Categories", 6)
    st.metric("Mode", "Simple Q&A")

# Main chat area
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### 💬 Chat")
    
    # Display messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="user-bubble">
                {msg["content"]}
                <div class="timestamp">{msg.get("timestamp", "")}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bot-bubble">
                {msg["content"]}
                <div class="timestamp">{msg.get("timestamp", "")}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if "college_card" in msg:
                st.markdown(msg["college_card"], unsafe_allow_html=True)
            
            if "college_list" in msg:
                for college in msg["college_list"][:5]:
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.markdown(f"**{college['name']}**")
                        st.caption(f"{college['type']}")
                    with col_b:
                        if st.button("View", key=f"v_{college['name']}_{len(st.session_state.messages)}"):
                            st.session_state.quick_query = f"Tell me about {college['name']}"
                            st.rerun()
    
    # Chat input
    if "quick_query" in st.session_state:
        prompt = st.session_state.quick_query
        del st.session_state.quick_query
    else:
        prompt = st.chat_input("💬 Ask anything about colleges...")
    
    if prompt:
        timestamp = datetime.now().strftime("%I:%M %p")
        
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": timestamp
        })
        
        # Generate response
        response = generate_response(prompt)
        
        # Create bot message
        bot_msg = {
            "role": "assistant",
            "content": response['text'],
            "timestamp": timestamp
        }
        
        if response['type'] == 'college':
            bot_msg["college_card"] = display_college_card(response['college'])
        elif response['type'] == 'list':
            bot_msg["college_list"] = response['colleges']
        elif response['type'] == 'handbook_answer' and response.get('college'):
            bot_msg["college_card"] = display_college_card(response['college'])
        
        st.session_state.messages.append(bot_msg)
        st.rerun()

with col2:
    st.markdown("### 💡 Suggested Questions")
    
    suggestions = [
        "Tell me about WIT",
        "Engineering colleges",
        "Admission requirements",
        "Fees information",
        "Placement details",
        "Hostel facilities"
    ]
    
    for sug in suggestions:
        if st.button(sug, key=f"sug_{sug}", use_container_width=True):
            st.session_state.quick_query = sug
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d; padding: 1rem;'>
    <p>🎓 Solapur Colleges Chatbot | Simple Q&A Mode | 35+ Colleges</p>
    <p>Ask about admissions, fees, placements, facilities, and more!</p>
</div>
""", unsafe_allow_html=True)
