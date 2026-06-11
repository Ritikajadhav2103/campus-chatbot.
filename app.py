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

# Try to import and initialize
@st.cache_resource
def load_chatbot(_api_key):
    try:
        from langchain_community.vectorstores import Chroma
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_community.llms import HuggingFaceHub
        from langchain.chains import RetrievalQA
        from langchain.prompts import PromptTemplate
        
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = Chroma(persist_directory="./db", embedding_function=embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
        
        llm = HuggingFaceHub(
            repo_id="google/flan-t5-large",
            model_kwargs={"temperature": 0.5, "max_length": 512}
        )
        
        template = """You are a helpful campus assistant for Walchand Institute of Technology.
        Use the context to answer the question. If you don't know, say so.
        
        Context: {context}
        Question: {question}
        Answer:"""
        prompt = PromptTemplate(template=template, input_variables=["context", "question"])
        
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
        return qa, None
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
            with st.spinner("Searching..."):
                qa, error = load_chatbot(api_key)
                if error:
                    response = f"Error loading chatbot: {error}"
                    st.error(response)
                elif qa:
                    try:
                        result = qa({"query": prompt})
                        response = result['result']
                        st.markdown(response)
                    except Exception as e:
                        response = f"Error: {str(e)}"
                        st.error(response)
                else:
                    response = "Chatbot not initialized"
                    st.error(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
