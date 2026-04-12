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

# LangChain & Google
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

# Configuración de variables
api_key = os.getenv("GOOGLE_API_KEY")
calendar_api_key = os.getenv("CALENDAR_API_KEY")
calendar_id = "c1a485b2e53f83061613ed9bcf992486abe82de9d4d0df653e0e50a5c0d61d8f@group.calendar.google.com"

# 1. Herramienta de Calendario (VET-13)
@tool
def comprobar_disponibilidad(fecha: str) -> str:
    """
    Consulta la agenda real de la clínica para un día específico.
    fecha: Formato YYYY-MM-DD.
    """
    if not calendar_api_key:
        return "Error: CALENDAR_API_KEY no configurada."
    
    try:
        cal_encoded = urllib.parse.quote(calendar_id)
        # Consultamos el día completo para verificar disponibilidad según "El Tetris"
        t_min = f"{fecha}T08:00:00Z"
        t_max = f"{fecha}T14:00:00Z"
        
        url = (f"https://www.googleapis.com/calendar/v3/calendars/{cal_encoded}/events?"
               f"key={calendar_api_key}&timeMin={t_min}&timeMax={t_max}&singleEvents=true")
        
        res = requests.get(url)
        if res.status_code != 200:
            return f"No pude acceder a la agenda. (Status: {res.status_code})"
        
        items = res.json().get("items", [])
        if len(items) >= 2: # Límite simplificado de perros o cirugías mayores
            return f"El día {fecha} ya tiene 2 citas programadas. Está completo según el cupo diario."
        
        return f"Hay huecos disponibles el {fecha}. Recuerda que operamos de Lunes a Jueves."
    except Exception as e:
        return f"Error en la conexión con Calendar: {str(e)}"

# 2. Inicialización del LLM (Solución al error 404)
# Usamos gemini-1.5-flash explícitamente sin prefijos experimentales
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    google_api_key=api_key,
    temperature=0.2 # Menor temperatura para mayor rigor en reglas de negocio [cite: 342]
)

tools = [comprobar_disponibilidad]

# 3. Carga de RAG (VET-11)
URL_RAG = "https://veterinary-clinic-teal.vercel.app/en/docs/instructions-before-operation"
try:
    loader = WebBaseLoader(URL_RAG)
    docs = loader.load()
    contexto_rag = docs[0].page_content[:5000]
except Exception:
    contexto_rag = "Ayuno: 8-12h sólidos. Agua hasta 2h antes. [cite: 34]"

# 4. Prompt con Reglas de Negocio (SDD)
prompt = ChatPromptTemplate.from_messages([
    ("system", f"""Eres el asistente de la Clínica Veterinaria. 
    Tu objetivo es agendar esterilizaciones siguiendo estas reglas estrictas:
    
    REGLAS DE DOMINIO:
    - Ayuno: 8-12 horas de sólidos antes de la cirugía. Agua hasta 2h antes[cite: 34].
    - Edad: Si el animal tiene más de 6 años, la analítica es OBLIGATORIA[cite: 30].
    - Celo: No operamos perras en celo; esperar 2 meses después[cite: 19].
    - Especies: Gatos (entrega 08:00-09:00), Perros (09:00-10:30)[cite: 111].
    - Días quirúrgicos: Lunes a Jueves únicamente[cite: 82].
    
    CONTEXTO ADICIONAL (RAG):
    {contexto_rag}
    
    Hoy es {datetime.date.today()}. Usa la herramienta para verificar fechas."""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 5. Agente y Memoria
agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

store: Dict[str, InMemoryChatMessageHistory] = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chain = RunnableWithMessageHistory(
    executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# 6. Endpoints FastAPI
class ChatMessage(BaseModel):
    session_id: str
    message: str

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(name="index.html", context={"request": request})

@app.post("/chat/test")
async def chat(msg: ChatMessage):
    try:
        # Importante: invoke devuelve un dict con la clave 'output' para agentes
        response = chain.invoke(
            {"input": msg.message},
            config={"configurable": {"session_id": msg.session_id}}
        )
        return {"response": response["output"]}
    except Exception as e:
        return {"response": f"Error del sistema: {str(e)}"}