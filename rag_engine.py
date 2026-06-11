from langchain.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceHub
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv

load_dotenv()

def load_qa_chain():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    vectorstore = Chroma(
        persist_directory="db",
        embedding_function=embeddings
    )
    
    retriever = vectorstore.as_retriever()
    
    llm = HuggingFaceHub(
        repo_id="google/flan-t5-base",
        model_kwargs={"temperature": 0.5, "max_length": 512}
    )
    
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever
    )
    
    return qa
