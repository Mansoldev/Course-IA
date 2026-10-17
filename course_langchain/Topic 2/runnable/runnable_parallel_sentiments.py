from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
import json
 
# Configuración del modelo
llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0)
output_parser = StrOutputParser()

def preprocess_text(text):
    """Limpia el texto eliminando espacios extras y limitando longitud"""
    return text.strip()[:500]
 
# Convertir la función en un Runnable
preprocessor = RunnableLambda(preprocess_text)

def generate_summary(text):
    """Genera un resumen conciso del texto"""
    prompt = f"Resume en una sola oración: {text}"
    # response = llm.invoke(prompt) # No devuelve texto google
    # return response.content
    chain = llm | output_parser
    return chain.invoke(prompt)

summary_branch = RunnableLambda(generate_summary)

def analyze_sentiment(text):
    """Analiza el sentimiento y devuelve resultado estructurado"""
    prompt = f"""Analiza el sentimiento del siguiente texto.
    Responde ÚNICAMENTE en formato JSON válido:
    {{"sentimiento": "positivo|negativo|neutro", "razon": "justificación breve"}}
    
    Texto: {text}"""

    chain = llm | output_parser
    response_str = chain.invoke(prompt)
    
    # Limpieza de posibles etiquetas markdown de código ```json ... ```
    cleaned_json = response_str.replace("```json", "").replace("```", "").strip()
    
    try:
        return json.loads(cleaned_json)
    except json.JSONDecodeError:
        return {"sentimiento": "neutro", "razon": "Error en análisis"}

sentiment_branch = RunnableLambda(analyze_sentiment)

def merge_results(data):
    """Combina los resultados de ambas ramas en un formato unificado"""
    return {
        "resumen": data["resumen"],
        "sentimiento": data["sentimiento_data"]["sentimiento"],
        "razon": data["sentimiento_data"]["razon"]
    }

merger = RunnableLambda(merge_results)

# def process_one(t):
#     resumen = generate_summary(t)              # Llamada 1 al LLM
#     sentimiento_data = analyze_sentiment(t)    # Llamada 2 al LLM
#     return merge_results({
#         "resumen": resumen,
#         "sentimiento_data": sentimiento_data
#     })
# Convertir en Runnable
# process = RunnableLambda(process_one)

parallel_analisis = RunnableParallel({
    "resumen": summary_branch,
    "sentimiento_data": sentiment_branch
})

# La cadena completa con procesamiento paralelo
chain = preprocessor | parallel_analisis | merger

# Prueba con diferentes textos
textos_prueba = [
    "¡Me encanta este producto! Funciona perfectamente y llegó muy rápido.",
    "El servicio al cliente fue terrible, nadie me ayudó con mi problema.",
    "El clima está nublado hoy, probablemente llueva más tarde."
]

# Procesar cada texto y mostrar resultados
# for texto in textos_prueba:
#     resultado = chain.invoke(texto)
#     print(f"Texto: {texto}")
#     print(f"Resultado: {resultado}")
#     print("-" * 50)

# Procesamiento en bloque, mejor gestion de llamadas al LLM
resultado_batch = chain.batch(textos_prueba)

print(resultado_batch)