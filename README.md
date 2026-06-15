#  AI Content Generator

Generador de contenido para redes sociales con IA generativa y fuentes científicas reales de arXiv. Proyecto desarrollado como prueba de concepto (PoC) para el bootcamp de IA de Factoria F5.

Permite generar contenido adaptado a distintas plataformas (Blog, Twitter/X, Instagram, LinkedIn) y audiencias, con la opción de enriquecer el resultado usando una arquitectura **RAG** que extrae conocimiento de papers científicos de arXiv.

---

##  Características

- **Generación multiplataforma:** prompts especializados para Blog, Twitter/X, Instagram y LinkedIn.
- **Adaptación por audiencia:** público general, profesionales, estudiantes, científicos, emprendedores.
- **RAG científico (opcional):** busca papers en arXiv, los indexa en una base de datos vectorial y usa su contenido como contexto para mejorar la calidad y rigor del texto generado.
- **Coste cero:** usa el tier gratuito de Groq como LLM y embeddings locales, sin gasto de API de pago.

---

##  Arquitectura

```
┌─────────────────────────────┐
│      Streamlit UI           │   ← interfaz web (app.py)
└──────────────┬──────────────┘
               │
       ┌───────┴────────┐
       │                │
       ▼                ▼
┌─────────────┐  ┌──────────────────┐
│ Generador   │  │   Pipeline RAG    │
│ de contenido│  │                   │
│ (prompts +  │  │  arXiv → Chunking │
│  Groq LLM)  │  │  → Embeddings     │
└─────────────┘  │  → ChromaDB       │
                 │  → Retriever      │
                 │  → Groq LLM       │
                 └──────────────────┘
```

**Flujo sin RAG:** el usuario introduce tema + plataforma + audiencia → se aplica el prompt adecuado → Groq genera el contenido.

**Flujo con RAG:** además, se buscan papers en arXiv → se indexan en ChromaDB con embeddings locales → se recuperan los más relevantes → su contenido se inyecta como contexto en el prompt.

---

##  Stack tecnológico

| Componente | Tecnología | Por qué |
|------------|-----------|---------|
| Lenguaje | Python 3.11+ | Estándar en el ecosistema de IA |
| Gestor de paquetes | uv | Rápido y moderno |
| Framework LLM | LangChain | Permite encadenar prompts y modelos de forma extensible |
| LLM | Groq (`llama-3.1-8b-instant`) | Gratuito y muy rápido |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` | Local y gratuito, sin coste de API |
| Base de datos vectorial | ChromaDB | Local, persistente, fácil de integrar |
| Fuente de datos | arXiv | Papers científicos abiertos |
| Interfaz | Streamlit | Crea una web funcional con solo Python |

---

##  Instalación y uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/gabriela-her/llm-content-generator.git
cd llm-content-generator
```

### 2. Instalar dependencias

```bash
uv pip install -e .
```

### 3. Configurar la API key

Crea un archivo `.env` en la raíz con tu clave de Groq (gratis en https://console.groq.com):

```env
GROQ_API_KEY=tu_api_key_aqui
```

### 4. Ejecutar la aplicación

```bash
uv run streamlit run src/ui/app.py
```

La app se abre en `http://localhost:8501`.

---

##  Estructura del proyecto

```
src/
├── generators/
│   └── content_generator.py   # Prompts por plataforma + llamada al LLM
├── rag/
│   ├── arxiv_loader.py         # Búsqueda de papers en arXiv
│   ├── vector_store.py         # ChromaDB + embeddings locales
│   └── rag_chain.py            # Pipeline RAG completo
└── ui/
    └── app.py                  # Interfaz Streamlit
```

---

##  Decisiones técnicas

Algunas decisiones de ingeniería tomadas durante el desarrollo:

- **Lazy loading del modelo de embeddings:** el modelo solo se carga la primera vez que se usa el RAG, no al arrancar la app. Esto acelera el arranque cuando solo se genera contenido simple.
- **Recorte del contexto RAG:** el tier gratuito de Groq limita a 6000 tokens por minuto. Los papers de arXiv son largos, así que se recorta cada documento para no exceder el límite, manteniendo el contexto relevante.
- **Ejecución directa de la app:** Streamlit re-ejecuta el script en cada interacción. Por eso la app se ejecuta directamente (`app.py`) en lugar de a través de un import, evitando problemas de caché de módulos.

---

##  Licencia

Proyecto educativo desarrollado por Gabriela Hernandez en el bootcamp de IA de Factoria F5.