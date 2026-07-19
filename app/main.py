from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import FileResponse

from app.services.prompt_security_service import PromptSecurityService

from app.schemas.chat import ChatRequest
from app.services.groq_service import GroqService
from app.services.database_service import DatabaseService

from fastapi.responses import JSONResponse


app = FastAPI(
    title="AI Gaming Assistant API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



db_service = DatabaseService()
security_service = PromptSecurityService()
ai_service = GroqService(db_service)

@app.post("/api/chat/history")
def chat_history(payload: ChatRequest):

    db_user = db_service.get_or_create_user(
        payload.user.model_dump()
    )

    sessions = db_service.get_user_chat_sessions(
        db_user["id"]
    )

    return JSONResponse({
        "chats": sessions
    })

@app.get("/api/chat/{session_id}")
def get_chat_messages(session_id: str):

    messages = db_service.get_messages(
        session_id
    )

    return JSONResponse({
        "messages": messages
    })

# ==========================================
# Rename Chat
# ==========================================

@app.put("/api/chat/{session_id}/rename")
def rename_chat(
    session_id: str,
    payload: dict,
):

    title = payload.get("title", "").strip()

    if not title:
        return JSONResponse(
            {
                "error": "Title cannot be empty."
            },
            status_code=400
        )

    chat = db_service.get_chat_session(session_id)

    if not chat:
        return JSONResponse(
            {
                "error": "Chat not found."
            },
            status_code=404
        )

    updated = db_service.rename_chat_session(
        session_id=session_id,
        title=title,
    )

    return JSONResponse(
        {
            "success": True,
            "chat": updated,
        }
    )


# ==========================================
# Delete Chat
# ==========================================

@app.delete("/api/chat/{session_id}")
def delete_chat(session_id: str):

    chat = db_service.get_chat_session(session_id)

    if not chat:
        return JSONResponse(
            {
                "error": "Chat not found."
            },
            status_code=404
        )

    db_service.delete_chat_session(session_id)

    return JSONResponse(
        {
            "success": True
        }
    )

@app.get("/api/test-db")
def test_db():
    return db_service.test_connection()

@app.post("/api/chat/new")
def create_chat(payload: ChatRequest):

    # Get or create the user
    db_user = db_service.get_or_create_user(
        payload.user.model_dump()
    )

    # Create new chat session
    session = db_service.create_chat_session(
        db_user["id"]
    )

    return JSONResponse({
        "session_id": session["id"]
    })

@app.post("/api/chat")
async def chat_endpoint(payload: ChatRequest):

    # Create user if needed
    db_user = db_service.get_or_create_user(payload.user.model_dump())

# security check for prompt injection

    security = security_service.validate(payload.message)

    if not security.allowed:

     return JSONResponse(
        {
            "error": security.message
        },
        status_code=400
    )

    payload.message = security.cleaned_prompt



    # -------------------------
    # Create chat session
    # -------------------------

    session_id = payload.session_id

    if session_id is None:

        session = db_service.create_chat_session(
            user_id=db_user["id"],
            title=payload.message[:50]
        )

        session_id = session["id"]


    # -------------------------
    # Save user message
    # -------------------------

    db_service.save_message(
        session_id=session_id,
        role="user",
        content=payload.message
    )


    return StreamingResponse(
        ai_service.get_chat_stream(
            payload.message,
            session_id=session_id
        ),
        media_type="text/plain",
        headers={
            "X-Session-Id": str(session_id)
        }
    )

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def home():
    return FileResponse("static/index.html")