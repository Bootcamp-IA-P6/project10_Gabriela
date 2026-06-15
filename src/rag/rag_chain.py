from src.rag.arxiv_loader import search_arxiv_papers
from src.rag.vector_store import create_vector_store, get_retriever
from src.generators.content_generator import generate_content


def run_rag_pipeline(topic: str, platform: str, audience: str) -> dict:
    """
    Pipeline RAG completo:
    1. Busca papers en arXiv sobre el tema
    2. Los guarda en ChromaDB
    3. Recupera los más relevantes
    4. Genera contenido enriquecido con ese contexto
    """

    print(f"🔍 Buscando papers sobre: {topic}")
    documents = search_arxiv_papers(query=topic, max_results=3)

    if not documents:
        return {
            "content": generate_content(topic, platform, audience),
            "sources": [],
            "used_rag": False,
        }

    print(f"📚 Indexando {len(documents)} papers...")
    vector_store = create_vector_store(documents)
    retriever = get_retriever(vector_store, k=2)

    relevant_docs = retriever.invoke(topic)

    # Recortamos cada paper a 800 caracteres para no pasarnos
    # del límite de tokens del tier gratuito de Groq (6000 TPM)
    context_parts = []
    for doc in relevant_docs:
        recorte = doc.page_content[:800]
        context_parts.append(recorte)

    context = "\n\n".join(context_parts)

    print("✍️ Generando contenido con contexto científico...")
    content = generate_content(topic, platform, audience, context=context)

    sources = [
        {
            "title": doc.metadata.get("title", "Sin título"),
            "url": doc.metadata.get("url", ""),
            "published": doc.metadata.get("published", ""),
        }
        for doc in relevant_docs
    ]

    return {
        "content": content,
        "sources": sources,
        "used_rag": True,
    }