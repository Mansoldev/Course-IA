# from langchain_openai import ChatOpenAI With openAI
# llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

from langchain_google_genai import ChatGoogleGenerativeAI #models: gemini-3.1-flash-lite, gemini-3.5-flash-lite, gemini-3.8-flash
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Instanciar el modelo
chat = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0.7)

# 2. Definir la plantilla
template = PromptTemplate(
    input_variables=["nombre"],
    template="Saluda al usuario con su nombre.\nNombre del usuario: {nombre}\nAsistente:",
)

# 3. Crear la cadena con LCEL (Prompt | Modelo | Parseador de texto)
chain = template | chat | StrOutputParser()

# 4. Invocación mediante .invoke() pasando un diccionario con la variable
result = chain.invoke({"nombre": "Juan"})

print(result)

