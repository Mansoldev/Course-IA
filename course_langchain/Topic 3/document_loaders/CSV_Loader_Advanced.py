from langchain_community.document_loaders import CSVLoader
from pathlib import Path

# Obtener la ruta del directorio donde reside el archivo de script actual
current_dir = Path(__file__).parent
csv_path = current_dir / "prueba.csv"
 
# Configuración avanzada para CSV
loader = CSVLoader(
    file_path=csv_path,
    csv_args={
        'delimiter': ',',
        'quotechar': '"',
        'fieldnames': ['fecha', 'producto', 'cantidad', 'precio', 'cliente']
    },
    encoding='utf-8',
    source_column='producto',  # Usar una columna como identificador
    metadata_columns=['fecha', 'cliente']  # Incluir en metadatos
)
 
docs = loader.load()
print(f"Registros de ventas cargados: {len(docs)}")
 
# Análisis de los datos cargados
productos = set()
clientes = set()
ventas_por_fecha = {}
 
for doc in docs[:10]:  # Mostrar primeros 10 registros
    print(f"\nRegistro: {doc.page_content}")
    print(f"Metadatos: {doc.metadata}")
    
    # Recopilar estadísticas
    if 'fecha' in doc.metadata:
        fecha = doc.metadata['fecha']
        ventas_por_fecha[fecha] = ventas_por_fecha.get(fecha, 0) + 1
    
    if 'cliente' in doc.metadata:
        clientes.add(doc.metadata['cliente'])
 
print(f"\nResumen de datos:")
print(f"  Clientes únicos: {len(clientes)}")
print(f"  Fechas con ventas: {len(ventas_por_fecha)}")
print(f"  Promedio de ventas por día: {len(docs) / len(ventas_por_fecha):.1f}")