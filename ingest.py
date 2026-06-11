from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv
import warnings

# Suppress Pydantic warnings
warnings.filterwarnings('ignore', category=UserWarning)

load_dotenv()

def ingest_documents():
    try:
        print("Starting document ingestion...")
        
        # Try to load PDF first, if not found, load text file
        if os.path.exists("data/Wit handbook.pdf"):
            print("Loading PDF file: data/Wit handbook.pdf")
            loader = PyPDFLoader("data/Wit handbook.pdf")
            documents = loader.load()
            print(f"Loaded {len(documents)} pages from PDF")
        elif os.path.exists("data/handbook.txt"):
            print("Loading text file: data/handbook.txt")
            loader = TextLoader("data/handbook.txt")
            documents = loader.load()
            print(f"Loaded text file")
        else:
            print("No handbook file found! Please add handbook PDF or TXT to data folder.")
            return
    except Exception as e:
        print(f"Error loading documents: {e}")
        return
    
    try:
        print("Splitting documents into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        docs = text_splitter.split_documents(documents)
        print(f"Created {len(docs)} chunks")
        
        print("Loading embeddings model...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        print("Creating vector store...")
        vectorstore = Chroma.from_documents(
            docs,
            embeddings,
            persist_directory="db"
        )
        print("✓ Documents Ingested Successfully!")
        print(f"✓ Total chunks created: {len(docs)}")
        print(f"✓ Vector store saved to: db/")
    except Exception as e:
        print(f"Error during ingestion: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    ingest_documents()
