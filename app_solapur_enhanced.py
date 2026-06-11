import streamlit as st
import json
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Solapur Colleges Guide",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "selected_college" not in st.session_state:
    st.session_state.selected_college = None
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None
if "colleges_data" not in st.session_state:
    try:
        with open("solapur_colleges_database.json", "r", encoding="utf-8") as f:
            st.session_state.colleges_data = json.load(f)
    except:
        st.session_state.colleges_data = {}

# Dynamic CSS
def get_theme_css(dark_mode):
    if dark_mode:
        return """
<style>
    :root {
        --primary-color: #667eea;
        --bg-color: #1a1a2e;
        --card-bg: #16213e;
        --text-color: #eaeaea;
        --text-secondary: #a0a0a0;
        --border-color: #3a3a52;
        --hover-bg: #252541;
    }
    .stApp { background-color: var(--bg-color); color: var(--text-color); }
"""
    else:
        return """
<style>
    :root {
        --primary-color: #667eea;
        --bg-color: #f8f9fa;
        --card-bg: #ffffff;
        --text-color: #212529;
        --text-secondary: #6c757d;
        --border-color: #e9ecef;
        --hover-bg: #f8f9ff;
    }
    .stApp { background-color: var(--bg-color); color: var(--text-color); }
"""

st.markdown(get_theme_css(st.session_state.dark_mode), unsafe_allow_html=True)

# Common CSS
st.markdown("""
<style>
    .college-card {
        background: var(--card-bg);
        border: 2px solid var(--border-color);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .college-card:hover {
        border-color: var(--primary-color);
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(102,126,234,0.2);
    }
    .college-name {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    .college-type {
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
    }
    .college-info {
        font-size: 0.95rem;
        color: var(--text-color);
        line-height: 1.6;
    }
    .category-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1.5rem 0 1rem 0;
        font-size: 1.5rem;
        font-weight: 700;
    }
    .detail-section {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .detail-title {
        color: var(--primary-color);
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .badge {
        display: inline-block;
        background: var(--primary-color);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.85rem;
        margin: 0.2rem;
    }
    .stat-box {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
    }
    .stat-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
    }
</style>
""", unsafe_allow_html=True)

def detect_category(query):
    """Detect which category user is asking about"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['engineering', 'engineer', 'b.tech', 'btech', 'polytechnic']):
        return 'engineering'
    elif any(word in query_lower for word in ['medical', 'mbbs', 'doctor', 'health', 'nursing', 'dental']):
        return 'medical'
    elif any(word in query_lower for word in ['commerce', 'b.com', 'bcom', 'management', 'mba', 'bba']):
        return 'commerce_management'
    elif any(word in query_lower for word in ['arts', 'science', 'b.a', 'b.sc', 'bsc']):
        return 'arts_science'
    elif any(word in query_lower for word in ['university', 'universities']):
        return 'universities'
    elif any(word in query_lower for word in ['all', 'list', 'show all', 'complete list']):
        return 'all'
    else:
        return None

def display_college_card(college, category_key):
    """Display a college card with click functionality"""
    with st.container():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f"""
            <div class="college-card">
                <div class="college-name">{college['name']}</div>
                <div class="college-type">📍 {college['type']} | Est. {college['established']}</div>
                <div class="college-info">
                    📞 {college['contact']}<br/>
                    📧 {college['email']}<br/>
                    🌐 {college['website']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("View Details", key=f"view_{college['name']}", use_container_width=True):
                st.session_state.selected_college = college
                st.session_state.selected_category = category_key
                st.rerun()

def display_college_details(college):
    """Display detailed information about a college"""
    st.markdown(f"## 🎓 {college['name']}")
    st.markdown(f"**{college['short_name']}** | {college['type']}")
    st.markdown("---")
    
    # Basic Info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-number">📅</div>
            <div class="stat-label">Established</div>
            <div class="stat-number" style="font-size: 1.5rem;">""" + college['established'] + """</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if 'intake' in college:
            st.markdown("""
            <div class="stat-box">
                <div class="stat-number">👥</div>
                <div class="stat-label">Intake</div>
                <div class="stat-number" style="font-size: 1.5rem;">""" + college['intake'] + """</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        if 'fees' in college:
            st.markdown("""
            <div class="stat-box">
                <div class="stat-number">💰</div>
                <div class="stat-label">Annual Fees</div>
                <div class="stat-number" style="font-size: 1.2rem;">""" + college['fees'] + """</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Description
    st.markdown('<div class="detail-section">', unsafe_allow_html=True)
    st.markdown('<div class="detail-title">📖 About</div>', unsafe_allow_html=True)
    st.write(college['description'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Courses
    st.markdown('<div class="detail-section">', unsafe_allow_html=True)
    st.markdown('<div class="detail-title">📚 Courses Offered</div>', unsafe_allow_html=True)
    courses_html = ""
    for course in college['courses']:
        courses_html += f'<span class="badge">{course}</span>'
    st.markdown(courses_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Contact Information
    st.markdown('<div class="detail-section">', unsafe_allow_html=True)
    st.markdown('<div class="detail-title">📞 Contact Information</div>', unsafe_allow_html=True)
    st.markdown(f"""
    **Address:** {college['location']}  
    **Phone:** {college['contact']}  
    **Email:** {college['email']}  
    **Website:** [{college['website']}]({college['website']})  
    **Affiliation:** {college['affiliation']}
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Facilities
    if 'facilities' in college:
        st.markdown('<div class="detail-section">', unsafe_allow_html=True)
        st.markdown('<div class="detail-title">🏛️ Facilities</div>', unsafe_allow_html=True)
        for facility in college['facilities']:
            st.markdown(f"• {facility}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Placement (if available)
    if 'placement_rate' in college:
        st.markdown('<div class="detail-section">', unsafe_allow_html=True)
        st.markdown('<div class="detail-title">🎯 Placement Information</div>', unsafe_allow_html=True)
        st.markdown(f"**Placement Rate:** {college['placement_rate']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Back button
    if st.button("⬅️ Back to List", use_container_width=True):
        st.session_state.selected_college = None
        st.rerun()

def display_category_colleges(category_key, category_data):
    """Display all colleges in a category"""
    st.markdown(f'<div class="category-header">{category_data["name"]}</div>', unsafe_allow_html=True)
    st.markdown(f"**Total Colleges:** {len(category_data['colleges'])}")
    
    for college in category_data['colleges']:
        display_college_card(college, category_key)

def display_all_colleges():
    """Display all colleges section-wise"""
    categories = st.session_state.colleges_data.get('categories', {})
    
    # Statistics
    st.markdown("## 📊 Solapur Colleges Overview")
    cols = st.columns(6)
    
    category_names = {
        'universities': '🏛️ Universities',
        'engineering': '⚙️ Engineering',
        'medical': '🏥 Medical',
        'commerce_management': '💼 Commerce',
        'arts_science': '📚 Arts/Science',
        'other': '🎓 Others'
    }
    
    for idx, (key, name) in enumerate(category_names.items()):
        if key in categories:
            count = len(categories[key]['colleges'])
            with cols[idx]:
                st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-number">{count}</div>
                    <div class="stat-label">{name}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Display each category
    for key in ['universities', 'engineering', 'medical', 'commerce_management', 'arts_science', 'other']:
        if key in categories:
            display_category_colleges(key, categories[key])

# Header
header_col1, header_col2 = st.columns([6, 1])

with header_col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 10px; text-align: center; color: white;'>
        <h1>🎓 Solapur Colleges Guide</h1>
        <p>Complete Information about 35+ Colleges in Solapur</p>
    </div>
    """, unsafe_allow_html=True)

with header_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
    if st.button(f"{theme_icon}", key="theme_toggle", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("### 🔍 Quick Navigation")
    
    categories = {
        'all': '📋 All Colleges',
        'universities': '🏛️ Universities',
        'engineering': '⚙️ Engineering',
        'medical': '🏥 Medical & Health',
        'commerce_management': '💼 Commerce/Management',
        'arts_science': '📚 Arts/Science',
        'other': '🎓 Other Colleges'
    }
    
    for key, label in categories.items():
        if st.button(label, key=f"cat_{key}", use_container_width=True):
            st.session_state.selected_category = key
            st.session_state.selected_college = None
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Statistics")
    total = sum(len(cat['colleges']) for cat in st.session_state.colleges_data.get('categories', {}).values())
    st.metric("Total Colleges", total)
    st.metric("City", "Solapur")
    st.metric("State", "Maharashtra")
    
    st.markdown("---")
    st.markdown("### 💡 Quick Search")
    st.info("""
    **Try asking:**
    - "Engineering colleges"
    - "Medical colleges"
    - "All colleges in Solapur"
    - "Commerce colleges"
    """)

# Main content
if st.session_state.selected_college:
    # Show college details
    display_college_details(st.session_state.selected_college)
elif st.session_state.selected_category:
    # Show category colleges
    if st.session_state.selected_category == 'all':
        display_all_colleges()
    else:
        category_data = st.session_state.colleges_data['categories'].get(st.session_state.selected_category)
        if category_data:
            display_category_colleges(st.session_state.selected_category, category_data)
else:
    # Welcome screen
    st.markdown("""
    <div style='text-align: center; padding: 3rem;'>
        <div style='font-size: 5rem; margin-bottom: 1rem;'>🎓</div>
        <h2>Welcome to Solapur Colleges Guide</h2>
        <p style='font-size: 1.2rem; color: var(--text-secondary); margin: 1rem 0;'>
            Explore 35+ colleges across 6 categories
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick category cards
    st.markdown("### 🔍 Browse by Category")
    
    cols = st.columns(3)
    quick_cats = [
        ('engineering', '⚙️ Engineering', 'Technical Education'),
        ('medical', '🏥 Medical', 'Healthcare Education'),
        ('commerce_management', '💼 Commerce', 'Business Education'),
        ('arts_science', '📚 Arts/Science', 'Liberal Arts'),
        ('universities', '🏛️ Universities', 'Higher Education'),
        ('all', '📋 All Colleges', 'Complete List')
    ]
    
    for idx, (key, icon_name, desc) in enumerate(quick_cats):
        with cols[idx % 3]:
            if st.button(f"{icon_name}\n{desc}", key=f"quick_{key}", use_container_width=True):
                st.session_state.selected_category = key
                st.rerun()

# Chat input
st.markdown("---")
st.markdown("### 💬 Ask About Colleges")

prompt = st.chat_input("Ask about colleges in Solapur...")

if prompt:
    # Detect category
    category = detect_category(prompt)
    
    if category:
        st.session_state.selected_category = category
        st.session_state.selected_college = None
        st.rerun()
    else:
        st.info("💡 Try asking about: Engineering colleges, Medical colleges, Commerce colleges, or 'All colleges in Solapur'")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 1rem; color: var(--text-secondary);'>
    <p>🎓 Solapur Colleges Guide | Complete Information about Higher Education in Solapur</p>
    <p>Data includes 35+ colleges across Universities, Engineering, Medical, Commerce, Arts/Science categories</p>
</div>
""", unsafe_allow_html=True)
