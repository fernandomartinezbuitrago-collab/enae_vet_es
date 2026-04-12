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

# Credenciales y Configuración
api_key = os.getenv("GOOGLE_API_KEY")
calendar_api_key = os.getenv("CALENDAR_API_KEY")
calendar_id = "c1a485b2e53f83061613ed9bcf992486abe82de9d4d0df653e0e50a5c0d61d8f@group.calendar.google.com"

# --- VET-13: Herramienta de Calendario Real (Reglas de la Sesión 1) ---
@tool
def comprobar_disponibilidad(fecha: str) -> str:
    """Consulta la agenda real. Formato fecha: YYYY-MM-DD. 
    Regla: Máximo 2 perros/cirugías por día."""
    if not calendar_api_key:
        return "Error: API Key de calendario no encontrada."
    
    try:
        cal_encoded = urllib.parse.quote(calendar_id)
        # Ventana quirúrgica: 09:00 a 13:00 [cite: 82]
        t_min = f"{fecha}T08:00:00Z"
        t_max = f"{fecha}T14:00:00Z"
        
        url = (f"https://www.googleapis.com/calendar/v3/calendars/{cal_encoded}/events?"
               f"key={calendar_api_key}&timeMin={t_min}&timeMax={t_max}&singleEvents=true")
        
        res = requests.get(url)
        if res.status_code != 200:
            return f"No se pudo acceder a la agenda (Error {res.status_code})."
        
        eventos = res.json().get("items", [])
        
        # Regla de Negocio "El Tetris": Máximo 2 perros por día [cite: 102, 105]
        if len(eventos) >= 2:
            return f"Lo siento, el {fecha} ya está completo con 2 citas. No hay más cupo quirúrgico."
        
        return f"El {fecha} tiene disponibilidad. Actualmente hay {len(eventos)} cita(s) de 2 posibles."
    except Exception as e:
        return f"Error en la consulta: {str(e)}"

# --- Configuración Gemini 2.0 Flash ---
# Usamos el modelo 2.0 que te funcionó anteriormente
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp", 
    google_api_key=api_key,
    temperature=0.1
)

tools = [comprobar_disponibilidad]

# --- VET-11: RAG (Instrucciones Preoperatorias) ---
URL_RAG = "https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation"
try:
    contexto_rag = WebBaseLoader(URL_RAG).load()[0].page_content[:4000]
except:
    contexto_rag = "Ayuno sólido: 8-12h. Agua: hasta 2h antes."

# --- SDD: System Prompt con Reglas de Negocio ---
prompt = ChatPromptTemplate.from_messages([
    ("system", f"""Eres el asistente experto de la Clínica Veterinaria. Hoy es {datetime.date.today()}.
    
    REGLAS PREOPERATORIAS (RAG):
    {contexto_rag}
    
    POLÍTICAS DE LA CLÍNICA (SDD):
    1. AYUNO: Sólidos 8-12h antes de la operación[cite: 34]. Agua permitida hasta 2h antes[cite: 35].
    2. ANALÍTICA: Obligatoria en animales de más de 6 años[cite: 30].
    3. CELO: Gatas pueden operarse; perras deben esperar 2 meses tras el fin del celo[cite: 18, 19].
    4. ENTREGAS: Gatos (08:00-09:00), Perros (09:00-10:30)[cite: 111].
    5. AGENDA: Siempre usa 'comprobar_disponibilidad' antes de sugerir una fecha. Solo operamos de Lunes a Jueves[cite: 82].
    """),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Agente
agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# Memoria (VET-10)
store: Dict[str, InMemoryChatMessageHistory] = {}
def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chain = RunnableWithMessageHistory(
    executor, get_session_history,
    input_messages_key="input", history_messages_key="history"
)

class ChatMessage(BaseModel):
    session_id: str
    message: str

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(name="index.html", context={"request": request})

@app.post("/chat/test")
async def chat(msg: ChatMessage):
    try:
        response = chain.invoke(
            {"input": msg.message},
            config={"configurable": {"session_id": msg.session_id}}
        )
        return {"response": response["output"]}
    except Exception as e:
        return {"response": f"Error del servidor: {str(e)}"}