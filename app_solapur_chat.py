import streamlit as st
import json
import os
from datetime import datetime
import time

# Page config
st.set_page_config(
    page_title="Solapur Colleges Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "colleges_data" not in st.session_state:
    try:
        with open("solapur_colleges_database.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # Flatten colleges into a searchable list
            st.session_state.colleges_data = data
            st.session_state.all_colleges = []
            for category in data.get('categories', {}).values():
                st.session_state.all_colleges.extend(category['colleges'])
    except:
        st.session_state.colleges_data = {}
        st.session_state.all_colleges = []

# CSS
st.markdown("""
<style>
    .stApp {
        background-color: #f8f9fa;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
    }
    .bot-message {
        background: white;
        border: 1px solid #e0e0e0;
        margin-right: 20%;
    }
    .college-card {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .college-image {
        width: 100%;
        height: 250px;
        object-fit: cover;
    }
    .college-content {
        padding: 1.5rem;
    }
    .college-name {
        font-size: 1.8rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    .college-type {
        font-size: 1rem;
        color: #6c757d;
        margin-bottom: 1rem;
    }
    .section-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #333;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .history-text {
        line-height: 1.8;
        color: #555;
        text-align: justify;
    }
    .course-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-size: 0.9rem;
    }
    .info-row {
        display: flex;
        align-items: center;
        margin: 0.5rem 0;
        color: #555;
    }
    .info-icon {
        margin-right: 0.5rem;
        font-size: 1.2rem;
    }
    .website-link {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        text-decoration: none;
        margin-top: 1rem;
        font-weight: 600;
    }
    .website-link:hover {
        background: #764ba2;
        color: white;
    }
    .timestamp {
        font-size: 0.75rem;
        color: #999;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def find_college(query):
    """Find college by name or short name"""
    query_lower = query.lower()
    
    for college in st.session_state.all_colleges:
        # Check full name
        if college['name'].lower() in query_lower or query_lower in college['name'].lower():
            return college
        # Check short name
        if college['short_name'].lower() in query_lower or query_lower in college['short_name'].lower():
            return college
        # Check for partial matches
        name_words = college['name'].lower().split()
        if any(word in query_lower for word in name_words if len(word) > 4):
            return college
    
    return None

def display_college_card(college):
    """Display college information as a beautiful card"""
    
    # Get photo URL or use placeholder
    photo_url = college.get('photo_url', 'https://images.unsplash.com/photo-1562774053-701939374585?w=800')
    
    card_html = f"""
    <div class="college-card">
        <img src="{photo_url}" class="college-image" alt="{college['name']}">
        <div class="college-content">
            <div class="college-name">{college['name']}</div>
            <div class="college-type">{college['type']} | Established {college['established']}</div>
            
            <div class="section-title">📖 About the College</div>
            <p class="history-text">{college.get('history', college.get('description', 'Information not available.'))}</p>
            
            <div class="section-title">📚 Courses Offered</div>
            <div>
    """
    
    for course in college['courses']:
        card_html += f'<span class="course-badge">{course}</span>'
    
    card_html += f"""
            </div>
            
            <div class="section-title">📍 Location & Contact</div>
            <div class="info-row">
                <span class="info-icon">📍</span>
                <span>{college['location']}</span>
            </div>
            <div class="info-row">
                <span class="info-icon">📞</span>
                <span>{college['contact']}</span>
            </div>
            <div class="info-row">
                <span class="info-icon">📧</span>
                <span>{college['email']}</span>
            </div>
            
            <div class="section-title">🌐 Official Website</div>
            <a href="{college['website']}" target="_blank" class="website-link">
                Visit Website →
            </a>
        </div>
    </div>
    """
    
    return card_html

def detect_query_type(query):
    """Detect what user is asking about"""
    query_lower = query.lower()
    
    # Check if asking about specific college
    if any(word in query_lower for word in ['tell me about', 'show details', 'information about', 'details of', 'about']):
        return 'college_details'
    
    # Check if asking for list
    if any(word in query_lower for word in ['list', 'show all', 'all colleges', 'engineering colleges', 'medical colleges']):
        return 'list_colleges'
    
    return 'general'

def generate_response(query):
    """Generate response based on query"""
    query_type = detect_query_type(query)
    
    if query_type == 'college_details':
        # Try to find the college
        college = find_college(query)
        
        if college:
            return {
                'type': 'college_card',
                'college': college,
                'text': f"Here's detailed information about {college['name']}:"
            }
        else:
            return {
                'type': 'text',
                'text': "Sorry, I could not find information about that college. Please check the college name and try again.\n\n💡 Try asking:\n• 'Tell me about Walchand Institute of Technology'\n• 'Show details of KBP College'\n• 'Information about Dayanand College'"
            }
    
    elif query_type == 'list_colleges':
        # Detect category
        query_lower = query.lower()
        if 'engineering' in query_lower:
            colleges = [c for c in st.session_state.all_colleges if 'engineering' in c['type'].lower() or 'polytechnic' in c['type'].lower()]
            return {
                'type': 'list',
                'colleges': colleges,
                'text': f"Here are {len(colleges)} engineering colleges in Solapur:"
            }
        elif 'medical' in query_lower:
            colleges = [c for c in st.session_state.all_colleges if 'medical' in c['type'].lower() or 'health' in c['type'].lower() or 'dental' in c['type'].lower() or 'nursing' in c['type'].lower()]
            return {
                'type': 'list',
                'colleges': colleges,
                'text': f"Here are {len(colleges)} medical & health colleges in Solapur:"
            }
        else:
            return {
                'type': 'list',
                'colleges': st.session_state.all_colleges[:10],
                'text': f"Here are some colleges in Solapur (showing 10 of {len(st.session_state.all_colleges)}):"
            }
    
    else:
        return {
            'type': 'text',
            'text': """👋 Welcome to Solapur Colleges Chatbot!

I can help you with:
• Detailed information about specific colleges
• List of colleges by category
• Contact information and courses

💬 Try asking:
• "Tell me about Walchand Institute of Technology"
• "Show details of Orchid College"
• "List engineering colleges"
• "Information about Dayanand College"

What would you like to know?"""
        }

# Header
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 2rem; border-radius: 10px; text-align: center; color: white; margin-bottom: 2rem;'>
    <h1>🎓 Solapur Colleges Chatbot</h1>
    <p>Get detailed information about 35+ colleges in Solapur</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 💡 Quick Examples")
    
    examples = [
        "Tell me about WIT",
        "Show details of KBP College",
        "Information about Dayanand College",
        "List engineering colleges",
        "Medical colleges in Solapur"
    ]
    
    for example in examples:
        if st.button(example, key=f"ex_{example}", use_container_width=True):
            st.session_state.quick_query = example
    
    st.markdown("---")
    st.markdown("### 📊 Statistics")
    st.metric("Total Colleges", len(st.session_state.all_colleges))
    st.metric("Categories", 6)
    
    st.markdown("---")
    st.markdown("### 🎓 Categories")
    st.markdown("""
    • Universities (2)
    • Engineering (7)
    • Medical & Health (4)
    • Commerce/Management (4)
    • Arts/Science (5)
    • Other Colleges (7)
    """)

# Main chat area
st.markdown("### 💬 Chat")

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <div>{msg["content"]}</div>
            <div class="timestamp">{msg.get("timestamp", "")}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <div>{msg["content"]}</div>
            <div class="timestamp">{msg.get("timestamp", "")}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display college card if present
        if "college_card" in msg:
            st.markdown(msg["college_card"], unsafe_allow_html=True)
        
        # Display college list if present
        if "college_list" in msg:
            for college in msg["college_list"]:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{college['name']}**")
                    st.caption(f"{college['type']} | {college['location']}")
                with col2:
                    if st.button("View Details", key=f"view_{college['name']}_{len(st.session_state.messages)}"):
                        st.session_state.quick_query = f"Tell me about {college['name']}"
                        st.rerun()

# Chat input
if "quick_query" in st.session_state:
    prompt = st.session_state.quick_query
    del st.session_state.quick_query
else:
    prompt = st.chat_input("Ask about any college in Solapur...")

if prompt:
    timestamp = datetime.now().strftime("%I:%M %p")
    
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": timestamp
    })
    
    # Generate response
    with st.spinner("Searching..."):
        time.sleep(0.5)
        response = generate_response(prompt)
    
    # Add bot message
    bot_msg = {
        "role": "assistant",
        "content": response['text'],
        "timestamp": timestamp
    }
    
    # Add college card if present
    if response['type'] == 'college_card':
        bot_msg["college_card"] = display_college_card(response['college'])
    
    # Add college list if present
    if response['type'] == 'list':
        bot_msg["college_list"] = response['colleges']
    
    st.session_state.messages.append(bot_msg)
    
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d; padding: 1rem;'>
    <p>🎓 Solapur Colleges Chatbot | Detailed information about 35+ colleges</p>
    <p>Ask about any college to see photos, history, courses, and contact details</p>
</div>
""", unsafe_allow_html=True)
