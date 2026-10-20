from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict
from langgraph.graph import END, START, StateGraph

## == dataclass: Ideal si quieres la sintaxis más limpia, el menor overhead posible y dependes del IDE / mypy para la revisión de tipos.

# 0. Enums para evitar cadenas mágicas
class StateKey(str, Enum):
    TEXTO_ORIGINAL = "texto_original"
    TEXTO_MAYUS = "texto_mayus"
    LONGITUD = "longitud"

class NodeName(str, Enum):
    MAYUS = "Mayus"
    CONTAR = "Contar"

# 1. Esquema de estado con @dataclass
@dataclass
class State:
    texto_original: str
    texto_mayus: str | None = None
    longitud: int | None = None


# 2. Funciones de los nodos
def poner_mayusculas(state: State) -> Dict[str, Any]:
    texto = state.texto_original
    return {StateKey.TEXTO_MAYUS: texto.upper()}

def contar_caracteres(state: State) -> Dict[str, Any]:
    # Si state.texto_mayus es None, podemos manejar la lógica de forma segura
    texto = state.texto_mayus or ""
    return {StateKey.LONGITUD: len(texto)}

# 3. Construcción del Grafo
graph = StateGraph(State)

# 4. Añadir los nodos al grafo
graph.add_node(NodeName.MAYUS, poner_mayusculas)
graph.add_node(NodeName.CONTAR, contar_caracteres)

# 5. Conectar los nodos en secuencia
graph.add_edge(START, NodeName.MAYUS)
graph.add_edge(NodeName.MAYUS, NodeName.CONTAR)
graph.add_edge(NodeName.CONTAR, END)

# 6. Compilar el grafo
compiled_graph = graph.compile()

# 7. Invocar el grafo con un estado inicial
estado_inicial = State(texto_original="Hola mundo")

resultado = compiled_graph.invoke(estado_inicial)
print("Resultado con Dataclass:")
print(resultado)