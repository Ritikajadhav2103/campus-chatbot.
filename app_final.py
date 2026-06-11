import streamlit as st
import os

st.set_page_config(page_title="Campus Info Chatbot", page_icon="🎓")
st.title("🎓 Campus Info Chatbot")
st.markdown("### Walchand Institute of Technology, Solapur")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "handbook" not in st.session_state:
    try:
        with open("data/handbook.txt", "r", encoding="utf-8") as f:
            st.session_state.handbook = f.read()
    except:
        st.session_state.handbook = ""

# Sidebar
with st.sidebar:
    st.header("📚 Campus Information System")
    st.info("Official Campus Information Assistant for Walchand Institute of Technology, Solapur")
    
    st.markdown("---")
    st.markdown("### 💡 Sample Questions")
    st.markdown("""
    - What is the attendance policy?
    - Tell me about placements
    - What are the hostel fees?
    - How do I join clubs?
    - Where is the library?
    - What is the fee structure?
    - Tell me about CBCS system
    - What is the grading system?
    - Who is the principal?
    """)
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.caption("This AI assistant provides accurate information strictly from official campus documents. If information is not available, you'll be directed to contact the college office.")

def search_handbook(query):
    """Fast and accurate search for relevant information"""
    query_lower = query.lower()
    full_text = st.session_state.handbook
    
    # Define search patterns for different topics
    search_patterns = {
        'club': ['7. CLUBS AND SOCIETIES', 'clubs and societies', 'registration process:', 'technical clubs:', 'cultural clubs:'],
        'join': ['registration', 'membership', 'coordinator:', 'eligibility:'],
        'fee': ['5. FEE STRUCTURE', 'annual tuition fee:', 'payment schedule:', 'fee structure (2024-25)'],
        'attendance': ['3. ATTENDANCE POLICY', 'minimum attendance', '75% attendance', 'condonation'],
        'placement': ['6. PLACEMENT CELL', 'training and placement', 'average package:', 'eligibility criteria'],
        'hostel': ['hostel facilities:', 'hostel fee:', 'boys hostel:', 'girls hostel:'],
        'library': ['library:', 'location: central building', 'timing:', 'books:'],
        'exam': ['4. EXAMINATION SYSTEM', 'internal assessment', 'external examination'],
        'grade': ['grading system:', 'sgpa', 'cgpa', 'grade points'],
        'cbcs': ['2. ACADEMIC REGULATIONS (CBCS SYSTEM)', 'choice based credit system', 'credit structure:'],
    }
    
    # Find which topic matches the query
    relevant_patterns = []
    for topic, patterns in search_patterns.items():
        if topic in query_lower:
            relevant_patterns.extend(patterns)
    
    # If no specific topic, use all query words
    if not relevant_patterns:
        relevant_patterns = [word for word in query_lower.split() if len(word) > 3]
    
    # Search for sections containing these patterns
    sections = full_text.split('=' * 80)
    best_section = None
    best_score = 0
    
    for section in sections:
        if len(section.strip()) < 100:
            continue
        
        section_lower = section.lower()
        
        # Skip table of contents
        if 'table of contents' in section_lower[:300]:
            continue
        
        # Calculate score based on pattern matches
        score = sum(10 for pattern in relevant_patterns if pattern in section_lower)
        
        if score > best_score:
            best_score = score
            best_section = section
    
    return [best_section.strip()] if best_section and best_score >= 10 else []

def format_answer(query, sections):
    """Format a professional, complete answer following campus assistant guidelines"""
    if not sections:
        return """❌ **Information Not Available**

This information is not available in the current campus database. 

Please contact:
• **College Office**: 0217-2320567
• **Email**: principal@witsolapur.org
• **Student Section**: 0217-2320573

You can also try asking about:
• Attendance policy • Fee structure • Placement details
• Clubs and societies • Hostel facilities • Library information
• Exam system • Grading system"""
    
    section = sections[0]
    lines = [l.strip() for l in section.split('\n') if l.strip()]
    
    # Extract meaningful content
    content_lines = []
    found_content = False
    
    for line in lines:
        # Skip separators
        if '=' * 10 in line:
            continue
        
        # Skip very short lines
        if len(line) < 3:
            continue
        
        # Skip section headers (all caps with numbers)
        if line[:2].replace('.', '').replace(' ', '').isdigit() and line.isupper():
            found_content = True
            continue
        
        # Collect content after header
        if found_content and len(line) > 10:
            content_lines.append(line)
    
    if not content_lines:
        # Fallback: take all non-empty lines
        content_lines = [l for l in lines if len(l) > 15 and '=' not in l]
    
    # Format the answer
    answer = "📖 **Official Information from WIT Handbook:**\n\n"
    
    # Add content
    for line in content_lines[:25]:
        answer += line + "\n\n"
    
    # Add footer
    answer += "\n---\n*Source: Official WIT Student Handbook 2024-25*"
    
    return answer

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask about campus..."):
    if not st.session_state.handbook:
        st.error("⚠️ Handbook not loaded. Please check data/handbook.txt exists")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching handbook..."):
                # Search for relevant content
                sections = search_handbook(prompt)
                response = format_answer(prompt, sections)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

# Show handbook status
if st.session_state.handbook:
    st.sidebar.success(f"✅ Handbook loaded ({len(st.session_state.handbook):,} characters)")
else:
    st.sidebar.error("❌ Handbook not loaded")
