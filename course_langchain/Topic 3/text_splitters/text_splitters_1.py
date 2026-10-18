from langchain_community.document_loaders import PyPDFLoader
#from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from pathlib import Path

## NO LANZAR PETA

# Obtener la ruta del directorio donde reside el archivo de script actual
current_dir = Path(__file__).parent
pdf_path = current_dir / "quijote.pdf"

# 1. Cargar el documento PDF
loader = PyPDFLoader(str(pdf_path))
pages = loader.load()

# 2. Combinar todas las páginas en un texto único
full_text = ""
for page in pages:
    full_text += page.page_content + "\n"

# 3. Pasar el texto al LLM
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0.2)
response = llm.invoke(f"Haz un resumen de los puntos mas importantes del siguiente documento: {full_text}")

print(response)