from langchain_community.document_loaders import YoutubeLoader
import re

# NO VA
# Extrae transcripciones automáticas de videos de YouTube.
# Casos de uso ideales:
# - Análisis de contenido educativo
# - Transcripción de conferencias
# - Análisis de tendencias en videos
# - Creación de resúmenes automáticos
 
# Cargar transcripción de un video educativo
video_url = "https://www.youtube.com/watch?v=A2sWWJj3kXo"
loader = YoutubeLoader.from_youtube_url(
    video_url,
    add_video_info=True,
    language=['es', 'en'],  # Priorizar idiomas
    translation='es'        # Traducir si es necesario
)
 
try:
    docs = loader.load()
    video_info = docs[0].metadata
    transcript = docs[0].page_content
    
    print("=== INFORMACIÓN DEL VIDEO ===")
    print(f"Título: {video_info.get('title', 'N/A')}")
    print(f"Autor: {video_info.get('author', 'N/A')}")
    print(f"Duración: {video_info.get('length', 'N/A')} segundos")
    print(f"Fecha de publicación: {video_info.get('publish_date', 'N/A')}")
    print(f"Vistas: {video_info.get('view_count', 'N/A')}")
    
    print(f"\n=== ANÁLISIS DE TRANSCRIPCIÓN ===")
    print(f"Longitud de transcripción: {len(transcript):,} caracteres")
    print(f"Palabras aproximadas: {len(transcript.split()):,}")
    
    # Extraer temas principales (palabras frecuentes)
    words = re.findall(r'\b[a-záéíóúñ]{4,}\b', transcript.lower())
    from collections import Counter
    common_words = Counter(words).most_common(10)
    
    print("\nPalabras más frecuentes:")
    for word, count in common_words:
        print(f"  {word}: {count} veces")
        
    print(f"\nPrimeros 500 caracteres:")
    print(transcript[:500] + "...")
    
except Exception as e:
    print(f"Error al cargar el video: {e}")