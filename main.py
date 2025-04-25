# main.py
import os
import streamlit as st
from dotenv import load_dotenv
from agents import Agent, TokenCounter
from orchestrator import AgentOrchestrator
from examples import create_example_queries

load_dotenv()

def main():
    st.set_page_config(page_title="LLM Razonador OpenAI", layout="wide")
    st.title("🧠 Razonador Multi-Agente con OpenAI")

    # Sidebar
    with st.sidebar:
        st.header("Configuración")
        key = os.getenv("OPENAI_API_KEY") or st.text_input("OpenAI API Key", type="password")
        if key:
            os.environ["OPENAI_API_KEY"] = key

        st.subheader("Modelo de OpenAI")
        model = st.selectbox("Modelo", ["gpt-4.1","gpt-4.1-mini","gpt-4o","gpt-3.5-turbo"], index=0)

        st.subheader("Agentes")
        use_math    = st.checkbox("Análisis Matemático", True)
        use_logic   = st.checkbox("Verificación Lógica", True)
        use_creative= st.checkbox("Pensamiento Creativo", False)
        reasoning   = st.checkbox("Razonamiento Explícito", True)

        if st.button("Reiniciar"):
            for k in ['processed_query','result','query']: st.session_state.pop(k, None)
            st.rerun()

    # Ejemplos y consulta
    examples = create_example_queries()
    choice = st.selectbox("Ejemplos:", ["Selecciona..."] + list(examples.keys()))
    query = examples.get(choice, "") if choice!="Selecciona..." else ""
    query = st.text_area("Consulta:", value=query, height=150)

    if st.button("Procesar") and query:
        orch = AgentOrchestrator()
        # agrega agentes según configuración
        if use_math:    orch.add_agent(Agent("Matemáticas", orch.counter, model, reasoning))
        if use_logic:   orch.add_agent(Agent("Lógica",      orch.counter, model, reasoning))
        if use_creative:orch.add_agent(Agent("Creativo",    orch.counter, model, reasoning))
        # coordinador
        orch.set_coordinator(Agent("Coordinador", orch.counter, model, reasoning))

        result = orch.process_query(query)

        st.subheader("📊 Estadísticas de Tokens")
        st.table(result['stats'])

        st.subheader("🤖 Respuesta Final")
        st.write(result['final']['content'])

        with st.expander("Respuestas de Agentes"):
            for name, resp in result['agents'].items():
                st.markdown(f"**{name}**: {resp['content']}")
                if resp.get('reasoning'):
                    with st.expander("Razonamiento"):
                        st.markdown(resp['reasoning'])

if __name__ == "__main__":
    main()
