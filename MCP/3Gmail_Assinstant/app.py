import streamlit as st
from client import GmailMCPClient
import asyncio

st.set_page_config(
    page_title="Gmail Assistant",
    page_icon="📧",
    layout="wide"
)

# Inicializar cliente
@st.cache_resource
def get_client():
    return GmailMCPClient()

client = get_client()

# Titulo
st.title("📧 Gmail Assistant con MCP")
st.markdown("Asistente inteligente para gestionar tu Gmail usando GPT-4o-mini")

# Sidebar para mostrar informacion del cliente MCP
with st.sidebar:
    st.header("🚀 Prompts Rápidos")
    
    if st.button("📊 Resumen diario de emails", use_container_width=True):
        st.session_state.use_prompt = "daily_email_summary"
        st.session_state.prompt_params = {}

    st.divider()

    with st.expander("✉️ Redactar email profesional"):
        recipient = st.text_input("Destinatario (opcional)", key="recipient")
        subject = st.text_input("Asunto (opcional)", key="subject")
        if st.button("Usar prompt", key="compose_btn"):
            st.session_state.use_prompt = "compose_professional_email"
            st.session_state.prompt_params = {
                "recipient": recipient,
                "subject": subject
            }

    st.divider()

    st.markdown("### ℹ️ Información del sistema")
    with st.spinner("Cargando info..."):
        info = asyncio.run(client.get_system_info())

    # Mostrar información en desplegables organizados
    with st.expander("🔧 Herramientas disponibles", expanded=False):
        st.caption(f"Total: {len(info['tools'])}")
        for tool in info['tools']:
            st.markdown(f"• `{tool}`")
    
    with st.expander("📦 Recursos estáticos", expanded=False):
        st.caption(f"Total: {len(info['resources'])}")
        for res in info['resources']:
            st.markdown(f"• `{res}`")
    
    with st.expander("📋 Plantillas de recursos", expanded=False):
        st.caption(f"Total: {len(info.get('templates', []))}")
        if info.get('templates'):
            for template in info['templates']:
                st.markdown(f"• `{template}`")
        else:
            st.info("No hay plantillas de recursos disponibles")
    
    with st.expander("💬 Prompts disponibles", expanded=False):
        st.caption(f"Total: {len(info['prompts'])}")
        for prompt in info['prompts']:
            st.markdown(f"• `{prompt}`")
