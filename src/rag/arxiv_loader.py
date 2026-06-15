import arxiv
from langchain_core.documents import Document


def search_arxiv_papers(query: str, max_results: int = 5) -> list[Document]:
    """
    Busca papers en arXiv y los devuelve como documentos de LangChain.

    Args:
        query: Término de búsqueda
        max_results: Número máximo de papers a recuperar

    Returns:
        Lista de Documents con el contenido y metadatos de cada paper
    """
    client = arxiv.Client()

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    documents = []

    for paper in client.results(search):
        content = f"""
Título: {paper.title}

Resumen: {paper.summary}

Autores: {', '.join(str(a) for a in paper.authors)}
Publicado: {paper.published.strftime('%Y-%m-%d')}
"""
        doc = Document(
            page_content=content,
            metadata={
                "title": paper.title,
                "url": paper.entry_id,
                "published": paper.published.strftime('%Y-%m-%d'),
            }
        )
        documents.append(doc)

    return documents