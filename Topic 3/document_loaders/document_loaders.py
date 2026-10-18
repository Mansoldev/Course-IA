from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

# Obtener la ruta del directorio donde reside el archivo de script actual
current_dir = Path(__file__).parent
pdf_path = current_dir / "Preguntas_de_Examen_Product_Owner.pdf"

# Cargar el documento
loader = PyPDFLoader(str(pdf_path))
pages = loader.load()

#print(dir(pages)) #Mostrar los atributos y métodos del objeto docs
#print(dir(pages[0])) #Mostrar los atributos y métodos del primer documento cargado
#print(pages[0].page_content) #Mostrar el contenido de la primera página del documento cargado

for i, page in enumerate(pages):
    print(f"=== Página {i + 1} ===\n") # Título de la página
    print(page.page_content)
    print("\n" + "-" * 80 + "\n")  # Separador entre páginas



