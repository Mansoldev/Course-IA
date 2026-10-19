from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Configuración de modelos
EMBEDDING_MODEL = "gemini-embedding-001"#"text-embedding-3-large"
QUERY_MODEL = "gemini-3.5-flash-lite"#"gpt-4o-mini"gemini-3.1-flash-lite
GENERATION_MODEL = "gemini-3.5-flash-lite"#"gpt-4o"

# Configuración del vector store
CHROMA_DB_PATH = str(BASE_DIR / "chroma_db")

# Configuración del retriever
SEARCH_TYPE = "mmr"
MMR_DIVERSITY_LAMBDA = 0.7
MMR_FETCH_K = 20
SEARCH_K = 2

# Configuracion alternativa para retriever hibrido
ENABLE_HYBRID_SEARCH = True
SIMILARITY_THRESHOLD = 0.70