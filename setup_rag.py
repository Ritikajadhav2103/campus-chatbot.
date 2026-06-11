"""
Setup script to ingest handbook data for RAG system
"""
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

def setup_rag():
    print("=" * 60)
    print("SOLAPUR COLLEGES CHATBOT - RAG SETUP")
    print("=" * 60)
    
    # Check if handbook exists
    handbook_path = "data/solapur_colleges_handbook.txt"
    if not os.path.exists(handbook_path):
        print(f"❌ Error: {handbook_path} not found!")
        print("Please make sure the handbook file exists.")
        return False
    
    print(f"✓ Found handbook: {handbook_path}")
    
    try:
        # Load handbook
        print("\n📖 Loading handbook...")
        loader = TextLoader(handbook_path, encoding='utf-8')
        documents = loader.load()
        print(f"✓ Loaded {len(documents)} document(s)")
        
        # Split into chunks
        print("\n✂️ Splitting into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        chunks = text_splitter.split_documents(documents)
        print(f"✓ Created {len(chunks)} chunks")
        
        # Load embeddings model
        print("\n🧠 Loading embeddings model...")
        print("   (This may take a minute on first run)")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        print("✓ Embeddings model loaded")
        
        # Create vector store
        print("\n💾 Creating vector store...")
        if os.path.exists("db"):
            print("   Removing old vector store...")
            import shutil
            shutil.rmtree("db")
        
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory="db"
        )
        print("✓ Vector store created and saved to 'db/' folder")
        
        # Test the vector store
        print("\n🧪 Testing vector store...")
        test_query = "What are the engineering colleges?"
        results = vectorstore.similarity_search(test_query, k=2)
        print(f"✓ Test query successful! Found {len(results)} relevant chunks")
        
        print("\n" + "=" * 60)
        print("✅ RAG SETUP COMPLETE!")
        print("=" * 60)
        print("\nYou can now run the chatbot:")
        print("  python -m streamlit run app_solapur_rag.py")
        print("\nThe chatbot will now be able to answer detailed questions like:")
        print("  • What are the admission requirements?")
        print("  • Tell me about fees at WIT")
        print("  • What facilities are available?")
        print("  • Placement information")
        print("  • Hostel details")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    setup_rag()
