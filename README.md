# 🎮 PC Game Consultant Chatbot

An AI-powered chatbot designed to assist gamers in diagnosing PC hardware issues, recommending gaming components, optimizing system performance, and answering PC gaming-related questions in real time.

Built with **FastAPI**, **Groq Cloud API**, **Vanilla HTML/CSS/JavaScript**, and **Auth0 Authentication**, the application follows the **Clean Architecture** design pattern to ensure scalability, maintainability, and separation of concerns.

---

# 📸 Features

- 🤖 AI-powered PC gaming consultant
- ⚡ Real-time streaming responses using Groq API
- 🔐 User authentication with Auth0
- 🎛 Adjustable AI inference parameters
  - System Prompt
  - Temperature
  - Top-P
  - Maximum Tokens
- 🧠 Clean Architecture backend
- 📡 FastAPI REST API
- 🎨 Modern responsive dashboard
- 🔄 Streaming token rendering without page refresh
- 🛡 Request validation using Pydantic

---

# 🏗 Project Architecture

The project follows the **Clean Architecture** approach, separating the application into independent layers.

```
                  Frontend (HTML/CSS/JavaScript)
                               │
                               │ JSON Request
                               ▼
                     FastAPI Routing Layer
                               │
                     Pydantic Validation
                               │
                               ▼
                     Business Service Layer
                               │
                        Groq API Client
                               │
                               ▼
                        Groq Cloud Models
                               │
                    Streaming AI Response
                               │
                               ▼
                         Browser Interface
```

---

# 📂 Project Structure

```
PC-Game-Consultant-Chatbot
│
├── app
│   ├── main.py
│   ├── schemas
│   │     └── chat.py
│   ├── services
│   │     └── groq_service.py
│   └── __init__.py
│
├── static
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── .env
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🛠 Technologies Used

### Backend

- FastAPI
- Uvicorn
- Groq Python SDK
- Pydantic
- Python Dotenv

### Frontend

- HTML5
- CSS3
- Vanilla JavaScript

### Authentication

- Auth0 SPA SDK

### AI

- Groq Cloud API
- Llama 3.1 8B Instant

---

# ⚙ Installation

## 1 Clone Repository

```bash
git clone https://github.com/yourusername/PC-Game-Consultant-Chatbot.git

cd PC-Game-Consultant-Chatbot
```

---

## 2 Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4 Create Environment File

Create a `.env` file.

```env
GROQ_API_KEY=your_groq_api_key
```

---

## 5 Run Application

```bash
python -m uvicorn app.main:app --reload
```

Open

```
http://127.0.0.1:8000
```

---

# 🔐 Auth0 Configuration

Create an application in Auth0.

Choose

```
Single Page Application (SPA)
```

Configure

```
Allowed Callback URLs
http://127.0.0.1:8000

Allowed Logout URLs
http://127.0.0.1:8000

Allowed Web Origins
http://127.0.0.1:8000

Allowed Origins (CORS)
http://127.0.0.1:8000
```

Update the following values inside `static/app.js`

```javascript
domain: "YOUR_AUTH0_DOMAIN",

clientId: "YOUR_CLIENT_ID"
```

---

# 🎛 AI Model Controls

The application allows users to customize model inference through the control panel.

| Parameter | Description |
|-----------|-------------|
| System Prompt | Defines assistant behavior |
| Temperature | Controls randomness |
| Top-P | Controls token sampling probability |
| Max Tokens | Maximum generated response length |

---

# 💬 Example Questions

- Recommend a gaming PC under $1000.
- Is my RTX 3060 suitable for 1440p gaming?
- My CPU reaches 95°C while gaming. What should I do?
- Should I upgrade my RAM or GPU first?
- Why am I experiencing FPS drops?
- Recommend components for a streaming PC.

---

# 🔄 API Endpoint

### POST

```
/chat
```

Example Request

```json
{
    "message":"Build me a gaming PC",
    "system_prompt":"You are an expert PC consultant.",
    "temperature":0.7,
    "top_p":1,
    "max_tokens":300
}
```

---

# 📈 Future Improvements

- Conversation history
- Persistent user profiles
- GPU benchmark database integration
- PCPartPicker integration
- Retrieval-Augmented Generation (RAG)
- Admin analytics dashboard
- Dark/Light mode
- Docker deployment
- Unit and integration tests

---

# 👨‍💻 Author

**Asad Ali**

AI & Backend Developer

---

# 📄 License

This project is licensed under the MIT License.