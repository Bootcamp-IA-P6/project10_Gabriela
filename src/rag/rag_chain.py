from src.rag.arxiv_loader import search_arxiv_papers
from src.rag.vector_store import create_vector_store, get_retriever
from src.generators.content_generator import generate_content


def run_rag_pipeline(
    topic: str,
    platform: str,
    audience: str,
    model: str = "llama-3.1-8b-instant",
    language: str = "Español",
    brand_info: str = "",
) -> dict:
    """
    Pipeline RAG completo:
    1. Busca papers en arXiv sobre el tema
    2. Los indexa en ChromaDB
    3. Recupera los más relevantes
    4. Genera contenido enriquecido con ese contexto
    """
    print(f"🔍 Buscando papers sobre: {topic}")
    documents = search_arxiv_papers(query=topic, max_results=3)

    if not documents:
        return {
            "content": generate_content(topic, platform, audience, model=model, language=language, brand_info=brand_info),
            "sources": [],
            "used_rag": False,
        }

    print(f"📚 Indexando {len(documents)} papers...")
    vector_store = create_vector_store(documents)
    retriever = get_retriever(vector_store, k=2)
    relevant_docs = retriever.invoke(topic)

    context_parts = [doc.page_content[:800] for doc in relevant_docs]
    context = "\n\n".join(context_parts)

    print("✍️ Generando contenido con contexto científico...")
    content = generate_content(
        topic, platform, audience,
        context=context,
        model=model,
        language=language,
        brand_info=brand_info,
    )

    sources = [
        {
            "title": doc.metadata.get("title", "Sin título"),
            "url": doc.metadata.get("url", ""),
            "published": doc.metadata.get("published", ""),
        }
        for doc in relevant_docs
    ]

    return {"content": content, "sources": sources, "used_rag": True}