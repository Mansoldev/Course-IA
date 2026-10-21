from langchain_core.tools import tool
from langchain_experimental.utilities.python import PythonREPL
from pydantic import BaseModel, Field

# Instancia del REPL
python_repl = PythonREPL()


# Esquema para definir claramente el argumento que espera el LLM
class PythonExecutionInput(BaseModel):
    code: str = Field(
        description="Código Python válido a ejecutar. Debe usar print() para mostrar resultados."
    )


@tool("execute_python", args_schema=PythonExecutionInput)
def execute_python(code: str) -> str:
    """Ejecuta código Python localmente y devuelve la salida estándar (stdout).
    Útil para cálculos matemáticos, manipulación de datos o lógica algorítmica.
    """
    try:
        result = python_repl.run(code)
        # Si el código no imprimiere nada (por ejemplo solo 'x = 2 + 2'), avisamos al LLM
        if not result:
            return "El código se ejecutó correctamente pero no generó ninguna salida (asegúrate de usar print())."
        return result
    except Exception as e:
        return f"Error al ejecutar el código: {str(e)}"


# Probando la herramienta
if __name__ == "__main__":
    output = execute_python.invoke({"code": "print(2 + 2)"})
    print("Resultado:", output)