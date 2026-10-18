from langchain_community.vectorstores import Chroma
#from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pathlib import Path

current_dir = Path(__file__).parent
persist_path_str = str(current_dir / "chroma_db")

# Aqui ya no creamos la BBDD a partir de los documentos, sino que la cargamos desde el directorio donde se encuentra persistida
vectorstore = Chroma(
    embedding_function=GoogleGenerativeAIEmbeddings(model="gemini-embedding-001"),#OpenAIEmbeddings(model="text-embedding-3-large"),
    persist_directory=persist_path_str
)

#Transformamos la BBDD en retriever, busqueda por similaridad, k=2 para obtener los 2 documentos más similares a la consulta
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2}) 

consulta = "¿Dónde se encuentra el local del contrato en el que participa María Jiménez Campos?"
resultados = retriever.invoke(consulta)

print("Top 2 documentos mas similares a la consulta:\n")
for i, doc in enumerate(resultados, start=1):
    print(f"Contenido: {doc.page_content}")
    print(f"Metadatos: {doc.metadata}")