from pathlib import Path
from langchain_community.document_loaders import UnstructuredHTMLLoader

# Procesa archivos HTML locales o remotos con análisis inteligente de estructura.
# Casos de uso ideales:
# - Procesamiento de reportes web
# - Análisis de documentación HTML
# - Extracción de contenido de emails HTML
# - Procesamiento de archivos exportados

# Obtener la ruta del directorio donde reside el archivo de script actual
current_dir = Path(__file__).parent
html_path = current_dir / "index.html"
 
# Procesar archivo HTML local
loader = UnstructuredHTMLLoader(
    html_path,
    mode="elements",  # Preservar estructura de elementos
    strategy="fast"   # Estrategia de procesamiento
)
 
docs = loader.load()
 
print(f"Elementos HTML procesados: {len(docs)}")
 
# Analizar tipos de elementos encontrados
element_types = {}
for doc in docs:
    element_type = doc.metadata.get('category', 'unknown')
    element_types[element_type] = element_types.get(element_type, 0) + 1
 
print("\nTipos de elementos encontrados:")
for element_type, count in sorted(element_types.items()):
    print(f"  {element_type}: {count}")
 
# Mostrar elementos de texto más largos
text_elements = [doc for doc in docs if doc.metadata.get('category') == 'NarrativeText']
text_elements.sort(key=lambda x: len(x.page_content), reverse=True)
 
print(f"\nTop 3 elementos de texto más largos:")
for i, element in enumerate(text_elements[:3]):
    print(f"{i+1}. {len(element.page_content)} caracteres:")
    print(f"   {element.page_content[:150]}...")