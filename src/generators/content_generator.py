from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

AVAILABLE_MODELS = {
    "llama-3.1-8b-instant": "Llama 3.1 8B (rápido)",
    "llama-3.3-70b-versatile": "Llama 3.3 70B (más potente)",
}

PLATFORM_PROMPTS = {
    "blog": """Eres un escritor experto en blogs.
Escribe un artículo de blog completo sobre: {topic}
Audiencia: {audience}
Contexto adicional: {context}
{brand_context}
Idioma: {language}

El artículo debe tener introducción, desarrollo y conclusión.
Usa un tono cercano y profesional.""",

    "twitter": """Eres un experto en Twitter/X.
Crea un hilo de 5 tweets sobre: {topic}
Audiencia: {audience}
Contexto adicional: {context}
{brand_context}
Idioma: {language}

Cada tweet debe empezar con su número (1/, 2/, etc).
Máximo 280 caracteres por tweet. Usa hashtags relevantes.""",

    "instagram": """Eres un experto en Instagram.
Crea una caption para Instagram sobre: {topic}
Audiencia: {audience}
Contexto adicional: {context}
{brand_context}
Idioma: {language}

Incluye emojis, llamada a la acción y hashtags al final.""",

    "linkedin": """Eres un experto en LinkedIn.
Escribe un post profesional sobre: {topic}
Audiencia: {audience}
Contexto adicional: {context}
{brand_context}
IMPORTANT: You MUST write the entire response in {language}. Do not use any other language.
Tono profesional pero cercano. Incluye una reflexión y llamada a la acción.""",
}


def generate_content(
    topic: str,
    platform: str,
    audience: str,
    context: str = "",
    model: str = "llama-3.1-8b-instant",
    language: str = "Español",
    brand_info: str = "",
) -> str:
    """
    Genera contenido para una plataforma específica.

    Args:
        topic: Tema del contenido
        platform: Plataforma (blog, twitter, instagram, linkedin)
        audience: Audiencia objetivo
        context: Contexto adicional (opcional, usado por RAG)
        model: Modelo de Groq a usar
        language: Idioma del contenido generado
        brand_info: Información de la empresa o persona (personalización)

    Returns:
        Contenido generado como string
    """
    llm = ChatGroq(
        model=model,
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.7,
    )

    brand_context = f"Información sobre quien publica: {brand_info}" if brand_info else ""

    prompt_template = PLATFORM_PROMPTS.get(platform, PLATFORM_PROMPTS["blog"])
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | llm

    response = chain.invoke({
        "topic": topic,
        "audience": audience,
        "context": context if context else "No hay contexto adicional.",
        "brand_context": brand_context,
        "language": language,
    })

    return response.content