import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

# Importaciones de LangChain para Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Cargar variables de entorno (tu GOOGLE_API_KEY)
load_dotenv()

app = FastAPI(title="Chatbot Clínica Veterinaria - MVP")
templates = Jinja2Templates(directory="templates")

class ChatMessage(BaseModel):
    message: str

# Configurar el "Cerebro" de Gemini
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Configurar la personalidad del Bot (El System Prompt)
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente virtual experto de una clínica veterinaria. Eres amable, profesional y conciso. Ayudas a los dueños de mascotas con dudas sobre preparativos médicos y esterilizaciones."),
    ("user", "{input}")
])

# Unir el prompt con el modelo
chain = prompt_template | llm

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "veterinary-backend"}

@app.post("/chat/test")
async def chat_test(chat_msg: ChatMessage):
    try:
        # Aquí ocurre la magia: Le pasamos el mensaje del usuario a LangChain/Gemini
        respuesta_ia = chain.invoke({"input": chat_msg.message})
        
        return {
            "response": respuesta_ia.content,
            "status": "success"
        }
    except Exception as e:
        # Si la API Key falla o hay un error, lo veremos aquí
        return {
            "response": f"Lo siento, mis circuitos veterinarios fallaron: {str(e)}",
            "status": "error"
        }