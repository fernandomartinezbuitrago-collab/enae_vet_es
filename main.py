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

# 1. Cargar variables de entorno (LIMPIO Y SEGURO PARA VERCEL)
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
calendar_api_key = os.getenv("CALENDAR_API_KEY")
calendar_id = "c1a485b2e53f83061613ed9bcf992486abe82de9d4d0df653e0e50a5c0d61d8f@group.calendar.google.com"

if api_key:
    genai.configure(api_key=api_key)

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
# 🔥 INTEGRACIÓN CON CALENDARIO (VET-13)
# ==========================================
@tool
def comprobar_disponibilidad(fecha: str, hora: str) -> str:
    """
    IMPORTANTE: Úsala para comprobar disponibilidad en la agenda de la clínica.
    La 'fecha' DEBE estar en formato YYYY-MM-DD.
    La 'hora' DEBE estar en formato HH:MM.
    """
    if not calendar_id:
        return "DILE AL USUARIO: Error interno con el ID del calendario."
    
    try:
        hora_limpia = hora.replace(".", ":")
        if ":" not in hora_limpia:
            hora_limpia += ":00"
            
        hora_int = int(hora_limpia.split(":")[0])
        if hora_int < 9 or hora_int >= 20:
            return "DILE AL USUARIO: Fuera de horario. La clínica atiende de 09:00 a 20:00."

        cal_seguro = urllib.parse.quote(calendar_id)
        url = f"https://www.googleapis.com/calendar/v3/calendars/{cal_seguro}/events?key={calendar_api_key}&timeMin={fecha}T00:00:00Z&timeMax={fecha}T23:59:59Z&singleEvents=true"
        
        respuesta = requests.get(url)
        
        if respuesta.status_code != 200:
            return f"Error técnico (Código {respuesta.status_code}). Avise al soporte."
        
        eventos = respuesta.json().get("items", [])
        ocupado = any(hora_limpia in ev.get("start", {}).get("dateTime", "") for ev in eventos)
                
        if ocupado:
            return f"Lo siento, a las {hora_limpia} el {fecha} la agenda está OCUPADA."
        return f"¡Buenas noticias! El {fecha} a las {hora_limpia} el calendario está LIBRE."
            
    except Exception as e:
        return f"Error de sistema: {str(e)}"

tools = [comprobar_disponibilidad]

# ==========================================
# 🧠 CEREBRO Y RAG (URL OBLIGATORIA +1 PT)
# ==========================================
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)

# CAMBIO CRÍTICO: Fuente exigida por el profesor para el punto extra
URL_RAG_OBLIGATORIA = "https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation" 

try:
    loader = WebBaseLoader(URL_RAG_OBLIGATORIA)
    docs = loader.load()
    texto_fuente = docs[0].page_content[:15000]
    hoy = datetime.date.today().strftime("%Y-%m-%d")
    
    mensaje_sistema = f"""Eres un asistente de una clínica veterinaria. Hoy es {hoy}.
    
    INSTRUCCIONES PREOPERATORIAS (RAG):
    {texto_fuente}
    
    REGLAS:
    1. Responde dudas médicas solo con la información anterior.
    2. Usa 'comprobar_disponibilidad' para citas.
    3. Mantén la memoria del paciente (perro/gato, edad).
    """
except Exception:
    hoy = datetime.date.today().strftime("%Y-%m-%d")
    mensaje_sistema = f"Asistente veterinario. Hoy es {hoy}. Usa tus herramientas para citas."

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