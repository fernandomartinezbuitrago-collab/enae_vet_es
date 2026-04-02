import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

# Importar las librerías de Google y LangChain
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# 1. Cargar variables de entorno
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# 2. Configurar la librería base de Google (para el diagnóstico)
if api_key:
    genai.configure(api_key=api_key)

app = FastAPI(title="Chatbot Clínica Veterinaria - MVP")
templates = Jinja2Templates(directory="templates")

class ChatMessage(BaseModel):
    message: str

# 3. Configurar el Cerebro
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    google_api_key=api_key
)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente virtual experto de una clínica veterinaria. Eres amable, profesional y conciso."),
    ("user", "{input}")
])
chain = prompt_template | llm

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# 🔥 EL NUEVO DIAGNÓSTICO ESTÁ AQUÍ 🔥
@app.get("/health")
async def health_check():
    try:
        # Extraemos los primeros 5 caracteres de la llave para asegurar que Vercel la está leyendo
        key_preview = api_key[:5] + "..." if api_key else "¡ERROR! LA LLAVE ESTÁ VACÍA"
        
        # Le pedimos a Google la lista de modelos disponibles para ESTA llave
        modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        return {
            "status": "ok",
            "llave_detectada": key_preview,
            "modelos_disponibles": modelos
        }
    except Exception as e:
        return {"status": "error", "detalle": str(e)}

@app.post("/chat/test")
async def chat_test(chat_msg: ChatMessage):
    try:
        respuesta_ia = chain.invoke({"input": chat_msg.message})
        return {
            "response": respuesta_ia.content,
            "status": "success"
        }
    except Exception as e:
        return {
            "response": f"Error del sistema: {str(e)}",
            "status": "error"
        }