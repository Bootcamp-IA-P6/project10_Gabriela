import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
from src.generators.content_generator import generate_content

st.set_page_config(page_title="AI Content Generator", page_icon="🤖")

st.title("🤖 AI Content Generator")
st.caption("Genera contenido para redes sociales con IA y fuentes científicas de arXiv")

st.divider()

col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox("Plataforma", ["blog", "twitter", "instagram", "linkedin"])
with col2:
    audience = st.selectbox(
        "Audiencia",
        ["público general", "profesionales", "estudiantes", "científicos", "emprendedores"],
    )

topic = st.text_input("Tema", placeholder="Ej: inteligencia artificial, física cuántica...")
use_rag = st.toggle("🔬 Enriquecer con papers científicos (RAG + arXiv)", value=False)

generate_btn = st.button("✨ Generar contenido", type="primary")

st.divider()

if generate_btn:
    if not topic:
        st.warning("Por favor, introduce un tema.")
    else:
        with st.spinner("Generando contenido..."):
            if use_rag:
                st.info("🔍 Buscando papers en arXiv...")
                from src.rag.rag_chain import run_rag_pipeline
                result = run_rag_pipeline(topic, platform, audience)
                content = result["content"]
                sources = result["sources"]
                used_rag = result["used_rag"]
            else:
                content = generate_content(topic, platform, audience)
                sources = []
                used_rag = False

        st.success("¡Contenido generado!")
        st.subheader("📄 Contenido generado")
        st.markdown(content)

        with st.expander("📋 Copiar texto plano"):
            st.code(content, language=None)

        if used_rag and sources:
            st.divider()
            st.subheader("📚 Fuentes científicas (arXiv)")
            for i, source in enumerate(sources, 1):
                with st.expander(f"{i}. {source['title']}"):
                    st.write(f"📅 {source['published']}")
                    st.write(f"🔗 [Ver paper]({source['url']})")