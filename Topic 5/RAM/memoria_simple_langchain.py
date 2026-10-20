from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
#from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
# from langgraph.checkpoint.memory import InMemorySaver 
# from langchain.agents import create_agent

## == Sin persistencia - Para prototipos o apps sencillas sin necesidad de guardar en disco
# Revisar modelo nuevo: https://docs.langchain.com/oss/python/langchain/short-term-memory

# def get_user_info() -> str:
#     """Look up information about the current user."""
#     return "No user profile on file."

#llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0)
# llm = create_agent(
#     model="google_genai:gemini-3.5-flash-lite",
#     checkpointer=InMemorySaver(),
# )

prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente útil."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm | StrOutputParser()

store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Cadena con memoria automatica por sesion
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

print("Chat en terminal (escribe 'salir' para terminar)\n")
session_id = "sesion_terminal"

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

    respuesta = chain_with_memory.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": session_id}}
    )
    print("Asistente:", respuesta)