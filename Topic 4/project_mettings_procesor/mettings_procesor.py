from langgraph.graph import StateGraph, START, END
#from langchain_openai import ChatOpenAI
#import openai  # Para transcripción Whisper
from typing import TypedDict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from google import genai
from langchain_core.output_parsers import StrOutputParser
from tkinter import filedialog

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0.3)
chain = llm | StrOutputParser()

class State(TypedDict):
    notes: str
    participants: List[str]
    topics: List[str]
    action_items: List[str]
    minutes: str
    summary: str

  
def extract_participants(state: State) -> State:
    prompt = f"""
    Analiza las siguientes notas de reunión y extrae únicamente los nombres de los participantes.    Notas: {state['notes']}    Instrucciones:
    - Responde SOLO con nombres separados por comas
    - No incluyas explicaciones adicionales
    - Formato: Juan García, María López, Carlos Ruiz
    """    
    response = chain.invoke(prompt)
    participants = [p.strip() for p in response.split(',') if p.strip()]    
    return {'participants': participants}

def extract_principal_topics(state: State) -> State:
    prompt = f"""
    Analiza las siguientes notas de reunión y extrae únicamente los temas principales discutidos.    Notas: {state['notes']}    Instrucciones:
    - Responde SOLO con temas separados por punto y coma
    - Incluye solo entre 3 y 5 temas principales
    - Formato: empleados; productividad; innovación
    """    
    response = chain.invoke(prompt)
    topics = [p.strip() for p in response.split(';') if p.strip()]    
    return {'topics': topics}

def extract_actions_with_responsable(state: State) -> State:
    prompt = f"""
    Analiza las siguientes notas de reunión y extrae únicamente las acciones acordadas, cada una junto con el responsable de realizarla.    Notas: {state['notes']}    Instrucciones:
    - Responde SOLO con acciones separadas por pipes | cada acción seguida del responsable entre paréntesis
    - Formato: repartir panfletos (Juan García) | organizar reunión (María López) | enviar informe (Carlos Ruiz)
    """    
    response = chain.invoke(prompt)
    actions = [p.strip() for p in response.split('|') if p.strip()]    
    return {'action_items': actions}

def extract_minutes(state: State) -> State:
    prompt = f"""
    Analiza las siguientes notas de reunión y extrae únicamente una Minuta formal de reunión.    Notas: {state['notes']}    Instrucciones:
    - Responde máximo 150 palabras
    - Formato: Minuta formal de reunión
    """    
    response = chain.invoke(prompt)
    minutes = response.strip()
    return {'minutes': minutes}

def extract_summary(state: State) -> State:
    prompt = f"""
    Analiza las siguientes notas de reunión y extrae únicamente un resumen ejecutivo conciso.    Notas: {state['notes']}    Instrucciones:
    - Responde máximo 30 palabras
    - Formato: Resumen ejecutivo conciso
    """    
    response = chain.invoke(prompt)
    summary = response.strip()  
    return {'summary': summary}

def create_workflow():
    workflow = StateGraph(State)

    workflow.add_node("extract_participants", extract_participants)
    workflow.add_node("extract_topics", extract_principal_topics)
    workflow.add_node("extract_actions", extract_actions_with_responsable)
    workflow.add_node("extract_minutes", extract_minutes)
    workflow.add_node("extract_summary", extract_summary)
  
    # Añadir resto de nodos    
    workflow.add_edge(START, "extract_participants")
    workflow.add_edge("extract_participants", "extract_topics")
    workflow.add_edge("extract_topics", "extract_actions")
    workflow.add_edge("extract_actions", "extract_minutes")
    workflow.add_edge("extract_minutes", "extract_summary")
    workflow.add_edge("extract_summary", END)

    # Definir resto del flujo    
    return workflow.compile()

def transcribe_media(file_path: str) -> str:
    client = genai.Client()
    audio_file = client.files.upload(file=file_path)
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[audio_file, "Transcribe el audio en español."]
    )
    
    return response.text

  
if __name__ == "__main__":
    app = create_workflow()    
    test_state = {
        'notes': "Reunión con Juan García y María López sobre el proyecto...",
        'participants': [],
        'topics': [],
        'action_items': [],
        'minutes': '',
        'summary': ''
    }    

    result = app.invoke(test_state)
    print(result)