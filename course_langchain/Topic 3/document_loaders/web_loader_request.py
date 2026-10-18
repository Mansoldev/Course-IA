import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document

url = "https://www.python.org/"
headers = {"User-Agent": "MiAppLangChain/1.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Extraer el texto limpio del HTML
texto_limpio = soup.get_text(separator="\n", strip=True)

# Crear el objeto Document compatible con LangChain
doc = Document(
    page_content=texto_limpio,
    metadata={"source": url, "title": soup.title.string if soup.title else ""}
)

print(f"Título: {doc.metadata['title']}")
print(f"Contenido (primeros 300 caracteres):\n{doc.page_content[:300]}")