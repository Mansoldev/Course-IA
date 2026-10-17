from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

template = "Eres un experto en marketing. Sugiere un eslogan creativo para un producto {producto}"

prompt = PromptTemplate(
    input_variables=["producto"],
    template=template
)

# prompt_lleno = prompt.format(producto="zapatos deportivos")
# print(prompt_lleno) 

# Con ChatPromptTemplate
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un traductor del español al inglés muy preciso."),
    ("human", "{texto}.")
])

mensajes = chat_prompt.format_messages(texto="Hola mundo, ¿cómo estás?")
for m in mensajes:
    print(f"{type(m)}: {m.content}")