from langchain_community.document_loaders import WebBaseLoader
import bs4  # 👈 Importante: importar la librería bs4

# El WebBaseLoader es perfecto para extraer contenido de páginas web de forma sencilla.
# Casos de uso ideales:
# - Documentación técnica
# - Artículos de blog
# - Noticias y contenido web estático
# - Scraping de contenido público
 
# Ejemplo básico: cargar documentación
loader = WebBaseLoader("https://docs.langchain.com/docs/")
docs = loader.load()
 
print(f"Título: {docs[0].metadata.get('title', 'Sin título')}")
print(f"URL: {docs[0].metadata['source']}")
print(f"Contenido: {docs[0].page_content[:300]}...")
 
# Ejemplo avanzado: múltiples URLs con configuración personalizada
urls = [
    "https://python.langchain.com/docs/concepts/",
    "https://python.langchain.com/docs/tutorials/",
    "https://python.langchain.com/docs/how_to/"
]
 
loader = WebBaseLoader(
    web_paths=urls,
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            "div", {"class": ["main-content", "article-content"]}
        )
    )
)
docs = loader.load()
 
print(f"Páginas cargadas: {len(docs)}")
for i, doc in enumerate(docs):
    print(f"Página {i+1}: {doc.metadata['source']}")
    print(f"Longitud: {len(doc.page_content)} caracteres")
