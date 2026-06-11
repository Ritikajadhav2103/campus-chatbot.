import streamlit as st
import os

st.set_page_config(page_title="Campus Info Chatbot", page_icon="🎓")
st.title("🎓 Campus Info Chatbot")
st.markdown("### Walchand Institute of Technology, Solapur")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "handbook" not in st.session_state:
    # Load handbook
    try:
        with open("data/handbook.txt", "r", encoding="utf-8") as f:
            st.session_state.handbook = f.read()
    except:
        st.session_state.handbook = ""

# Sidebar
with st.sidebar:
    st.header("Configuration")
    st.markdown("[Get HuggingFace Token](https://huggingface.co/settings/tokens)")
    api_key = st.text_input("HuggingFace API Token", type="password")
    
    if api_key:
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = api_key
        st.success("✓ Token configured!")
    
    st.markdown("---")
    st.markdown("### Sample Questions")
    st.markdown("""
    - What is the attendance policy?
    - Tell me about placements
    - What are the hostel fees?
    - How do I join clubs?
    - Where is the library?
    - What is the fee structure?
    - Tell me about CBCS system
    """)

def search_handbook(query):
    """Simple keyword search in handbook"""
    query_lower = query.lower()
    lines = st.session_state.handbook.split('\n')
    
    relevant_sections = []
    current_section = []
    
    for i, line in enumerate(lines):
        # Check if line contains query keywords
        if any(word in line.lower() for word in query_lower.split()):
            # Get context (5 lines before and after)
            start = max(0, i - 5)
            end = min(len(lines), i + 6)
            section = '\n'.join(lines[start:end])
            if section not in relevant_sections:
                relevant_sections.append(section)
    
    return '\n\n---\n\n'.join(relevant_sections[:3]) if relevant_sections else ""

def get_answer(query, context, api_key):
    """Get answer from HuggingFace"""
    try:
        import requests
        
        # Using a different model that's actively maintained
        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        prompt = f"""Answer this question about Walchand Institute of Technology based on the context provided. Keep the answer concise.

Context: {context[:1000]}

Question: {query}

Answer:"""
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.5,
                "return_full_text": False
            }
        }
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', str(result))
            elif isinstance(result, dict):
                return result.get('generated_text', str(result))
            return str(result)
        elif response.status_code == 503:
            return "Model is loading, please wait 20 seconds and try again."
        elif response.status_code == 401:
            return "Invalid API token. Please check your HuggingFace token."
        else:
            return f"API Error {response.status_code}. Try a different question or wait a moment."
            
    except Exception as e:
        return f"Error: {str(e)}"

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask about campus..."):
    if not api_key:
        st.error("⚠️ Enter your HuggingFace token in the sidebar")
    elif not st.session_state.handbook:
        st.error("⚠️ Handbook not loaded. Please check data/handbook.txt exists")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Searching handbook..."):
                # Search for relevant content
                context = search_handbook(prompt)
                
                if context:
                    # Get AI response
                    response = get_answer(prompt, context, api_key)
                    st.markdown(response)
                    
                    # Show source
                    with st.expander("📚 View Source"):
                        st.text(context[:500] + "...")
                else:
                    response = "I couldn't find relevant information in the handbook. Please try rephrasing your question."
                    st.warning(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

# Show handbook status
if st.session_state.handbook:
    st.sidebar.success(f"✓ Handbook loaded ({len(st.session_state.handbook)} characters)")
else:
    st.sidebar.error("✗ Handbook not loaded")
