import os
from langchain_community.document_loaders import WebBaseLoader

# 1. Configurar un User-Agent para identificarse en la petición HTTP
os.environ["USER_AGENT"] = "MiAppLangChain/1.0 (Contacto: mi_email@ejemplo.com)"

# 2. Instanciar y cargar el contenido web
loader = WebBaseLoader("https://www.python.org/")
web_docs = loader.load()
#print(web_docs)

# 3. Inspeccionar el contenido del primer documento cargado
print(f"Total de documentos/páginas: {len(web_docs)}")
print("\nMetadatos:")
print(web_docs[0].metadata)

print("\nPrimeros 300 caracteres del texto extraído:")
#print(web_docs[0].page_content[:300])
print(web_docs[0].page_content)