from langchain_community.document_loaders import GitLoader

# Carga archivos directamente desde repositorios Git.
# Casos de uso ideales:
# - Análisis de código fuente
# - Documentación de proyectos
# - Auditorías de repositorios
# - Generación de documentación automática
 
# Clonar y procesar repositorio
loader = GitLoader(
    clone_url="https://github.com/usuario/proyecto-ejemplo.git",
    repo_path="./temp_repo",
    branch="main",
    file_filter=lambda file_path: file_path.endswith(('.py', '.md', '.txt'))
)
 
docs = loader.load()
print(f"Archivos cargados del repositorio: {len(docs)}")
 
# Análisis por tipo de archivo
file_types = {}
total_lines = 0
 
for doc in docs:
    file_path = doc.metadata['source']
    file_ext = file_path.split('.')[-1] if '.' in file_path else 'sin_extension'
    
    file_types[file_ext] = file_types.get(file_ext, 0) + 1
    lines = doc.page_content.count('\n') + 1
    total_lines += lines
    
    print(f"Archivo: {file_path}")
    print(f"  Líneas: {lines}")
    print(f"  Caracteres: {len(doc.page_content)}")
    print(f"  Vista previa: {doc.page_content[:100]}...")
    print()
 
print(f"\nEstadísticas del repositorio:")
print(f"  Total de líneas de código: {total_lines:,}")
print(f"  Tipos de archivo:")
for ext, count in sorted(file_types.items()):
    print(f"    .{ext}: {count} archivos")