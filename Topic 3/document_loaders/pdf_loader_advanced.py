from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

# Los PDFs contienen información valiosa que este loader puede extraer página por página.
# Casos de uso ideales:
# - Manuales técnicos
# - Contratos y documentos legales
# - Papers académicos
# - Reportes empresariales

# Obtener la ruta del directorio donde reside el archivo de script actual
current_dir = Path(__file__).parent
pdf_path = current_dir / "Preguntas_de_Examen_Product_Owner.pdf"
 
# Cargar PDF con información detallada por página
loader = PyPDFLoader(str(pdf_path))
pages = loader.load_and_split()
 
print(f"Total de páginas: {len(pages)}")
 
# Analizar contenido por página
for i, page in enumerate(pages[:3]):  # Primeras 3 páginas
    print(f"\n=== PÁGINA {i+1} ===")
    print(f"Número de página: {page.metadata['page']}")
    print(f"Archivo fuente: {page.metadata['source']}")
    print(f"Contenido: {page.page_content[:200]}...")
    
    # Estadísticas de la página
    words = len(page.page_content.split())
    chars = len(page.page_content)
    print(f"Palabras: {words}, Caracteres: {chars}")
 
# Buscar páginas con contenido específico
keyword = "configuración"
relevant_pages = [
    page for page in pages 
    if keyword.lower() in page.page_content.lower()
]
print(f"\nPáginas que mencionan '{keyword}': {len(relevant_pages)}")