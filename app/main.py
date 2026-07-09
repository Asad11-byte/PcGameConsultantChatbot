from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.schemas.chat import ChatRequest
from app.services.groq_service import GroqService  # Updated Import

app = FastAPI(title="Clean Architecture Groq AI Pipeline")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq Service
ai_service = GroqService()

@app.post("/api/chat")
async def chat_endpoint(payload: ChatRequest):
    """
    Validates payload using Pydantic, passes the message to the Groq service,
    and returns a live token stream directly to the JavaScript frontend.
    """
    user_prompt = payload.message
    
    return StreamingResponse(
        ai_service.get_chat_stream(user_prompt), 
        media_type="text/plain"
    )

app.mount("/", StaticFiles(directory="static", html=True), name="static")