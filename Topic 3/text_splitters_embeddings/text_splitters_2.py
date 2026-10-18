from langchain_community.document_loaders import PyPDFLoader
#from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser

# Obtener la ruta del directorio donde reside el archivo de script actual
current_dir = Path(__file__).parent
pdf_path = current_dir / "quijote.pdf"

# 1. Cargar el documento PDF
loader = PyPDFLoader(str(pdf_path))
pages = loader.load()

# Dividir el texto en chunks mas pequeños
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=10000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(pages)

# 3. Pasar el texto al LLM
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0.2)
cadena = llm | StrOutputParser()
summaries = []

i = 0
for chunk in chunks:
    if i > 5:
        break
    response = cadena.invoke(f"Haz un resumen de los puntos mas importantes del siguiente texto: {chunk.page_content}")
    summaries.append(response)
    i += 1

print(summaries)

final_summary = cadena.invoke(f"Combina y sintetiza estos resumenes en un resumen coherente y completo: {" ".join(summaries)}")
print(final_summary)