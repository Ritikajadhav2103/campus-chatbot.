"""
Simple ingestion script - Run this if ingest.py fails due to Python version issues
"""
import os

print("=" * 60)
print("CAMPUS INFO CHATBOT - DOCUMENT INGESTION")
print("=" * 60)

# Check Python version
import sys
print(f"\nPython Version: {sys.version}")

if sys.version_info >= (3, 14):
    print("\n⚠️  WARNING: Python 3.14 detected!")
    print("LangChain currently supports Python 3.9-3.12")
    print("\nRecommended actions:")
    print("1. Install Python 3.11 or 3.12")
    print("2. Create a virtual environment with compatible Python:")
    print("   py -3.11 -m venv venv")
    print("   .\\venv\\Scripts\\activate")
    print("   pip install -r requirements.txt")
    print("\nExiting...")
    sys.exit(1)

# If Python version is OK, proceed with ingestion
try:
    from langchain_community.document_loaders import PyPDFLoader, TextLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import Chroma
    from langchain_huggingface import HuggingFaceEmbeddings
    
    print("\n✓ All imports successful")
    print("\nStarting document ingestion...")
    
    # Load documents
    if os.path.exists("data/Wit handbook.pdf"):
        print("Loading: data/Wit handbook.pdf")
        loader = PyPDFLoader("data/Wit handbook.pdf")
        documents = loader.load()
        print(f"✓ Loaded {len(documents)} pages")
    elif os.path.exists("data/handbook.txt"):
        print("Loading: data/handbook.txt")
        loader = TextLoader("data/handbook.txt", encoding='utf-8')
        documents = loader.load()
        print(f"✓ Loaded text file")
    else:
        print("\n❌ No handbook found!")
        print("Please add one of these files:")
        print("  - data/Wit handbook.pdf")
        print("  - data/handbook.txt")
        sys.exit(1)
    
    # Split into chunks
    print("\nSplitting into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    docs = text_splitter.split_documents(documents)
    print(f"✓ Created {len(docs)} chunks")
    
    # Create embeddings
    print("\nLoading embedding model (this may take a minute)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    print("✓ Embeddings model loaded")
    
    # Create vector store
    print("\nCreating vector database...")
    vectorstore = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory="db"
    )
    print("✓ Vector database created")
    
    print("\n" + "=" * 60)
    print("✓ INGESTION COMPLETE!")
    print("=" * 60)
    print(f"Total chunks: {len(docs)}")
    print(f"Database location: db/")
    print("\nYou can now run: streamlit run app.py")
    
except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("\nPlease install dependencies:")
    print("pip install -r requirements.txt")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
