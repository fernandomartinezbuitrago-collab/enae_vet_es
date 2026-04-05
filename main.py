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

# 1. Cargar variables de entorno
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

app = FastAPI(title="Chatbot Clínica Veterinaria - RAG")
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

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=api_key
)

# ==========================================
# 🔥 INICIO DE RAG (Ingesta de Fuente Oficial)
# ==========================================
# URL oficial sobre la que el bot va a aprender (puedes cambiarla por la de tu clínica si tienes)
URL_OFICIAL = "https://es.wikipedia.org/wiki/Castraci%C3%B3n" 

try:
    # 1. Ingiere y consulta la URL
    loader = WebBaseLoader(URL_OFICIAL)
    docs = loader.load()
    texto_fuente = docs[0].page_content[:15000] # Cogemos los primeros 15.000 caracteres
    
    # 2. Obligamos al bot a citar la fuente y basarse en ella
    mensaje_sistema = f"""Eres un asistente virtual experto de una clínica veterinaria. Eres amable y profesional.
    IMPORTANTE: Debes basar tus respuestas EXCLUSIVAMENTE en la siguiente INFORMACIÓN OFICIAL de la clínica.
    Si el usuario pregunta algo que no está en esta información oficial, responde: "Lo siento, según la información oficial de la clínica no tengo ese dato. Por favor, contacta directamente con nuestro mostrador."
    
    INFORMACIÓN OFICIAL OBTENIDA DE LA URL:
    {texto_fuente}
    """
except Exception as e:
    # 3. Manejo de errores cuando la fuente no está disponible
    print(f"Error cargando la fuente: {e}")
    mensaje_sistema = "Eres un asistente de clínica veterinaria. (AVISO INTERNO: La fuente de datos oficial está caída, responde bajo tu propio conocimiento pero avisa de esto al cliente)."
# ==========================================
# 🔥 FIN DE RAG
# ==========================================

prompt_template = ChatPromptTemplate.from_messages([
    ("system", mensaje_sistema),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}")
])

chain = prompt_template | llm

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
    return {"status": "ok", "estado_rag": "Fuente cargada correctamente" if "INFORMACIÓN OFICIAL" in mensaje_sistema else "Error al cargar fuente"}

@app.post("/chat/test")
async def chat_test(chat_msg: ChatMessage):
    try:
        respuesta_ia = conversational_chain.invoke(
            {"input": chat_msg.message},
            config={"configurable": {"session_id": chat_msg.session_id}}
        )
        return {"response": respuesta_ia.content, "status": "success"}
    except Exception as e:
        return {"response": f"Error del sistema: {str(e)}", "status": "error"}