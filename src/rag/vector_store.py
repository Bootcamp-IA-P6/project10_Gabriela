from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Embeddings locales y gratuitos — no necesita API key
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def create_vector_store(documents: list[Document]) -> Chroma:
    """
    Crea un vector store en memoria con los documentos dados.

    Args:
        documents: Lista de documentos de LangChain

    Returns:
        Vector store de ChromaDB listo para buscar
    """
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
    )
    return vector_store


def get_retriever(vector_store: Chroma, k: int = 3):
    """
    Devuelve un retriever que busca los k documentos más relevantes.

    Args:
        vector_store: El vector store de ChromaDB
        k: Número de documentos a recuperar

    Returns:
        Retriever listo para usar en la cadena RAG
    """
    return vector_store.as_retriever(search_kwargs={"k": k})