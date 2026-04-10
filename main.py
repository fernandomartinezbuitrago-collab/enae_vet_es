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

# 1. Cargar variables y configurar Google
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
calendar_api_key = os.getenv("CALENDAR_API_KEY")
calendar_id = "c1a485b2e53f83061613ed9bcf992486abe82de9d4d0df653e0e50a5c0d61d8f@group.calendar.google.com"

if api_key:
    genai.configure(api_key=api_key)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class ChatMessage(BaseModel):
    session_id: str
    message: str

store: Dict[str, InMemoryChatMessageHistory] = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# 2. Herramienta de Calendario (Punto Extra)
@tool
def comprobar_disponibilidad(fecha: str, hora: str) -> str:
    """Consulta si hay hueco en la clínica. Fecha: YYYY-MM-DD, Hora: HH:MM."""
    try:
        cal_seguro = urllib.parse.quote(calendar_id)
        url = f"https://www.googleapis.com/calendar/v3/calendars/{cal_seguro}/events?key={calendar_api_key}&timeMin={fecha}T00:00:00Z&timeMax={fecha}T23:59:59Z&singleEvents=true"
        
        res = requests.get(url)
        if res.status_code != 200:
            return f"Error de conexión con la agenda (Código {res.status_code})."
        
        items = res.json().get("items", [])
        h_limpia = hora.replace(".", ":")
        if ":" not in h_limpia: h_limpia += ":00"
        
        ocupado = any(h_limpia in ev.get("start", {}).get("dateTime", "") for ev in items)
        
        if ocupado:
            return f"Lo siento, a las {h_limpia} el {fecha} ya está ocupado."
        return f"¡Buenas noticias! El {fecha} a las {h_limpia} el calendario está LIBRE."
    except Exception as e:
        return f"Error técnico en la herramienta: {str(e)}"

# 3. Configuración del Agente
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)
tools = [comprobar_disponibilidad]

# RAG Obligatorio (Punto Extra)
URL_RAG = "https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation"
try:
    loader = WebBaseLoader(URL_RAG)
    docs = loader.load()
    contexto = docs[0].page_content[:10000]
except:
    contexto = "No se pudo cargar la información de ayuno. Use reglas generales."

hoy = datetime.date.today().strftime("%Y-%m-%d")

prompt = ChatPromptTemplate.from_messages([
    ("system", f"""Eres un asistente veterinario experto. Hoy es {hoy}.
    Información de apoyo (RAG): {contexto}
    
    Reglas de oro:
    1. Si te preguntan por citas, usa SIEMPRE 'comprobar_disponibilidad'.
    2. Si el animal tiene >6 años, avisa que necesita analítica[cite: 53].
    3. Si está en celo, explica que no se puede operar ahora[cite: 55].
    """),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

chain = RunnableWithMessageHistory(
    executor, get_session_history,
    input_messages_key="input", history_messages_key="history"
)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/chat/test")
async def chat(msg: ChatMessage):
    try:
        res = chain.invoke(
            {"input": msg.message},
            config={"configurable": {"session_id": msg.session_id}}
        )
        return {"response": res["output"]}
    except Exception as e:
        return {"response": f"Error del servidor: {str(e)}"}