from langchain_chroma import Chroma
#from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path

# Obtener la ruta del directorio donde reside el archivo de script actual
current_dir = Path(__file__).parent
pdf_path = current_dir / "contratos"
#print(pdf_path)
loader = PyPDFDirectoryLoader(pdf_path)
documentos = loader.load()

print(f"Se cargaron {len(documentos)} documentos desde el directorio.")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=5000,
    chunk_overlap=1000
)

docs_split = text_splitter.split_documents(documentos)

print(f"Se crearon {len(docs_split)} chunks de texto.")

# Crea la BBDD a partir de los documentos divididos en chunks
persist_path_str = str(current_dir / "chroma_db")
vectorstore = Chroma.from_documents(
    docs_split,
    embedding=GoogleGenerativeAIEmbeddings(model="gemini-embedding-001"),#OpenAIEmbeddings(model="text-embedding-3-large"),
    persist_directory=persist_path_str
)

consulta = "¿Dónde se encuentra el local del contrato en el que participa María Jiménez Campos"

resultados = vectorstore.similarity_search(consulta, k=2)

print("Top 3 documentos mas similares a la consulta:\n")
for i, doc in enumerate(resultados, start=1):
    print(f"Contenido: {doc.page_content}")
    print(f"Metadatos: {doc.metadata}")