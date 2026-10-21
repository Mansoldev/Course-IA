from langchain_core.tools import tool
from langchain_core.tools import StructuredTool # Con Structured Tool - más personalizable, pero más antiguo

@tool("Herramienta acceso base de datos usuarios", return_direct=True) #El resultado es el resultado final, no vuelve al LLM
def herramienta_personalizada(query: str) -> str: #Typehint tipado
    """Consulta la base de datos de usuarios de la empresa.""" #DocString
    # Codigo que accede a la base de datos
    return f"Respuesta a la consulta: {query}"

output = herramienta_personalizada.run("Consulta de prueba")
print(output)

print(f"Nombre de la herramienta: {herramienta_personalizada.name}")
print(f"Descripcion de la herramienta: {herramienta_personalizada.description}")


# Con Structured Tool - más personalizable, pero más antiguo
def herramienta_personalizada2(query: str) -> str: #Typehint tipado
    """Consulta la base de datos de usuarios de la empresa.""" #DocString
    # Codigo que accede a la base de datos
    return f"Respuesta a la consulta: {query}"

my_tool = StructuredTool.from_function(herramienta_personalizada2)

print(my_tool.run("consulta personalizada"))