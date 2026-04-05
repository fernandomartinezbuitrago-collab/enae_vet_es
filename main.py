import os
from typing import Dict
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.document_loaders import WebBaseLoader

# NUEVAS IMPORTACIONES PARA AGENTES Y HERRAMIENTAS
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent

# 1. Cargar variables de entorno
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

app = FastAPI(title="Chatbot Clínica Veterinaria - Agente con Tools")
templates = Jinja2Templates(directory="templates")

class ChatMessage(BaseModel):
    session_id: str
    message: str

store: Dict[str, InMemoryChatMessageHistory] = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    if len(store[session_id].messages) > 10:
        store[session_id].messages = store[session_id].messages[-10:]
    return store[session_id]

# ==========================================
# 🔥 INICIO DE MOCK TOOL (Ticket VET-12)
# ==========================================
@tool
def comprobar_disponibilidad(fecha: str, hora: str) -> str:
    """
    IMPORTANTE: Úsala SIEMPRE que el usuario quiera pedir cita o pregunte por disponibilidad.
    Consulta la disponibilidad de la clínica simulando una base de datos.
    Requiere una fecha y una hora aproximada.
    """
    # Contrato de E/S simulado (Criterios de Aceptación)
    if "10" in hora:
        return "Resultado de la BBDD: DISPONIBLE. Hay un hueco libre a esa hora."
    elif "11" in hora:
        return "Resultado de la BBDD: NO DISPONIBLE. La agenda está totalmente llena."
    else:
        return "Resultado de la BBDD: ERROR. El sistema de agenda está caído o la hora es inválida."

# Añadimos nuestra herramienta a la "caja de herramientas" de la IA
tools = [comprobar_disponibilidad]
# ==========================================
# 🔥 FIN DE MOCK TOOL
# ==========================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=api_key
)

URL_OFICIAL = "https://es.wikipedia.org/wiki/Castraci%C3%B3n" 
try:
    loader = WebBaseLoader(URL_OFICIAL)
    docs = loader.load()
    texto_fuente = docs[0].page_content[:15000]
    
    # Modificamos el prompt para que sepa cuándo usar RAG y cuándo usar Tools
    mensaje_sistema = f"""Eres un asistente de una clínica veterinaria.
    Reglas de comportamiento:
    1. Para dudas médicas, responde EXCLUSIVAMENTE basándote en la INFORMACIÓN OFICIAL. Si no está, di que no lo sabes.
    2. Si el usuario quiere consultar disponibilidad o pedir cita, NO mires la información oficial. USA INMEDIATAMENTE la herramienta 'comprobar_disponibilidad'.
    
    INFORMACIÓN OFICIAL:
    {texto_fuente}
    """
except Exception as e:
    mensaje_sistema = "Eres un asistente de clínica. La fuente falló, pero puedes usar tus herramientas para buscar citas."

prompt_template = ChatPromptTemplate.from_messages([
    ("system", mensaje_sistema),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"), # ESPACIO PARA QUE LA IA "PIENSE" AL USAR TOOLS
])

# En lugar de una cadena básica, creamos un "Agente"
agent = create_tool_calling_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

conversational_chain = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/chat/test")
async def chat_test(chat_msg: ChatMessage):
    try:
        respuesta_ia = conversational_chain.invoke(
            {"input": chat_msg.message},
            config={"configurable": {"session_id": chat_msg.session_id}}
        )
        # ⚠️ IMPORTANTE: Un Agente devuelve un diccionario con "output", no "content"
        return {"response": respuesta_ia["output"], "status": "success"}
    except Exception as e:
        return {"response": f"Error del sistema: {str(e)}", "status": "error"}