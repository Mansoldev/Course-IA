from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

print("Modelos disponibles para embeddings en tu cuenta:")
for m in client.models.list():
    # Comprobar si el modelo soporta generar embeddings
    if hasattr(m, 'supported_actions') and 'embedContent' in m.supported_actions:
        print(f"- {m.name}")