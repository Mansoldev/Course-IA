import os
import numpy as np
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

# Instanciar el modelo de embeddings de Google - VER EMBEDDINGS_LISTAR_GOOGLE.PY PARA VER LOS MODELOS DISPONIBLES
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

texto1 = "La capital de Francia es París."
texto2 = "París es un nombre común para mascotas."

# Generar vectores de embedding para cada consulta
vec1 = embeddings.embed_query(texto1)
vec2 = embeddings.embed_query(texto2)

print(f"Dimensión de los vectores: {len(vec1)}")

# Cálculo de similitud coseno
cos_sim = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

print(f"Similitud coseno entre vec1 y vec2: {cos_sim:.3f}")