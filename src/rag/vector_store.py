from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

_embeddings = None


def get_embeddings():
    """
    Carga el modelo de embeddings solo la primera vez (lazy loading).
    Las siguientes llamadas reutilizan el modelo ya cargado.
    """
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    return _embeddings


def create_vector_store(documents: list[Document]) -> Chroma:
    """Crea un vector store en memoria con los documentos dados."""
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=get_embeddings(),
    )
    return vector_store


def get_retriever(vector_store: Chroma, k: int = 3):
    """Devuelve un retriever que busca los k documentos más relevantes."""
    return vector_store.as_retriever(search_kwargs={"k": k})