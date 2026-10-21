from langgraph.graph import MessagesState, StateGraph, START
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
#from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

## == Memoria persistente secuencial - para conservar historiales entre ejecuciones, reinicios o despliegues

#llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0)
chain = llm | StrOutputParser()

workflow = StateGraph(state_schema=MessagesState)

def chatbot_node(state):
    """Nodo que procesa mensajes y genera respuestas."""
    system_prompt = "Eres un asistente amigable que recuerda conversaciones previas."
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = chain.invoke(messages)
    return {"messages": [response]}

workflow.add_node("chatbot", chatbot_node)
workflow.add_edge(START, "chatbot")

# Compilar el grafo
conn = sqlite3.connect("historial.db", check_same_thread=False)
memory = SqliteSaver(conn)
app = workflow.compile(checkpointer=memory)

def chat(message, thread_id="sesion_terminal"): # El thread_id hará que podamos recuperar la session
    config = {"configurable": {"thread_id": thread_id}}
    result = app.invoke({"messages": [HumanMessage(content=message)]}, config)
    return result["messages"][-1].content

if __name__ == "__main__":
    print("Chat en terminal (escribe 'salir' para terminar)\n")
    session_id = "sesion_terminal2"

    while True:
        try:
            user_input = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nHasta luego!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"salir", "exit", "quit"}:
            print("Hasta luego!")
            break

        respuesta = chat(user_input, session_id)
        print("Asistente:", respuesta)