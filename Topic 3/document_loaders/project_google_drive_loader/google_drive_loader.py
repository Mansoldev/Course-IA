from langchain_google_community.drive import GoogleDriveLoader

credentials_path = "C:\\Users\\Mario\\Documents\\Temporal\\credentials.json"  # Ruta al archivo de credenciales de Google Drive
token_path = "C:\\Users\\Mario\\Documents\\Temporal\\token.json"  # Ruta al archivo de token de Google Drive

# Cargar el documento desde Google Drive (file_id es el identificador del archivo en Google Drive)
loader = GoogleDriveLoader(
    folder_id="1pykPpIkzuDmBYfuOW9VZbGeax7RfWbGr", # Carpeta tests
    credentials_path=credentials_path,
    token_path=token_path,
    recursive=True  # Cambiar a True si deseas cargar documentos de subcarpetas también
)

documents = loader.load()

#print(documents)  # Imprime la lista de documentos cargados
for i, document in enumerate(documents):
    print(f"=== Documento {i + 1} ===\n")  # Título de la página
    print(document.page_content)
    print("\n" + "-" * 80 + "\n")  # Separador entre páginas