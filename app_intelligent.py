"""
Intelligent Solapur Colleges Chatbot
With advanced question understanding, synonym recognition, and fast response
"""

import streamlit as st
import json
import time
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Solapur Colleges - Intelligent Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Intent Keywords with Synonyms
INTENT_KEYWORDS = {
    'hostel': {
        'keywords': ['hostel', 'accommodation', 'dormitory', 'stay', 'residence', 'boarding', 'living', 'rooms'],
        'field': 'facilities'
    },
    'facilities': {
        'keywords': ['facility', 'facilities', 'infrastructure', 'campus', 'amenities', 'resources', 'equipment'],
        'field': 'facilities'
    },
    'courses': {
        'keywords': ['course', 'courses', 'program', 'programs', 'branch', 'branches', 'department', 'departments', 'stream', 'streams', 'degree', 'degrees'],
        'field': 'courses'
    },
    'admission': {
        'keywords': ['admission', 'admit', 'admissions', 'join', 'enroll', 'enrollment', 'eligibility', 'entrance', 'apply', 'application', 'how to join'],
        'field': 'affiliation'
    },
    'placement': {
        'keywords': ['placement', 'placements', 'placed', 'job', 'jobs', 'recruit', 'recruitment', 'company', 'companies', 'package', 'salary', 'career', 'hiring'],
        'field': 'placement_rate'
    },
    'fees': {
        'keywords': ['fee', 'fees', 'cost', 'costs', 'price', 'pricing', 'charge', 'charges', 'tuition', 'expense', 'expenses', 'money'],
        'field': 'fees'
    },
    'location': {
        'keywords': ['location', 'address', 'where', 'situated', 'place', 'area', 'direction', 'directions', 'map'],
        'field': 'location'
    },
    'contact': {
        'keywords': ['contact', 'phone', 'mobile', 'number', 'call', 'email', 'mail', 'reach', 'connect', 'telephone'],
        'field': 'contact'
    }
}

# Performance Optimization: Load data once
@st.cache_data
def load_colleges_data():
    """Load and cache college data"""
    try:
        with open("solapur_colleges_database.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            all_colleges = []
            for category in data.get('categories', {}).values():
                all_colleges.extend(category['colleges'])
            return data, all_colleges
    except:
        return {}, []

colleges_data, all_colleges = load_colleges_data()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# CSS Styling
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
        margin: 0.5rem 0;
        max-width: 70%;
        float: right;
        clear: both;
    }
    .bot-bubble {
        background: white;
        color: #333;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.5rem 0;
        max-width: 75%;
        float: left;
        clear: both;
    }
</style>
""", unsafe_allow_html=True)

def detect_intent(query):
    """Detect user intent with synonym support"""
    query_lower = query.lower()
    detected = []
    
    for intent, data in INTENT_KEYWORDS.items():
        if any(kw in query_lower for kw in data['keywords']):
            detected.append(intent)
    
    return detected

def find_college_smart(query):
    """Smart college detection"""
    query_lower = query.lower()
    
    # Exact match
    for college in all_colleges:
        if college['name'].lower() == query_lower:
            return college
    
    # Short name match
    for college in all_colleges:
        if college['short_name'].lower() == query_lower:
            return college
    
    # Contains match
    for college in all_colleges:
        if query_lower in college['name'].lower() or college['name'].lower() in query_lower:
            return college
    
    # Word match
    query_words = set(query_lower.split())
    for college in all_colleges:
        name_words = set(college['name'].lower().split())
        if len(query_words & name_words) >= 2:
            return college
    
    return None

def generate_intelligent_response(query):
    """Generate intelligent response based on intent"""
    start_time = time.time()
    
    college = find_college_smart(query)
    intents = detect_intent(query)
    
    if college and intents:
        intent = intents[0]
        
        if intent == 'hostel':
            # Specific hostel question
            facilities = college.get('facilities', [])
            hostel_facilities = [f for f in facilities if 'hostel' in f.lower()]
            
            if hostel_facilities:
                text = f"**Hostel Facilities at {college['name']}:**\n\n"
                for fac in hostel_facilities:
                    text += f"• {fac}\n"
            else:
                text = f"**Hostel Information for {college['name']}:**\n\n"
                text += "Please contact the college directly for hostel availability and facilities.\n\n"
                text += f"📞 {college.get('contact', 'N/A')}\n"
                text += f"🌐 {college.get('website', 'N/A')}"
            
            response_time = time.time() - start_time
            return {'type': 'specific', 'text': text, 'time': response_time}
        
        elif intent == 'facilities':
            if 'hostel' in query.lower():
                # Asking about hostel within facilities
                facilities = college.get('facilities', [])
                hostel_facilities = [f for f in facilities if 'hostel' in f.lower()]
                
                if hostel_facilities:
                    text = f"**Hostel Facilities at {college['name']}:**\n\n"
                    for fac in hostel_facilities:
                        text += f"• {fac}\n"
                else:
                    text = "Hostel information not available. Please contact the college."
            else:
                # General facilities
                facilities = college.get('facilities', [])
                if facilities:
                    text = f"**Facilities at {college['name']}:**\n\n"
                    for fac in facilities:
                        text += f"• {fac}\n"
                else:
                    text = "Facility information not available."
            
            response_time = time.time() - start_time
            return {'type': 'specific', 'text': text, 'time': response_time}
        
        elif intent == 'courses':
            courses = college.get('courses', [])
            text = f"**Courses Offered at {college['name']}:**\n\n"
            for course in courses:
                text += f"• {course}\n"
            
            response_time = time.time() - start_time
            return {'type': 'specific', 'text': text, 'time': response_time}
        
        elif intent == 'fees':
            fees = college.get('fees', 'Not available')
            text = f"**Fee Structure for {college['name']}:**\n\n"
            text += f"💰 Annual Fee: {fees}\n\n"
            text += "Note: Fees may vary by course. Contact college for exact details."
            
            response_time = time.time() - start_time
            return {'type': 'specific', 'text': text, 'time': response_time}
        
        elif intent == 'admission':
            text = f"**Admission Information for {college['name']}:**\n\n"
            text += f"📚 Affiliated to: {college.get('affiliation', 'N/A')}\n\n"
            text += "For admission details:\n"
            text += f"• Visit: {college.get('website', 'N/A')}\n"
            text += f"• Contact: {college.get('contact', 'N/A')}\n"
            text += f"• Email: {college.get('email', 'N/A')}"
            
            response_time = time.time() - start_time
            return {'type': 'specific', 'text': text, 'time': response_time}
        
        elif intent == 'placement':
            text = f"**Placement Information for {college['name']}:**\n\n"
            text += f"📊 Placement Rate: {college.get('placement_rate', 'N/A')}\n\n"
            text += "The college has a dedicated placement cell.\n"
            text += f"For more details: {college.get('website', 'N/A')}"
            
            response_time = time.time() - start_time
            return {'type': 'specific', 'text': text, 'time': response_time}
        
        elif intent == 'contact':
            text = f"**Contact Information for {college['name']}:**\n\n"
            text += f"📍 {college.get('location', 'N/A')}\n"
            text += f"📞 {college.get('contact', 'N/A')}\n"
            text += f"📧 {college.get('email', 'N/A')}\n"
            text += f"🌐 {college.get('website', 'N/A')}"
            
            response_time = time.time() - start_time
            return {'type': 'specific', 'text': text, 'time': response_time}
    
    elif college and not intents:
        # Clarification needed
        response_time = time.time() - start_time
        return {
            'type': 'clarification',
            'college': college,
            'text': f"What would you like to know about **{college['name']}**?",
            'options': [
                "📚 Courses",
                "💰 Fees",
                "🏠 Hostel",
                "🏢 Facilities",
                "📝 Admission",
                "💼 Placements",
                "📍 Contact"
            ],
            'time': response_time
        }
    
    response_time = time.time() - start_time
    return {
        'type': 'help',
        'text': "I couldn't find that information. Try asking about a specific college or topic.",
        'time': response_time
    }

# Header
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 2rem; border-radius: 15px; text-align: center; color: white; 
            margin-bottom: 2rem;'>
    <h1 style='margin: 0;'>🎓 Intelligent Solapur Colleges Assistant</h1>
    <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>
        Smart • Fast • Accurate - Powered by AI
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 💬 Chat History")
    if st.session_state.messages:
        st.markdown(f"**{len(st.session_state.messages)} messages**")
        if st.button("🗑️ Clear", width="stretch"):
            st.session_state.messages = []
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Stats")
    st.metric("Colleges", len(all_colleges))
    st.metric("Response", "< 1 sec")
    
    st.markdown("---")
    st.markdown("### 💡 Try Asking")
    st.info("""
    • "Hostel facilities in WIT"
    • "Courses in Orchid College"
    • "WIT fees structure"
    • "Admission process"
    """)

# Main chat
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### 💬 Chat")
    
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
            
            if "options" in msg:
                cols = st.columns(len(msg["options"]))
                for idx, opt in enumerate(msg["options"]):
                    with cols[idx]:
                        if st.button(opt, key=f"opt_{idx}_{len(st.session_state.messages)}"):
                            st.session_state.quick_query = opt.split(" ", 1)[1]
                            st.rerun()
    
    if "quick_query" in st.session_state:
        prompt = st.session_state.quick_query
        del st.session_state.quick_query
    else:
        prompt = st.chat_input("Ask about any college...")
    
    if prompt:
        timestamp = datetime.now().strftime("%I:%M %p")
        
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": timestamp
        })
        
        response = generate_intelligent_response(prompt)
        
        bot_msg = {
            "role": "assistant",
            "content": response['text'],
            "timestamp": timestamp
        }
        
        if response['type'] == 'clarification':
            bot_msg["options"] = response['options']
        
        st.session_state.messages.append(bot_msg)
        st.rerun()

with col2:
    st.markdown("### 🎯 Quick Actions")
    if st.button("🏛️ Universities", width="stretch"):
        st.session_state.quick_query = "Universities in Solapur"
        st.rerun()
    if st.button("⚙️ Engineering", width="stretch"):
        st.session_state.quick_query = "Engineering colleges"
        st.rerun()
    if st.button("🏥 Medical", width="stretch"):
        st.session_state.quick_query = "Medical colleges"
        st.rerun()

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🎓 Intelligent Assistant | Fast & Accurate | 35+ Colleges</p>
</div>
""", unsafe_allow_html=True)
