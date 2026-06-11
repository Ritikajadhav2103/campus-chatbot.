import streamlit as st
import json
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Solapur Colleges Directory",
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
            st.session_state.colleges_data = json.load(f)
    except:
        st.session_state.colleges_data = {}

# Dynamic CSS
def get_theme_css(dark_mode):
    if dark_mode:
        return """
<style>
    :root {
        --bg-color: #1a1a2e;
        --card-bg: #16213e;
        --text-color: #eaeaea;
        --text-secondary: #a0a0a0;
        --primary-color: #667eea;
        --border-color: #3a3a52;
        --hover-bg: #252541;
    }
    .stApp { background-color: var(--bg-color); color: var(--text-color); }
    [data-testid="stSidebar"] { background-color: var(--card-bg); }
</style>"""
    else:
        return """
<style>
    :root {
        --bg-color: #f8f9fa;
        --card-bg: #ffffff;
        --text-color: #212529;
        --text-secondary: #6c757d;
        --primary-color: #667eea;
        --border-color: #e9ecef;
        --hover-bg: #f8f9ff;
    }
    .stApp { background-color: var(--bg-color); color: var(--text-color); }
</style>"""

st.markdown(get_theme_css(st.session_state.dark_mode), unsafe_allow_html=True)

# Common CSS
st.markdown("""
<style>
    .category-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-size: 1.3rem;
        font-weight: 700;
    }
    .college-card {
        background: var(--card-bg);
        border: 2px solid var(--border-color);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    .college-card:hover {
        border-color: var(--primary-color);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(102,126,234,0.2);
    }
    .college-name {
        color: var(--primary-color);
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .college-info {
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin: 0.3rem 0;
    }
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def format_category_colleges(category_name, colleges_list):
    """Format colleges in a category for display"""
    output = f"\n### {category_name}\n\n"
    
    for idx, college in enumerate(colleges_list, 1):
        output += f"**{idx}. {college['name']}**\n"
        if 'type' in college:
            output += f"   • Type: {college['type']}\n"
        if 'location' in college:
            output += f"   • Location: {college['location']}\n"
        if 'contact' in college:
            output += f"   • Contact: {college['contact']}\n"
        if 'courses' in college and isinstance(college['courses'], list):
            output += f"   • Courses: {', '.join(college['courses'][:3])}\n"
        if 'fees' in college:
            output += f"   • Fees: {college['fees']}\n"
        if 'website' in college:
            output += f"   • Website: {college['website']}\n"
        output += "\n"
    
    return output

def search_colleges(query):
    """Search and return colleges based on query"""
    query_lower = query.lower()
    categories = st.session_state.colleges_data.get('categories', {})
    
    response = ""
    
    # Check for category-specific queries
    if any(word in query_lower for word in ['all college', 'list college', 'show college', 'colleges in solapur']):
        # Show all categories
        response = "# 🎓 Complete List of Colleges in Solapur\n\n"
        response += f"**Total Colleges:** {st.session_state.colleges_data.get('total_colleges', 'N/A')}\n\n"
        
        for cat_key, cat_data in categories.items():
            response += format_category_colleges(cat_data['name'], cat_data['colleges'])
        
        return response
    
    # University queries
    elif any(word in query_lower for word in ['university', 'universities']):
        if 'universities' in categories:
            response = "# 🏛️ Universities in Solapur\n\n"
            response += format_category_colleges(
                categories['universities']['name'],
                categories['universities']['colleges']
            )
        return response
    
    # Engineering queries
    elif any(word in query_lower for word in ['engineering', 'b.tech', 'btech', 'polytechnic']):
        if 'engineering' in categories:
            response = "# ⚙️ Engineering Colleges in Solapur\n\n"
            response += format_category_colleges(
                categories['engineering']['name'],
                categories['engineering']['colleges']
            )
        return response
    
    # Medical queries
    elif any(word in query_lower for word in ['medical', 'mbbs', 'doctor', 'health', 'nursing', 'dental']):
        if 'medical' in categories:
            response = "# 🏥 Medical & Health Colleges in Solapur\n\n"
            response += format_category_colleges(
                categories['medical']['name'],
                categories['medical']['colleges']
            )
        return response
    
    # Commerce/Management queries
    elif any(word in query_lower for word in ['commerce', 'management', 'mba', 'bba', 'b.com', 'bcom']):
        if 'commerce_management' in categories:
            response = "# 💼 Commerce / Management Colleges in Solapur\n\n"
            response += format_category_colleges(
                categories['commerce_management']['name'],
                categories['commerce_management']['colleges']
            )
        return response
    
    # Arts/Science queries
    elif any(word in query_lower for word in ['arts', 'science', 'b.a', 'b.sc', 'bsc']):
        if 'arts_science' in categories:
            response = "# 📚 Arts / Science Colleges in Solapur\n\n"
            response += format_category_colleges(
                categories['arts_science']['name'],
                categories['arts_science']['colleges']
            )
        return response
    
    # Other colleges
    elif any(word in query_lower for word in ['other', 'pharmacy', 'law', 'hotel']):
        if 'other' in categories:
            response = "# 🏫 Other Colleges in Solapur\n\n"
            response += format_category_colleges(
                categories['other']['name'],
                categories['other']['colleges']
            )
        return response
    
    # Specific college search
    else:
        # Search for specific college name
        found_colleges = []
        for cat_key, cat_data in categories.items():
            for college in cat_data['colleges']:
                if query_lower in college['name'].lower() or query_lower in college.get('short_name', '').lower():
                    found_colleges.append((cat_data['name'], college))
        
        if found_colleges:
            response = f"# 🔍 Search Results for '{query}'\n\n"
            for cat_name, college in found_colleges:
                response += f"**{college['name']}**\n"
                response += f"Category: {cat_name}\n"
                if 'type' in college:
                    response += f"Type: {college['type']}\n"
                if 'location' in college:
                    response += f"Location: {college['location']}\n"
                if 'contact' in college:
                    response += f"Contact: {college['contact']}\n"
                if 'website' in college:
                    response += f"Website: {college['website']}\n"
                if 'description' in college:
                    response += f"\n{college['description']}\n"
                response += "\n---\n\n"
            return response
        else:
            return """I couldn't find specific information about that. 

You can ask me about:
• **All colleges** - "List all colleges in Solapur"
• **Universities** - "Show universities"
• **Engineering** - "Engineering colleges"
• **Medical** - "Medical colleges"
• **Commerce** - "Commerce colleges"
• **Arts/Science** - "Arts and Science colleges"
• **Specific college** - "Tell me about WIT" """

# Header
header_col1, header_col2 = st.columns([6, 1])

with header_col1:
    st.markdown("""
    <div class="main-header">
        <h1>🎓 Solapur Colleges Directory</h1>
        <p>Complete Guide to 35+ Colleges in Solapur</p>
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
    st.markdown("### 📋 Categories")
    
    categories = [
        ("🏛️ Universities", "universities"),
        ("⚙️ Engineering", "engineering colleges"),
        ("🏥 Medical & Health", "medical colleges"),
        ("💼 Commerce / Management", "commerce colleges"),
        ("📚 Arts / Science", "arts colleges"),
        ("🏫 Other Colleges", "other colleges"),
        ("📊 All Colleges", "all colleges")
    ]
    
    for icon_name, query in categories:
        if st.button(icon_name, key=f"cat_{query}", use_container_width=True):
            st.session_state.quick_query = query
    
    st.markdown("---")
    st.markdown("### 📊 Statistics")
    st.metric("Total Colleges", "35+")
    st.metric("Categories", "6")
    st.metric("City", "Solapur")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    if not st.session_state.messages:
        st.markdown("""
        ### 👋 Welcome to Solapur Colleges Directory!
        
        I can help you find information about colleges in Solapur city.
        
        **Ask me about:**
        - 🏛️ Universities in Solapur
        - ⚙️ Engineering Colleges
        - 🏥 Medical & Health Colleges
        - 💼 Commerce / Management Colleges
        - 📚 Arts / Science Colleges
        - 🏫 Other Colleges
        
        **Try these questions:**
        - "List all colleges in Solapur"
        - "Show me engineering colleges"
        - "Tell me about WIT"
        - "Medical colleges in Solapur"
        """)
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

with col2:
    st.markdown("### 🎯 Quick Stats")
    
    categories_data = st.session_state.colleges_data.get('categories', {})
    
    if 'universities' in categories_data:
        st.info(f"**Universities:** {len(categories_data['universities']['colleges'])}")
    if 'engineering' in categories_data:
        st.info(f"**Engineering:** {len(categories_data['engineering']['colleges'])}")
    if 'medical' in categories_data:
        st.info(f"**Medical:** {len(categories_data['medical']['colleges'])}")
    if 'commerce_management' in categories_data:
        st.info(f"**Commerce:** {len(categories_data['commerce_management']['colleges'])}")
    if 'arts_science' in categories_data:
        st.info(f"**Arts/Science:** {len(categories_data['arts_science']['colleges'])}")
    if 'other' in categories_data:
        st.info(f"**Others:** {len(categories_data['other']['colleges'])}")

# Chat input
if "quick_query" in st.session_state:
    prompt = st.session_state.quick_query
    del st.session_state.quick_query
else:
    prompt = st.chat_input("Ask about colleges in Solapur...")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get response
    response = search_colleges(prompt)
    
    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: var(--text-secondary); padding: 1rem;'>
    <p>🎓 Solapur Colleges Directory | Complete Information about 35+ Colleges</p>
    <p>Data sourced from official college websites and verified sources</p>
</div>
""", unsafe_allow_html=True)
