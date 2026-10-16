# from langchain_openai import ChatOpenAI With openAI
# llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

from langchain_google_genai import ChatGoogleGenerativeAI #models: gemini-3.1-flash-lite, gemini-3.5-flash-lite, gemini-3.8-flash
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0.7)

pregunta = "¿En que año llegó el ser humano a la luna por primera vez?"
print("Pregunta: ", pregunta)

respuesta = llm.invoke(pregunta)
# Si la respuesta devuelve una lista de diccionarios/bloques:
if isinstance(respuesta.content, list):
    texto_limpio = respuesta.content[0]['text']
else:
    texto_limpio = respuesta.content

print("Respuesta: ", texto_limpio)

