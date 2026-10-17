from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

class AnalisisTexto(BaseModel):
    resumen: str = Field(description="Resumen breve del texto")
    sentimiento: str = Field(description="Sentimiento del texto (positivo, negativo o neutro)")
    palabras_clave: list[str] = Field(description="Lista de palabras clave del texto")

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0.6)

structured_llm = llm.with_structured_output(AnalisisTexto)

texto_prueba = "Me encantó la nueva película de acción, tiene muchos efectos especiales y emoción"

resultado = structured_llm.invoke(f"Analiza el siguiente texto: {texto_prueba}")
print(resultado.model_dump_json(indent=4))