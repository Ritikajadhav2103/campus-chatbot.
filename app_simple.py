import streamlit as st
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Campus Info Chatbot", page_icon="🎓")
st.title("🎓 Campus Info Chatbot")
st.markdown("### Walchand Institute of Technology, Solapur")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("Configuration")
    st.markdown("[Get HuggingFace Token](https://huggingface.co/settings/tokens)")
    api_key = st.text_input("HuggingFace API Token", type="password")
    
    if api_key:
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = api_key
        st.success("✓ Token configured!")
    
    st.markdown("---")
    st.info("Ask questions about WIT Solapur campus")
    
    st.markdown("### Sample Questions")
    st.markdown("""
    - What is the attendance policy?
    - Tell me about placements
    - What are the hostel fees?
    - How do I join clubs?
    - Where is the library?
    """)

# Simple Q&A without complex chains
@st.cache_resource
def load_vectorstore():
    try:
        from langchain_community.vectorstores import Chroma
        from langchain_huggingface import HuggingFaceEmbeddings
        
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = Chroma(persist_directory="./db", embedding_function=embeddings)
        return vectorstore, None
    except Exception as e:
        return None, str(e)

def get_llm_response(context, question, api_key):
    try:
        from langchain_community.llms import HuggingFaceHub
        
        llm = HuggingFaceHub(
            repo_id="google/flan-t5-large",
            model_kwargs={"temperature": 0.5, "max_length": 512},
            huggingfacehub_api_token=api_key
        )
        
        prompt = f"""You are a helpful campus assistant for Walchand Institute of Technology.
Use the context below to answer the question. If you don't know, say so.

Context: {context}

Question: {question}

Answer:"""
        
        response = llm(prompt)
        return response, None
    except Exception as e:
        return None, str(e)

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask about campus..."):
    if not api_key:
        st.error("⚠️ Enter your HuggingFace token in the sidebar")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Searching campus documents..."):
                vectorstore, error = load_vectorstore()
                
                if error:
                    response = f"Error loading database: {error}"
                    st.error(response)
                elif vectorstore:
                    try:
                        # Search for relevant documents
                        docs = vectorstore.similarity_search(prompt, k=3)
                        context = "\n\n".join([doc.page_content for doc in docs])
                        
                        # Get LLM response
                        response, error = get_llm_response(context, prompt, api_key)
                        
                        if error:
                            response = f"Error getting response: {error}"
                            st.error(response)
                        else:
                            st.markdown(response)
                            
                            # Show sources
                            with st.expander("📚 View Sources"):
                                for i, doc in enumerate(docs):
                                    st.markdown(f"**Source {i+1}:**")
                                    st.text(doc.page_content[:300] + "...")
                    except Exception as e:
                        response = f"Error: {str(e)}"
                        st.error(response)
                else:
                    response = "Database not loaded"
                    st.error(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
