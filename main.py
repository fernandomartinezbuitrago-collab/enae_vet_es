from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="Chatbot Clínica Veterinaria - MVP")
templates = Jinja2Templates(directory="templates") # <--- NUEVA LÍNEA

class ChatMessage(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse) # <--- CAMBIADO
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "veterinary-backend"}

@app.post("/chat/test")
async def chat_test(chat_msg: ChatMessage):
    # Por ahora es un mock (simulación) para el ticket VET-7
    return {
        "response": f"He recibido tu mensaje: '{chat_msg.message}'. El chatbot estará listo pronto.",
        "status": "mock_mode"
    }