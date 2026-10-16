from langchain_core.runnables import RunnableLambda

paso1 = RunnableLambda(lambda x: f"Numero {x}")

def duplicar_texto(texto: str) -> str:
    return [texto] * 2

paso2 = RunnableLambda(duplicar_texto)

# tansformar la salida de paso1 a la entrada de paso2
cadena = paso1 | paso2

resultado = cadena.invoke(5)
print(resultado) 