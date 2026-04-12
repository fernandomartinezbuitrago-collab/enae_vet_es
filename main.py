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

# Configuración de Identificadores (VET-1)
api_key = os.getenv("GOOGLE_API_KEY")
calendar_api_key = os.getenv("CALENDAR_API_KEY")
calendar_id = "c1a485b2e53f83061613ed9bcf992486abe82de9d4d0df653e0e50a5c0d61d8f@group.calendar.google.com"

# --- VET-13: Herramienta de Calendario Real (Reglas Sesión 1) ---
@tool
def comprobar_disponibilidad(fecha: str) -> str:
    """Consulta la agenda de la clínica. Formato: YYYY-MM-DD.
    Límite: Máximo 2 cirugías por día (Regla del Tetris)."""
    if not calendar_api_key: return "Error: API Key de calendario no configurada."
    try:
        cal_encoded = urllib.parse.quote(calendar_id)
        # Ventana quirúrgica: 09:00 a 13:00 [cite: 82]
        t_min, t_max = f"{fecha}T08:00:00Z", f"{fecha}T14:00:00Z"
        url = f"https://www.googleapis.com/calendar/v3/calendars/{cal_encoded}/events?key={calendar_api_key}&timeMin={t_min}&timeMax={t_max}&singleEvents=true"
        
        res = requests.get(url)
        if res.status_code != 200: return "No se puede acceder a la agenda ahora mismo."
        
        items = res.json().get("items", [])
        # Regla: Máximo 2 perros/citas por día [cite: 105]
        if len(items) >= 2:
            return f"El día {fecha} está COMPLETO (cupo de 2 mascotas alcanzado)."
        
        return f"El día {fecha} está DISPONIBLE. Tenemos {2 - len(items)} hueco(s) libre(s)."
    except Exception as e:
        return f"Error técnico en Calendar: {str(e)}"

# --- SOLUCIÓN AL 404: Configuración Robusta ---
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", # Modelo estándar con capa gratuita
    google_api_key=api_key,
    temperature=0.1
)

tools = [comprobar_disponibilidad]

# --- VET-11: RAG (Instrucciones Preoperatorias) ---
try:
    contexto_rag = WebBaseLoader("https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation").load()[0].page_content[:4000]
except:
    contexto_rag = "Ayuno sólido: 8-12h[cite: 34]. Agua: hasta 2h antes[cite: 35]."

# --- SDD: Prompt con Reglas de Negocio Reales ---
prompt = ChatPromptTemplate.from_messages([
    ("system", f"""Eres el asistente experto de la Clínica Veterinaria. Hoy es {datetime.date.today()}.
    
    INSTRUCCIONES PREOPERATORIAS (RAG):
    {contexto_rag}
    
    REGLAS OBLIGATORIAS (SDD):
    1. AYUNO: Sólidos 8-12h antes[cite: 34]. Agua hasta 1-2h antes[cite: 35].
    2. EDAD: Si el animal tiene >6 años, analítica preoperatoria OBLIGATORIA[cite: 30].
    3. CELO: Gatas OK[cite: 18]. Perras NO; esperar 2 meses tras el fin del celo[cite: 19].
    4. ENTREGAS: Gatos (08:00-09:00) [cite: 111, 113], Perros (09:00-10:30)[cite: 111, 117].
    5. AGENDA: Usa 'comprobar_disponibilidad' para confirmar fechas. Solo operamos Lunes a Jueves[cite: 82].
    """),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

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
        return {"response": f"Error del sistema: {str(e)}"}