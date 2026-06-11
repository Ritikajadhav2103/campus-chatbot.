import streamlit as st
import json
import time
from datetime import datetime

# Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="Solapur Colleges Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Performance Optimization: Load data once using @st.cache_data
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
colleges_data, all_colleges = load_colleges_data()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "search_query" not in st.session_state:
    st.session_state.search_query = ""

# Modern CSS with animations
st.markdown("""
<style>
    /* Main container */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Chat container */
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    /* User message bubble */
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
    
    /* Bot message bubble */
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
    
    /* Typing indicator */
    .typing-indicator {
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 20px;
        margin: 0.5rem auto 0.5rem 0;
        max-width: 100px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        animation: pulse 1.5s infinite;
    }
    
    .typing-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #667eea;
        margin: 0 2px;
        animation: bounce 1.4s infinite;
    }
    
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    
    /* College card */
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
    
    /* Quick reply buttons */
    .quick-reply {
        display: inline-block;
        background: white;
        border: 2px solid #667eea;
        color: #667eea;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.9rem;
    }
    
    .quick-reply:hover {
        background: #667eea;
        color: white;
    }
    
    /* Animations */
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes bounce {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-10px); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Timestamp */
    .timestamp {
        font-size: 0.7rem;
        color: #999;
        margin-top: 0.3rem;
    }
    
    /* Search box */
    .search-box {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Enhanced Intent Keywords with Synonyms for Intelligent Response
INTENT_KEYWORDS = {
    'hostel': ['hostel', 'accommodation', 'dormitory', 'stay', 'residence', 'boarding', 'living', 'rooms'],
    'facilities': ['facility', 'facilities', 'infrastructure', 'campus', 'amenities', 'resources', 'equipment'],
    'courses': ['course', 'courses', 'program', 'programs', 'branch', 'branches', 'department', 'departments', 'stream', 'streams', 'degree', 'degrees'],
    'admission': ['admission', 'admit', 'admissions', 'join', 'enroll', 'enrollment', 'eligibility', 'entrance', 'apply', 'application', 'how to join'],
    'placement': ['placement', 'placements', 'placed', 'job', 'jobs', 'recruit', 'recruitment', 'company', 'companies', 'package', 'salary', 'career', 'hiring'],
    'fees': ['fee', 'fees', 'cost', 'costs', 'price', 'pricing', 'charge', 'charges', 'tuition', 'expense', 'expenses', 'money'],
    'location': ['location', 'address', 'where', 'situated', 'place', 'area', 'direction', 'directions', 'map'],
    'contact': ['contact', 'phone', 'mobile', 'number', 'call', 'email', 'mail', 'reach', 'connect', 'telephone']
}

def detect_intent(query):
    """Detect user intent with synonym support"""
    query_lower = query.lower()
    detected = []
    
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(kw in query_lower for kw in keywords):
            detected.append(intent)
    
    return detected

# Enhanced keyword detection with synonyms and intent recognition
INTENT_KEYWORDS = {
    'hostel': {
        'keywords': ['hostel', 'accommodation', 'dormitory', 'stay', 'residence', 'boarding', 'living'],
        'response_field': 'hostel_availability'
    },
    'facilities': {
        'keywords': ['facility', 'facilities', 'infrastructure', 'campus', 'amenities', 'resources'],
        'response_field': 'facilities'
    },
    'courses': {
        'keywords': ['course', 'courses', 'program', 'programs', 'branch', 'branches', 'department', 'departments', 'stream', 'streams', 'degree'],
        'response_field': 'courses'
    },
    'admission': {
        'keywords': ['admission', 'admit', 'admissions', 'join', 'enroll', 'enrollment', 'eligibility', 'entrance', 'apply', 'application'],
        'response_field': 'admission_process'
    },
    'placement': {
        'keywords': ['placement', 'placements', 'placed', 'job', 'jobs', 'recruit', 'recruitment', 'company', 'companies', 'package', 'salary', 'career'],
        'response_field': 'placement_information'
    },
    'fees': {
        'keywords': ['fee', 'fees', 'cost', 'costs', 'price', 'pricing', 'charge', 'charges', 'tuition', 'expense', 'expenses'],
        'response_field': 'fees'
    },
    'location': {
        'keywords': ['location', 'address', 'where', 'situated', 'place', 'area', 'direction', 'directions'],
        'response_field': 'location'
    },
    'contact': {
        'keywords': ['contact', 'phone', 'mobile', 'number', 'call', 'email', 'mail', 'reach', 'connect'],
        'response_field': 'contact'
    },
    'website': {
        'keywords': ['website', 'site', 'web', 'url', 'link', 'online', 'portal'],
        'response_field': 'website'
    }
}

def detect_intent(query):
    """Detect user intent from query with synonym support"""
    query_lower = query.lower()
    detected_intents = []
    
    for intent, data in INTENT_KEYWORDS.items():
        if any(keyword in query_lower for keyword in data['keywords']):
            detected_intents.append(intent)
    
    return detected_intents

# Smart keyword detection for fast response
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
    """Optimized college search with multiple matching strategies"""
    query_lower = query.lower()
    
    # Strategy 1: Exact name match (fastest)
    for college in all_colleges:
        if college['name'].lower() == query_lower:
            return college
    
    # Strategy 2: Short name match
    for college in all_colleges:
        if college['short_name'].lower() == query_lower:
            return college
    
    # Strategy 3: Contains match
    for college in all_colleges:
        if query_lower in college['name'].lower() or college['name'].lower() in query_lower:
            return college
    
    # Strategy 4: Word match
    query_words = set(query_lower.split())
    for college in all_colleges:
        name_words = set(college['name'].lower().split())
        if len(query_words & name_words) >= 2:  # At least 2 words match
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
    """Display college as a beautiful card using Streamlit components"""
    # This function now returns None and uses st.image directly
    return None

def generate_response(query):
    """Enhanced response generation with intelligent intent detection and synonym support"""
    query_lower = query.lower()
    
    # First, try to find which college the question is about
    college = find_college_fast(query)
    
    # Detect user intent with synonym support
    intents = detect_intent(query)
    
    if college and intents:
        # User asked specific question about a college
        intent = intents[0]  # Primary intent
        
        if intent == 'hostel':
            # Specific hostel question - return ONLY hostel info
            facilities = college.get('facilities', [])
            hostel_facilities = [f for f in facilities if 'hostel' in f.lower()]
            
            if hostel_facilities:
                hostel_text = "\n• ".join(hostel_facilities)
                response_text = f"**Hostel Facilities at {college['name']}:**\n\n• {hostel_text}"
            else:
                response_text = f"**Hostel Information for {college['name']}:**\n\nPlease contact the college directly for hostel availability and facilities.\n\n📞 {college.get('contact', 'N/A')}\n🌐 {college.get('website', 'N/A')}"
            
            return {
                'type': 'specific',
                'text': response_text,
                'college': college
            }
        
        elif intent == 'facilities':
            # Check if asking specifically about hostel within facilities
            if 'hostel' in query_lower or 'accommodation' in query_lower or 'dormitory' in query_lower:
                facilities = college.get('facilities', [])
                hostel_facilities = [f for f in facilities if 'hostel' in f.lower()]
                
                if hostel_facilities:
                    hostel_text = "\n• ".join(hostel_facilities)
                    response_text = f"**Hostel Facilities at {college['name']}:**\n\n• {hostel_text}"
                else:
                    response_text = f"**Hostel Information:**\n\nPlease contact the college for hostel details.\n📞 {college.get('contact', 'N/A')}"
            else:
                # General facilities (excluding hostel if not asked)
                facilities = college.get('facilities', [])
                if facilities:
                    facilities_text = "\n• ".join(facilities)
                    response_text = f"**Facilities at {college['name']}:**\n\n• {facilities_text}"
                else:
                    response_text = f"**Facilities Information:**\n\nPlease visit the college website for detailed facility information."
            
            return {
                'type': 'specific',
                'text': response_text,
                'college': college
            }
        
        elif intent == 'courses':
            courses = college.get('courses', [])
            if courses:
                courses_text = "\n• ".join(courses)
                response_text = f"**Courses Offered at {college['name']}:**\n\n• {courses_text}"
            else:
                response_text = f"**Courses Information:**\n\nPlease visit the college website for course details."
            
            return {
                'type': 'specific',
                'text': response_text,
                'college': college
            }
        
        elif intent == 'admission':
            affiliation = college.get('affiliation', 'Information not available')
            response_text = f"**Admission Information for {college['name']}:**\n\n"
            response_text += f"📚 Affiliated to: {affiliation}\n\n"
            response_text += "For detailed admission process:\n"
            response_text += f"• Visit: {college.get('website', 'N/A')}\n"
            response_text += f"• Contact: {college.get('contact', 'N/A')}\n"
            response_text += f"• Email: {college.get('email', 'N/A')}"
            
            return {
                'type': 'specific',
                'text': response_text,
                'college': college
            }
        
        elif intent == 'placement':
            placement_rate = college.get('placement_rate', 'Information not available')
            response_text = f"**Placement Information for {college['name']}:**\n\n"
            response_text += f"📊 Placement Rate: {placement_rate}\n\n"
            response_text += "The college has a dedicated placement cell that works with top companies for student placements.\n\n"
            response_text += f"For more details, visit: {college.get('website', 'N/A')}"
            
            return {
                'type': 'specific',
                'text': response_text,
                'college': college
            }
        
        elif intent == 'fees':
            fees_info = college.get('fees', 'Not available')
            response_text = f"**Fee Structure for {college['name']}:**\n\n"
            response_text += f"💰 Annual Fee: {fees_info}\n\n"
            response_text += "Note: Fees may vary by course and category. Please contact the college for exact fee structure."
            
            return {
                'type': 'specific',
                'text': response_text,
                'college': college
            }
        
        elif intent == 'location':
            response_text = f"**Location of {college['name']}:**\n\n"
            response_text += f"📍 Address: {college.get('location', 'N/A')}\n"
            response_text += f"🌐 Website: {college.get('website', 'N/A')}"
            
            return {
                'type': 'specific',
                'text': response_text,
                'college': college
            }
        
        elif intent == 'contact':
            response_text = f"**Contact Information for {college['name']}:**\n\n"
            response_text += f"📍 Address: {college.get('location', 'N/A')}\n"
            response_text += f"📞 Phone: {college.get('contact', 'N/A')}\n"
            response_text += f"📧 Email: {college.get('email', 'N/A')}\n"
            response_text += f"🌐 Website: {college.get('website', 'N/A')}"
            
            return {
                'type': 'specific',
                'text': response_text,
                'college': college
            }
    
    elif college and not intents:
        # User asked about college but no specific intent - show full card
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
    
    # Default response
    return {
        'type': 'help',
        'text': "I couldn't understand that. You can ask about colleges in Solapur or search a college name."
    }

# Header
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 2rem; border-radius: 15px; text-align: center; color: white; 
            box-shadow: 0 8px 16px rgba(0,0,0,0.2); margin-bottom: 2rem;'>
    <h1 style='margin: 0; font-size: 2.5rem;'>🎓 Solapur Colleges Chatbot</h1>
    <p style='margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;'>
        Fast, Interactive, and Smart - Get instant college information
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar with chat history and quick actions
with st.sidebar:
    st.markdown("### 💬 Chat History")
    
    if st.session_state.messages:
        st.markdown(f"**{len(st.session_state.messages)} messages**")
        if st.button("🗑️ Clear History", width="stretch"):
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
        if st.button(label, key=f"qa_{label}", width="stretch"):
            st.session_state.quick_query = query
    
    st.markdown("---")
    st.markdown("### 📊 Statistics")
    st.metric("Total Colleges", len(all_colleges))
    st.metric("Categories", 6)
    st.metric("Response Time", "< 0.5s")
    
    st.markdown("---")
    st.markdown("### 🔍 Search")
    search_input = st.text_input("Search college name", key="search_input")
    if search_input:
        st.session_state.quick_query = f"Tell me about {search_input}"

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
            
            if "college_data" in msg:
                # Display college card using Streamlit components with attractive styling
                college = msg["college_data"]
                import os
                
                # Create a beautiful card container
                st.markdown("""
                <div style='background: white; border-radius: 15px; padding: 0; 
                            box-shadow: 0 8px 16px rgba(0,0,0,0.1); overflow: hidden; margin: 1rem 0;'>
                """, unsafe_allow_html=True)
                
                # Check for local image
                local_image = f"data/college_images/{college['short_name'].lower().replace(' ', '_')}.jpg"
                if os.path.exists(local_image):
                    st.image(local_image, width="stretch")
                else:
                    photo_url = college.get('photo_url', 'https://images.unsplash.com/photo-1562774053-701939374585?w=800')
                    st.image(photo_url, width="stretch")
                
                # College info with better styling
                st.markdown(f"""
                <div style='padding: 1.5rem;'>
                    <h2 style='color: #667eea; margin: 0 0 0.5rem 0; font-size: 1.8rem;'>{college['name']}</h2>
                    <p style='color: #666; font-size: 1rem; margin: 0 0 1.5rem 0;'>
                        {college['type']} | Est. {college['established']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # About section with better styling
                history = college.get('history', college.get('description', 'Information not available.'))
                st.markdown(f"""
                <div style='padding: 0 1.5rem 1rem 1.5rem;'>
                    <h3 style='color: #333; font-size: 1.2rem; margin-bottom: 0.5rem;'>📖 About</h3>
                    <p style='color: #555; line-height: 1.6; font-size: 0.95rem;'>{history[:300]}...</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Courses with better styling
                st.markdown("""
                <div style='padding: 0 1.5rem 1rem 1.5rem;'>
                    <h3 style='color: #333; font-size: 1.2rem; margin-bottom: 0.8rem;'>📚 Courses Offered</h3>
                </div>
                """, unsafe_allow_html=True)
                
                cols = st.columns(3)
                for idx, course in enumerate(college['courses'][:6]):
                    with cols[idx % 3]:
                        st.markdown(f"""
                        <div style='padding: 0 0.5rem;'>
                            <span style='display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                         color: white; padding: 0.5rem 1rem; border-radius: 20px; margin: 0.3rem 0;
                                         font-size: 0.85rem; font-weight: 500; white-space: nowrap;
                                         box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);'>{course}</span>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Contact with better styling
                st.markdown(f"""
                <div style='padding: 1rem 1.5rem 1.5rem 1.5rem;'>
                    <h3 style='color: #333; font-size: 1.2rem; margin-bottom: 0.8rem;'>📍 Contact</h3>
                    <p style='color: #555; line-height: 1.8; font-size: 0.95rem; margin: 0;'>
                        📍 <strong>Location:</strong> {college['location']}<br>
                        📞 <strong>Phone:</strong> {college['contact']}<br>
                        📧 <strong>Email:</strong> {college['email']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Website button
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.link_button("🌐 Visit Website", college['website'], use_container_width=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            
            if "college_list" in msg:
                for idx, college in enumerate(msg["college_list"][:5]):
                    msg_idx = st.session_state.messages.index(msg)
                    st.markdown(f"""
                    <div style='background: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                                box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: flex; 
                                justify-content: space-between; align-items: center;'>
                        <div>
                            <div style='font-weight: 600; color: #333; font-size: 1.1rem;'>{college['name']}</div>
                            <div style='color: #666; font-size: 0.9rem; margin-top: 0.3rem;'>{college['type']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("View Details", key=f"v_{college['name']}_{msg_idx}_{idx}", width="stretch"):
                        st.session_state.quick_query = f"Tell me about {college['name']}"
                        st.rerun()
    
    # Chat input
    if "quick_query" in st.session_state:
        prompt = st.session_state.quick_query
        del st.session_state.quick_query
    else:
        prompt = st.chat_input("💬 Ask about any college...")
    
    if prompt:
        timestamp = datetime.now().strftime("%I:%M %p")
        
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": timestamp
        })
        
        # Generate response immediately
        response = generate_response(prompt)
        
        # Create bot message
        bot_msg = {
            "role": "assistant",
            "content": response['text'],
            "timestamp": timestamp
        }
        
        if response['type'] == 'college':
            bot_msg["college_data"] = response['college']
        elif response['type'] == 'specific':
            # For specific questions, just show the text answer
            pass  # Text is already in content
        elif response['type'] == 'list':
            bot_msg["college_list"] = response['colleges']
        
        st.session_state.messages.append(bot_msg)
        st.rerun()

with col2:
    st.markdown("### 💡 Suggested Questions")
    
    suggestions = [
        "Tell me about WIT",
        "Engineering colleges",
        "Medical colleges",
        "Best colleges in Solapur",
        "Show all colleges"
    ]
    
    for sug in suggestions:
        if st.button(sug, key=f"sug_{sug}", width="stretch"):
            st.session_state.quick_query = sug
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d; padding: 1rem;'>
    <p>🎓 Solapur Colleges Chatbot | Fast & Interactive | 35+ Colleges</p>
    <p>Optimized for speed and performance | Mobile-friendly design</p>
</div>
""", unsafe_allow_html=True)
