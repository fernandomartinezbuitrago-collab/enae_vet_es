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

api_key = os.getenv("GOOGLE_API_KEY")
calendar_api_key = os.getenv("CALENDAR_API_KEY")
calendar_id = "c1a485b2e53f83061613ed9bcf992486abe82de9d4d0df653e0e50a5c0d61d8f@group.calendar.google.com"

# --- VET-13: Herramienta de Calendario Real ---
@tool
def comprobar_disponibilidad(fecha: str) -> str:
    """Consulta la agenda real de la clínica. Formato: YYYY-MM-DD."""
    if not calendar_api_key: return "Error de configuración de la agenda."
    try:
        cal_encoded = urllib.parse.quote(calendar_id)
        t_min, t_max = f"{fecha}T08:00:00Z", f"{fecha}T14:00:00Z"
        url = f"https://www.googleapis.com/calendar/v3/calendars/{cal_encoded}/events?key={calendar_api_key}&timeMin={t_min}&timeMax={t_max}&singleEvents=true"
        res = requests.get(url)
        if res.status_code != 200: return "No hay conexión con el calendario."
        items = res.json().get("items", [])
        if len(items) >= 2: # Regla del Tetris [cite: 102, 105]
            return f"El día {fecha} está completo (máximo 2 citas)."
        return f"El día {fecha} tiene {2 - len(items)} hueco(s) libre(s)."
    except Exception as e:
        return f"Error técnico: {str(e)}"

# --- CONFIGURACIÓN ESTABLE (GEMINI PRO) ---
llm = ChatGoogleGenerativeAI(
    model="gemini-pro", 
    google_api_key=api_key,
    temperature=0.1,
    convert_system_message_to_human=True # Vital para modelos antiguos
)

tools = [comprobar_disponibilidad]

# --- VET-11: RAG (URL Oficial) ---
try:
    contexto_rag = WebBaseLoader("https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation").load()[0].page_content[:4000]
except:
    contexto_rag = "Ayuno sólido: 8-12h. Agua: hasta 2h antes. [cite: 34, 35]"

# --- SDD: Prompt con Reglas de Negocio ---
prompt = ChatPromptTemplate.from_messages([
    ("system", f"""Eres el asistente de la Clínica Veterinaria. Hoy es {datetime.date.today()}.
    
    REGLAS DE NEGOCIO:
    1. AYUNO: 8-12h sólidos, agua hasta 2h antes[cite: 34, 35].
    2. EDAD: >6 años analítica OBLIGATORIA[cite: 30].
    3. CELO: Perras no; esperar 2 meses[cite: 19].
    4. ENTREGAS: Gatos (08:00-09:00), Perros (09:00-10:30)[cite: 111].
    5. AGENDA: Solo operamos de Lunes a Jueves[cite: 82]. Usa 'comprobar_disponibilidad'.
    
    Contexto RAG: {contexto_rag}"""),
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
    except Exception:
        return {"response": "Lo siento, el sistema está saturado. Reintenta en unos segundos."}