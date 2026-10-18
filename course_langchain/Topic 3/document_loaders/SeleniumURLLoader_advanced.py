from langchain_community.document_loaders import SeleniumURLLoader
from selenium.webdriver.chrome.options import Options

# Para páginas web que requieren renderizado de JavaScript.
# Casos de uso ideales:
# - Single Page Applications (SPAs)
# - Dashboards interactivos
# - Sitios con autenticación
# - Contenido generado por JavaScript

# Configurar opciones de navegador
chrome_options = Options()
chrome_options.add_argument("--headless")  # Sin interfaz gráfica
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
 
# URLs con contenido dinámico
urls = [
    "https://example.com/dashboard-dinamico",
    "https://spa-application.com/data",
    "https://chart-website.com/interactive"
]
 
loader = SeleniumURLLoader(
    urls=urls,
    browser="chrome",
    executable_path="/path/to/chromedriver"  # Opcional si está en PATH
)
#chrome_options=chrome_options
 
docs = loader.load()
 
print(f"Páginas procesadas: {len(docs)}")
 
for i, doc in enumerate(docs):
    print(f"\n=== PÁGINA {i+1} ===")
    print(f"URL: {doc.metadata['source']}")
    print(f"Título: {doc.metadata.get('title', 'Sin título')}")
    print(f"Contenido renderizado: {len(doc.page_content)} caracteres")
    
    # Buscar elementos que indiquen contenido dinámico
    dynamic_indicators = ['data-', 'ng-', 'v-', 'react-', 'vue-']
    has_dynamic = any(indicator in doc.page_content for indicator in dynamic_indicators)
    print(f"Contiene elementos dinámicos: {'Sí' if has_dynamic else 'No'}")
    
    print(f"Vista previa: {doc.page_content[:200]}...")
