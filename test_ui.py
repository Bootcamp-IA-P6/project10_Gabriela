import streamlit as st

st.title("Test")

col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox("Plataforma", ["blog", "twitter", "instagram"])
with col2:
    audience = st.selectbox("Audiencia", ["general", "profesionales"])

topic = st.text_input("Tema")
use_rag = st.toggle("RAG", value=False)
btn = st.button("Generar", type="primary", use_container_width=True)

st.write(f"Elegiste: {platform}, {audience}")