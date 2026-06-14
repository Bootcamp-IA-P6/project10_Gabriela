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

    Args:
        topic: Tema del contenido
        platform: Plataforma (blog, twitter, instagram, linkedin)
        audience: Audiencia objetivo

    Returns:
        Diccionario con el contenido generado y las fuentes usadas
    """

    # Paso 1 — Buscar papers en arXiv
    print(f"🔍 Buscando papers sobre: {topic}")
    documents = search_arxiv_papers(query=topic, max_results=5)

    if not documents:
        return {
            "content": generate_content(topic, platform, audience),
            "sources": [],
            "used_rag": False,
        }

    # Paso 2 — Crear vector store con los papers
    print(f"📚 Indexando {len(documents)} papers...")
    vector_store = create_vector_store(documents)
    retriever = get_retriever(vector_store, k=3)

    # Paso 3 — Recuperar los más relevantes para el tema
    relevant_docs = retriever.invoke(topic)

    # Paso 4 — Construir contexto con los papers recuperados
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    # Paso 5 — Generar contenido enriquecido
    print("✍️ Generando contenido con contexto científico...")
    content = generate_content(topic, platform, audience, context=context)

    # Fuentes usadas
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