from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Chatbot Clínica Veterinaria - MVP")

class ChatMessage(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"status": "online", "message": "Servidor de la Clínica Veterinaria funcionando"}

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