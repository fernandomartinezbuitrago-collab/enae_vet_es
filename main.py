import os
import datetime
import urllib.parse
import requests
from typing import Dict
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent

load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Configuración del Caso (Sesión 1 y 2)
api_key = os.getenv("GOOGLE_API_KEY")
calendar_api_key = os.getenv("CALENDAR_API_KEY")
calendar_id = "c1a485b2e53f83061613ed9bcf992486abe82de9d4d0df653e0e50a5c0d61d8f@group.calendar.google.com"

# --- VET-13: Lógica de Agenda "El Tetris" ---
@tool
def comprobar_disponibilidad(fecha: str) -> str:
    """Verifica si hay cupo quirúrgico (máx 2 perros o 240 min). fecha: YYYY-MM-DD."""
    if not calendar_api_key: return "Error: Configuración de API ausente."
    try:
        cal_encoded = urllib.parse.quote(calendar_id)
        # Ventana quirúrgica: 09:00 a 13:00 [cite: 82]
        t_min, t_max = f"{fecha}T08:00:00Z", f"{fecha}T14:00:00Z"
        url = f"https://www.googleapis.com/calendar/v3/calendars/{cal_encoded}/events?key={calendar_api_key}&timeMin={t_min}&timeMax={t_max}&singleEvents=true"
        
        res = requests.get(url)
        if res.status_code != 200: return "Agenda no disponible temporalmente."
        
        eventos = res.json().get("items", [])
        
        # Regla de Negocio: Máximo 2 perros por día [cite: 105]
        if len(eventos) >= 2:
            return f"El día {fecha} está COMPLETO. Ya hay 2 mascotas programadas."
        
        return f"El día {fecha} tiene disponibilidad. Hay {2 - len(eventos)} hueco(s) libre(s)."
    except Exception as e:
        return f"Error en calendario: {str(e)}"

# --- SOLUCIÓN AL ERROR 404 (Models/v1beta) ---
# Forzamos v1 y el modelo flash estable
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=api_key,
    version="v1",  # CRÍTICO: Esto elimina el error de v1beta
    temperature=0.1
)

tools = [comprobar_disponibilidad]

# --- VET-11: RAG Obligatorio ---
try:
    contexto_rag = WebBaseLoader("https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation").load()[0].page_content[:4000]
except:
    contexto_rag = "Ayuno 8-12h sólido. Agua hasta 2h antes."

# --- SDD: Prompt Definitivo ---
prompt = ChatPromptTemplate.from_messages([
    ("system", f"""Eres el asistente de la Clínica Veterinaria (ENAE). Hoy es {datetime.date.today()}.
    
    REGLAS DEL NEGOCIO (SDD):
    1. AYUNO: Sólidos 8-12h antes. Agua hasta 2h antes[cite: 34, 425].
    2. EDAD: Si es >6 años, analítica OBLIGATORIA[cite: 30, 422].
    3. CELO: No operamos perras en celo; esperar 2 meses[cite: 19, 420].
    4. ENTREGAS: Gatos (08:00-09:00), Perros (09:00-10:30)[cite: 111, 121].
    5. AGENDA: Usa 'comprobar_disponibilidad' antes de confirmar citas.
    
    Contexto RAG: {contexto_rag}"""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Ejecutor del Agente
agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

store: Dict[str, InMemoryChatMessageHistory] = {}
def get_history(session_id: str):
    if session_id not in store: store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chain = RunnableWithMessageHistory(executor, get_history, input_messages_key="input", history_messages_key="history")

class ChatMessage(BaseModel):
    session_id: str
    message: str

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(name="index.html", context={"request": request})

@app.post("/chat/test")
async def chat(msg: ChatMessage):
    try:
        res = chain.invoke({"input": msg.message}, config={"configurable": {"session_id": msg.session_id}})
        return {"response": res["output"]}
    except Exception as e:
        return {"response": f"Error técnico: {str(e)}"}