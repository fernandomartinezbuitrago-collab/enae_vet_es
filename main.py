import os
import requests
import datetime
import urllib.parse
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
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent

# 1. Cargar variables de entorno (SALTÁNDONOS VERCEL POR COMPLETO)
load_dotenv()

api_key = "AIzaSyCdpYOFXMR-SQECA0mldSoQPbeosat3Zno" 
calendar_api_key = "AIzaSyAyKMcZQh2M4pJsvQ3TaTGm4PLIrNKWCAU" 
calendar_id = "c1a485b2e53f83061613ed9bcf992486abe82de9d4d0df653e0e50a5c0d61d8f@group.calendar.google.com"

# ESTO OBLIGA A LA IA A USAR ESTA LLAVE SÍ O SÍ (mata el error 403)
os.environ["GOOGLE_API_KEY"] = api_key

if api_key:
    genai.configure(api_key=api_key)

# Inicializar FastAPI (SOLO UNA VEZ)
app = FastAPI(title="Chatbot Clínica Veterinaria - PRO")
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
# 🔥 INICIO: INTEGRACIÓN CON CALENDARIO REAL (VET-13)
# ==========================================
@tool
def comprobar_disponibilidad(fecha: str, hora: str) -> str:
    """
    IMPORTANTE: Úsala para comprobar disponibilidad en la agenda de la clínica.
    La 'fecha' DEBE estar en formato YYYY-MM-DD.
    La 'hora' DEBE estar en formato HH:MM.
    """
    if not calendar_id:
        return "DILE AL USUARIO: Error interno, el ID del calendario no está configurado en Vercel."
    
    try:
        # Limpiar la hora por si el usuario escribe "10.00" o "12"
        hora_limpia = hora.replace(".", ":")
        if ":" not in hora_limpia:
            hora_limpia += ":00"
            
        hora_int = int(hora_limpia.split(":")[0])
        if hora_int < 9 or hora_int >= 20:
            return "DILE AL USUARIO: Fuera de horario. La clínica solo atiende de 09:00 a 20:00."

        # Codificar el ID del calendario (vital si es un email con @)
        cal_seguro = urllib.parse.quote(calendar_id)
        
        # Consultar la API oficial de Google Calendar CON SU LLAVE CORRECTA
        url = f"https://www.googleapis.com/calendar/v3/calendars/{cal_seguro}/events?key={calendar_api_key}&timeMin={fecha}T00:00:00Z&timeMax={fecha}T23:59:59Z&singleEvents=true"
        
        respuesta = requests.get(url)
        
        # EL CHIVATO: Si Google nos bloquea, obligamos al bot a darnos el código exacto
        if respuesta.status_code != 200:
            return f"DILE AL USUARIO LITERALMENTE ESTO: Error de Google API - HTTP {respuesta.status_code}: {respuesta.text}"
        
        eventos = respuesta.json().get("items", [])
        
        ocupado = False
        for evento in eventos:
            inicio_evento = evento.get("start", {}).get("dateTime", "")
            if hora_limpia in inicio_evento:
                ocupado = True
                break
                
        if ocupado:
            return f"Lo siento, a las {hora_limpia} el {fecha} la agenda está OCUPADA."
        else:
            return f"¡Buenas noticias! El {fecha} a las {hora_limpia} el calendario está LIBRE."
            
    except Exception as e:
        return f"DILE AL USUARIO LITERALMENTE ESTO: Error de Python: {str(e)}"

# Herramientas del agente
tools = [comprobar_disponibilidad]

# ==========================================
# 🔥 FIN DE INTEGRACIÓN
# ==========================================

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)

URL_OFICIAL = "https://es.wikipedia.org/wiki/Castraci%C3%B3n" 
try:
    loader = WebBaseLoader(URL_OFICIAL)
    docs = loader.load()
    texto_fuente = docs[0].page_content[:15000]
    
    # Inyectamos la fecha real de HOY en el cerebro de la IA
    hoy = datetime.date.today().strftime("%Y-%m-%d")
    mensaje_sistema = f"""Eres un asistente de una clínica veterinaria.
    HOY ES: {hoy}. Usa esta fecha para calcular cuándo es 'mañana' o 'el próximo martes'.
    
    Reglas:
    1. Para dudas médicas, responde basándote en la INFORMACIÓN OFICIAL.
    2. Si preguntan disponibilidad de citas, usa la herramienta 'comprobar_disponibilidad'. No te inventes las horas.
    
    INFORMACIÓN OFICIAL:
    {texto_fuente}
    """
except Exception as e:
    hoy = datetime.date.today().strftime("%Y-%m-%d")
    mensaje_sistema = f"Eres un asistente veterinario. Hoy es {hoy}. La fuente falló, pero puedes usar tus herramientas para buscar citas."

prompt_template = ChatPromptTemplate.from_messages([
    ("system", mensaje_sistema),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

conversational_chain = RunnableWithMessageHistory(
    agent_executor, get_session_history,
    input_messages_key="input", history_messages_key="history"
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
        return {"response": respuesta_ia["output"], "status": "success"}
    except Exception as e:
        return {"response": f"Error del sistema: {str(e)}", "status": "error"}