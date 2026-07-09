# PC Game Consultant Chatbot 🎮🚀

An AI-powered, high-performance chatbot application built with a **Clean Architecture** pattern. This specialized assistant functions as an expert hardware technician and gaming optimization specialist, helping users diagnose performance bottlenecks, recommend custom system build specifications, and troubleshoot hardware issues in real-time.

Powered by **FastAPI** on the backend and leveraging **Groq API Cloud** for blazing-fast asynchronous token streaming.

---

## 🏗️ Architecture & Data Flow

This project strictly follows a **Clean Architecture** pattern to isolate components, maintain high scannability, and allow for easy future modifications (such as swapping model providers or rebuilding the frontend).

*   **Presentation Layer (Frontend):** Pure HTML, CSS, and client-side JavaScript. Captures user prompts along with configuration parameters (testing knobs) and handles the incoming stream.
*   **API / Routing Layer (`app/main.py`):** The gatekeeper of the application. Utilizes **Pydantic** schemas to validate incoming payload constraints before passing them to the business logic.
*   **Service Layer (`app/services/`):** The brain of the backend. It wraps the core business logic, injects the specialized PC Consultant system prompt, and interfaces directly with Groq's asynchronous infrastructure.

```text
[Frontend Interface] ──(JSON Payload)──► [FastAPI Endpoint] ──(Pydantic Validation)──► [Groq Service Layer] ──► [Groq API Cloud]
                                                                                                                   │
[User Terminal View] ◄──(Chunk Rendering)── [JS Stream Reader] ◄──(StreamingResponse)◄─────────────────────────────┘