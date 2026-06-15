import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
from src.generators.content_generator import generate_content, AVAILABLE_MODELS

st.set_page_config(page_title="ContentAI", page_icon="✦", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        color: white;
    }
    .hero h1 { font-size: 2.2rem; font-weight: 700; margin: 0; }
    .hero p { opacity: 0.85; margin: 0.4rem 0 0; font-size: 1rem; }

    .card {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .output-card {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border-left: 4px solid #667eea;
        border-radius: 0 12px 12px 0;
        padding: 1.5rem;
        margin-top: 1rem;
    }

    div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
    }

    div[data-testid="stToggle"] { margin-top: 0.5rem; }
    .stSelectbox label, .stTextInput label, .stTextArea label { font-weight: 500; }
</style>

<div class="hero">
    <h1>✦ ContentAI</h1>
    <p>Genera contenido para redes sociales con IA y fuentes científicas reales</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox("Plataforma", ["blog", "twitter", "instagram", "linkedin"],
        format_func=lambda x: {"blog": "Blog", "twitter": "Twitter / X", "instagram": "Instagram", "linkedin": "LinkedIn"}[x])
with col2:
    audience = st.selectbox("Audiencia", ["público general", "profesionales", "estudiantes", "científicos", "emprendedores"])

topic = st.text_input("Tema", placeholder="Ej: inteligencia artificial, física cuántica, cambio climático...")

col3, col4 = st.columns(2)
with col3:
    model = st.selectbox("Modelo", options=list(AVAILABLE_MODELS.keys()), format_func=lambda x: AVAILABLE_MODELS[x])
with col4:
    language = st.selectbox("Idioma", ["Español", "English", "Français", "Italiano"])

brand_info = st.text_area("Perfil o empresa (opcional)",
    placeholder="Ej: Startup de tecnología sostenible dirigida a jóvenes creativos...", height=80)

use_rag = st.toggle("Enriquecer con papers científicos (RAG + arXiv)", value=False)

generate_btn = st.button("Generar")

if generate_btn:
    if not topic:
        st.warning("Introduce un tema para continuar.")
    else:
        with st.spinner("Generando..."):
            if use_rag:
                from src.rag.rag_chain import run_rag_pipeline
                result = run_rag_pipeline(topic, platform, audience, model=model, language=language, brand_info=brand_info)
                content = result["content"]
                sources = result["sources"]
                used_rag = result["used_rag"]
            else:
                content = generate_content(topic, platform, audience, model=model, language=language, brand_info=brand_info)
                sources = []
                used_rag = False

        st.markdown(f"""
        <div class="output-card">
            {content.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Copiar texto plano"):
            st.code(content, language=None)

        if used_rag and sources:
            st.markdown("#### Fuentes")
            for i, source in enumerate(sources, 1):
                with st.expander(f"{i}. {source['title']}"):
                    st.write(f"Publicado: {source['published']}")
                    st.write(f"[Ver paper]({source['url']})")