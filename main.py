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

# 1. Cargar variables de entorno
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

app = FastAPI(title="Chatbot Clínica Veterinaria - MVP")
templates = Jinja2Templates(directory="templates")

# 2. Modelo de datos actualizado (ahora exige session_id)
class ChatMessage(BaseModel):
    session_id: str
    message: str

# 3. Almacén de memoria en RAM (Diccionario)
store: Dict[str, InMemoryChatMessageHistory] = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    
    # ESTRATEGIA DE CONTROL DE MEMORIA (CAC): Mantener solo los últimos 10 mensajes
    if len(store[session_id].messages) > 10:
        store[session_id].messages = store[session_id].messages[-10:]
        
    return store[session_id]

# 4. Configurar el Cerebro con Memoria
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=api_key
)

# Añadimos un "MessagesPlaceholder" para que LangChain inyecte el historial
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente virtual experto de una clínica veterinaria. Eres amable, profesional y conciso."),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}")
])

chain = prompt_template | llm

# Empaquetamos la cadena con la gestión de historial automática
conversational_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/health")
async def health_check():
    try:
        key_preview = api_key[:5] + "..." if api_key else "¡ERROR! LA LLAVE ESTÁ VACÍA"
        modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return {"status": "ok", "llave_detectada": key_preview, "modelos_disponibles": modelos}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}

@app.post("/chat/test")
async def chat_test(chat_msg: ChatMessage):
    try:
        # 5. Ejecutar la IA pasándole el ID de la sesión
        respuesta_ia = conversational_chain.invoke(
            {"input": chat_msg.message},
            config={"configurable": {"session_id": chat_msg.session_id}}
        )
        return {
            "response": respuesta_ia.content,
            "status": "success"
        }
    except Exception as e:
        return {
            "response": f"Error del sistema: {str(e)}",
            "status": "error"
        }