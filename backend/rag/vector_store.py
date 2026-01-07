from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

PERSIST_DIRECTORY = "dbv1/chroma_db"

def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def create_vector_store(documents):
    """Create and persist ChromaDB vector store"""
    print(" Creating embeddings and storing in ChromaDB...")

    embedding_model = get_embedding_model()

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=PERSIST_DIRECTORY,
        collection_metadata={"hnsw:space": "cosine"}
    )

    print(f" Vector store created and saved to {PERSIST_DIRECTORY}")
    return vectorstore


def get_vector_store():
    """Load existing ChromaDB vector store from disk"""
    print("Loading vector store from disk...")

    embedding_model = get_embedding_model()

    vectorstore = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_model
    )

    return vectorstore
