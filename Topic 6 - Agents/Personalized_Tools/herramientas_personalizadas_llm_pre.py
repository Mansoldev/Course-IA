from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0.2)

@tool("user_db_tool", return_direct=True) #El resultado es el resultado final, no vuelve al LLM
def herramienta_personalizada(query: str) -> str: #Typehint tipado
    """Consulta la base de datos de usuarios de la empresa.""" #DocString
    # Codigo que accede a la base de datos
    return f"Respuesta a la consulta: {query}"

llm_with_tools = llm.bind_tools([herramienta_personalizada])

response = llm_with_tools.invoke("Genera un resumen de la informacion sobre el usuario UX341234 que se encuentra en nuestra base de datos.")

print(response.tool_calls[0]["args"])