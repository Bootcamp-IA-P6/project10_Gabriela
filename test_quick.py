from dotenv import load_dotenv
load_dotenv()

# Test 1 — Groq conecta?
from src.generators.content_generator import generate_content
print("🧪 Probando generador...")
result = generate_content(
    topic="inteligencia artificial",
    platform="twitter",
    audience="público general"
)
print(result)
print("✅ Generador OK\n")

# Test 2 — arXiv funciona?
from src.rag.arxiv_loader import search_arxiv_papers
print("🧪 Probando arXiv...")
papers = search_arxiv_papers("artificial intelligence", max_results=2)
print(f"Papers encontrados: {len(papers)}")
print(f"Primer paper: {papers[0].metadata['title']}")
print("✅ arXiv OK\n")

# Test 3 — Vector store funciona?
from src.rag.vector_store import create_vector_store, get_retriever
print("🧪 Probando ChromaDB...")
vs = create_vector_store(papers)
retriever = get_retriever(vs)
docs = retriever.invoke("artificial intelligence")
print(f"Documentos recuperados: {len(docs)}")
print("✅ ChromaDB OK")