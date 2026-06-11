import streamlit as st
import json
import time
from datetime import datetime
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os

# Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="Solapur Colleges Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Performance Optimization: Load data once using @st.cache_resource
@st.cache_resource
def load_rag_system():
    """Load and cache RAG system for answering detailed questions"""
    try:
        # Check if vector store exists
        if not os.path.exists("db"):
            return None, None
        
        # Load embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Load vector store
        vectorstore = Chroma(
            persist_directory="db",
            embedding_function=embeddings
        )
        
        # Create LLM
        llm = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.2",
            temperature=0.7,
            max_new_tokens=512,
            huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_TOKEN", "")
        )
        
        # Create prompt template
        prompt_template = """You are a helpful assistant for Solapur colleges. Use the following context to answer the question.
If you don't know the answer, say "I don't have that information in the handbook."

Context: {context}

Question: {question}

Answer: """
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        return qa_chain, vectorstore
    except Exception as e:
        print(f"Error loading RAG system: {e}")
        return None, None

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
qa_chain, vectorstore = load_rag_system()

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
    
    /* Animations */
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Timestamp */
    .timestamp {
        font-size: 0.7rem;
        color: #999;
        margin-top: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

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

def is_detailed_question(query):
    """Check if query is asking for detailed information from handbook"""
    detailed_keywords = [
        'admission', 'fees', 'placement', 'eligibility', 'criteria', 'process',
        'requirement', 'facility', 'hostel', 'scholarship', 'exam', 'syllabus',
        'faculty', 'department', 'course', 'duration', 'how to', 'what is',
        'when', 'where', 'why', 'explain', 'describe', 'tell me about',
        'information about', 'details', 'rules', 'regulations', 'timings'
    ]
    
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in detailed_keywords)

def generate_response(query):
    """Generate response using college database or RAG system"""
    
    # First, check if asking about specific college
    college = find_college_fast(query)
    
    # If detailed question and RAG is available, use RAG
    if is_detailed_question(query) and qa_chain is not None:
        try:
            # If asking about specific college, add context
            if college:
                enhanced_query = f"Question about {college['name']}: {query}"
            else:
                enhanced_query = query
            
            result = qa_chain.invoke({"query": enhanced_query})
            answer = result.get('result', '').strip()
            
            if answer and "don't have that information" not in answer.lower():
                return {
                    'type': 'rag_answer',
                    'text': answer,
                    'college': college
                }
        except Exception as e:
            print(f"RAG error: {e}")
    
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
    
    # If RAG available, try to answer
    if qa_chain is not None:
        try:
            result = qa_chain.invoke({"query": query})
            answer = result.get('result', '').strip()
            if answer:
                return {
                    'type': 'rag_answer',
                    'text': answer
                }
        except:
            pass
    
    # Default response
    return {
        'type': 'help',
        'text': "I couldn't understand that. You can ask about:\n• Specific colleges (e.g., 'Tell me about WIT')\n• College categories (e.g., 'Engineering colleges')\n• Detailed questions (e.g., 'What are the admission requirements?', 'Tell me about fees')"
    }

# Header
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 2rem; border-radius: 15px; text-align: center; color: white; 
            box-shadow: 0 8px 16px rgba(0,0,0,0.2); margin-bottom: 2rem;'>
    <h1 style='margin: 0; font-size: 2.5rem;'>🎓 Solapur Colleges Chatbot</h1>
    <p style='margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;'>
        AI-Powered Assistant - Ask anything about colleges!
    </p>
</div>
""", unsafe_allow_html=True)

# Show RAG status
if qa_chain is None:
    st.warning("⚠️ RAG system not loaded. Run `python ingest.py` first to enable detailed Q&A. Currently showing college database only.")

# Sidebar with chat history and quick actions
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
    rag_status = "✅ Active" if qa_chain else "❌ Inactive"
    st.metric("RAG System", rag_status)
    
    st.markdown("---")
    st.markdown("### 🔍 Search")
    search_input = st.text_input("Search college name", key="search_input")
    if search_input:
        st.session_state.quick_query = f"Tell me about {search_input}"
        st.rerun()

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
        with st.spinner("🤔 Thinking..."):
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
        elif response['type'] == 'rag_answer' and response.get('college'):
            bot_msg["college_card"] = display_college_card(response['college'])
        
        st.session_state.messages.append(bot_msg)
        st.rerun()

with col2:
    st.markdown("### 💡 Suggested Questions")
    
    suggestions = [
        "Tell me about WIT",
        "Engineering colleges",
        "Admission process",
        "What are the fees?",
        "Placement information",
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
    <p>🎓 Solapur Colleges Chatbot | AI-Powered Q&A | 35+ Colleges</p>
    <p>Ask about admissions, fees, placements, facilities, and more!</p>
</div>
""", unsafe_allow_html=True)
