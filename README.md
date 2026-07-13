# 🎮 PC Game Consultant Chatbot

An AI-powered **PC Game Consultant Chatbot** that helps gamers build gaming PCs, troubleshoot hardware issues, diagnose performance bottlenecks, optimize FPS, and receive intelligent hardware recommendations.

The application is built using **FastAPI**, **Groq Llama 3.3 70B**, **Supabase**, **Auth0**, and a responsive frontend developed with **Vanilla HTML, CSS, and JavaScript**.

---

# 🚀 Features

- 🤖 AI-powered gaming hardware assistant
- 💬 Real-time streaming AI responses
- 🔐 Secure authentication with Auth0
- 👤 Automatic user creation
- 💾 Persistent chat history using Supabase
- 📝 Multiple chat sessions
- 🖥️ Gaming PC build recommendations
- 🎮 FPS optimization guidance
- 🔧 Hardware troubleshooting
- 🌡️ Thermal and performance diagnostics
- 📱 Responsive UI for desktop and mobile

---

# 🛠️ Tech Stack

## Backend

- FastAPI
- Python
- Groq API
- Llama 3.3 70B Versatile
- Supabase
- Auth0
- Uvicorn

## Frontend

- HTML5
- CSS3
- Vanilla JavaScript

## Database

Supabase PostgreSQL

---

# 🏗️ Project Architecture

```
                           ┌─────────────────────┐
                           │     Web Browser     │
                           │ HTML • CSS • JS     │
                           └──────────┬──────────┘
                                      │
                                      │ HTTP
                                      │
                           ┌──────────▼──────────┐
                           │      FastAPI        │
                           │    REST Endpoints   │
                           └──────────┬──────────┘
                                      │
             ┌────────────────────────┼────────────────────────┐
             │                        │                        │
             │                        │                        │
     ┌───────▼────────┐      ┌────────▼────────┐      ┌────────▼────────┐
     │ Authentication │      │  Groq Service   │      │ Database Service│
     │     Auth0      │      │ Llama 3.3 70B   │      │    Supabase     │
     └────────────────┘      └─────────────────┘      └─────────────────┘
                                                               │
                                                               │
                                               ┌───────────────▼──────────────┐
                                               │         PostgreSQL           │
                                               │                              │
                                               │ • Users                      │
                                               │ • Chat Sessions              │
                                               │ • Messages                   │
                                               └──────────────────────────────┘
```

---

# 📂 Project Structure

```
PC-Game-Consultant/
│
├── app/
│   │
│   ├── schemas/
│   │   └── chat.py
│   │
│   ├── services/
│   │   ├── database_service.py
│   │   └── groq_service.py
│   │
│   └── main.py
│
├── static/
│   │
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   ├── sidebar.css
│   ├── landingpage.css
│   └── responsive.css
│
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/pc-game-consultant.git

cd pc-game-consultant
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=your_groq_api_key

SUPABASE_URL=your_supabase_url

SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
```

Configure Auth0 credentials in **app.js**.

---

## 5. Run the Project

```bash
uvicorn app.main:app --reload
```

Visit

```
http://127.0.0.1:8000
```

---

# 🔑 Authentication Flow

```
User
   │
   ▼
Auth0 Login
   │
   ▼
Authenticated User
   │
   ▼
FastAPI
   │
   ▼
Create/Get User
   │
   ▼
Supabase
```

---

# 💬 Chat Flow

```
User Message
      │
      ▼
FastAPI Endpoint
      │
      ▼
Get/Create User
      │
      ▼
Create Chat Session
      │
      ▼
Save User Message
      │
      ▼
Groq LLM
      │
      ▼
Stream Response
      │
      ▼
Save Assistant Response
      │
      ▼
Return Response to Browser
```

---

# 🗄️ Database Schema

## users

| Column |
|---------|
| id |
| auth0_id |
| name |
| email |
| picture |

---

## chat_sessions

| Column |
|---------|
| id |
| user_id |
| title |
| created_at |

---

## messages

| Column |
|---------|
| id |
| session_id |
| role |
| content |
| created_at |

---

# 📡 API Endpoints

## Test Database

```
GET /api/test-db
```

---

## Create Chat

```
POST /api/chat/new
```

---

## Send Message

```
POST /api/chat
```

Streams AI responses while storing messages in Supabase.

---

# 💡 Example Prompts

- Build me a gaming PC under $1000.
- Recommend the best GPU for 1440p gaming.
- Why is my FPS dropping in Valorant?
- Is my Ryzen 5 5600 bottlenecking an RTX 4070?
- My PC shuts down while gaming.
- Suggest the best gaming monitor under $300.
- Compare RTX 5070 vs RX 9070 XT.

---

# ✨ Future Improvements

- Chat history sidebar
- Rename chats
- Delete chats
- Search previous conversations
- Markdown rendering
- Syntax highlighting
- Image upload
- Hardware compatibility checker
- Gaming benchmark database
- User profile page
- Dark/Light mode
- Export conversations

---

# 📸 Screenshots

Add screenshots of:

- Landing Page
- Login Screen
- Chat Interface
- Sidebar
- Mobile View

---

# 📦 Requirements

```
fastapi
uvicorn[standard]
groq
supabase
python-dotenv
python-multipart
pydantic
httpx
```

---

# 👨‍💻 Author

**Asad Ali**

GitHub: https://github.com/your-github

LinkedIn: https://linkedin.com/in/your-linkedin

---

# ⭐ If you found this project useful

Give the repository a ⭐ on GitHub!

---

# 📄 License

This project is licensed under the MIT License.