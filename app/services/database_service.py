import os
from urllib import response
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


class DatabaseService:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

        if not self.url or not self.key:
            raise ValueError("Supabase credentials are missing.")

        self.client: Client = create_client(self.url, self.key)

    def test_connection(self):
        try:
            print("URL:", self.url)
            print("Key exists:", self.key is not None)

            response = (
                self.client
                .table("users")
                .select("*")
                .limit(1)
                .execute()
            )

            return {
                "success": True,
                "data": response.data
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "type": type(e).__name__
            }

    def get_or_create_user(self, auth0_user):

     print("\n===== get_or_create_user() CALLED =====")
     print(auth0_user)

     auth0_id = auth0_user["sub"]

     existing = (
        self.client
        .table("users")
        .select("*")
        .eq("auth0_id", auth0_id)
        .execute()
    )

     print("Existing:", existing.data)

     if existing.data:
        print("User already exists")
        return existing.data[0]

     new_user = {
        "auth0_id": auth0_id,
        "email": auth0_user.get("email"),
        "name": auth0_user.get("name"),
        "picture": auth0_user.get("picture")
    }

     print("Inserting:", new_user)

     created = (
        self.client
        .table("users")
        .insert(new_user)
        .execute()
    )

     print("Created:", created.data)

     return created.data[0]
    
    def create_chat_session(self, user_id: int, title: str = "New Chat"):
     response = (
        self.client
        .table("chat_sessions")
        .insert({
            "user_id": user_id,
            "title": title
        })
        .execute()
    )

     return response.data[0]

    def get_user_chat_sessions(self, user_id: int):

     response = (
        self.client
        .table("chat_sessions")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )

     return response.data
    
    def save_message(self, session_id: int, role: str, content: str):
     response = (
        self.client
        .table("messages")
        .insert({
            "session_id": session_id,
            "role": role,
            "content": content
        })
        .execute()
    )

     return response.data[0]
    def get_chat_session(self, session_id: str):
     response = (
        self.client
        .table("chat_sessions")
        .select("*")
        .eq("id", session_id)
        .single()
        .execute()
    )
     return response.data
    def get_messages(self, session_id: str):
     response = (
        self.client
        .table("messages")
        .select("role, content")
        .eq("session_id", session_id)
        .order("created_at")
        .execute()
    )

     return response.data