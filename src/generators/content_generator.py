from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

# Inicializamos el modelo de Groq
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7,
)

# Prompts personalizados por plataforma
PLATFORM_PROMPTS = {
    "blog": """Eres un escritor experto en blogs. 
Escribe un artículo de blog completo sobre: {topic}
Audiencia: {audience}
Contexto adicional: {context}

El artículo debe tener introducción, desarrollo y conclusión.
Usa un tono cercano y profesional.""",

    "twitter": """Eres un experto en Twitter/X.
Crea un hilo de 5 tweets sobre: {topic}
Audiencia: {audience}
Contexto adicional: {context}

Cada tweet debe empezar con su número (1/, 2/, etc).
Máximo 280 caracteres por tweet. Usa hashtags relevantes.""",

    "instagram": """Eres un experto en Instagram.
Crea una caption para Instagram sobre: {topic}
Audiencia: {audience}
Contexto adicional: {context}

Incluye emojis, llamada a la acción y hashtags al final.""",

    "linkedin": """Eres un experto en LinkedIn.
Escribe un post profesional sobre: {topic}
Audiencia: {audience}
Contexto adicional: {context}

Tono profesional pero cercano. Incluye una reflexión y llamada a la acción.""",
}


def generate_content(topic: str, platform: str, audience: str, context: str = "") -> str:
    """
    Genera contenido para una plataforma específica.
    
    Args:
        topic: Tema del contenido
        platform: Plataforma (blog, twitter, instagram, linkedin)
        audience: Audiencia objetivo
        context: Contexto adicional (opcional, usado por RAG)
    
    Returns:
        Contenido generado como string
    """
    prompt_template = PLATFORM_PROMPTS.get(platform, PLATFORM_PROMPTS["blog"])
    
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | llm
    
    response = chain.invoke({
        "topic": topic,
        "audience": audience,
        "context": context if context else "No hay contexto adicional.",
    })
    
    return response.content