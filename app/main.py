from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.schemas.chat import ChatRequest
from app.services.groq_service import GroqService
from app.services.database_service import DatabaseService


app = FastAPI(title="Clean Architecture Groq AI Pipeline")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai_service = GroqService()
db_service = DatabaseService()



@app.get("/api/test-db")
def test_db():
    return db_service.test_connection()


@app.post("/api/chat")
async def chat_endpoint(payload: ChatRequest):

    # Create user in Supabase (or return existing user)
    db_user = db_service.get_or_create_user(payload.user.model_dump())

    print("\n========== DATABASE USER ==========")
    print(db_user)
    print("===================================\n")

    return StreamingResponse(
        ai_service.get_chat_stream(payload.message),
        media_type="text/plain"
    )

app.mount("/", StaticFiles(directory="static", html=True), name="static")