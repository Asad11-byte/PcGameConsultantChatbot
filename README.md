
# 🎮 PC Game Consultant Chatbot

An AI-powered **PC Game Consultant Chatbot** that helps gamers build custom gaming rigs, troubleshoot complex hardware issues, diagnose real-time performance bottlenecks, optimize frame rates, and receive intelligent component pairings.

The application is built using a modern decoupled stack: **FastAPI** on the backend, **Groq (Llama 3.3 70B)** executing advanced tool-calling utilities, **Supabase** for secure storage workflows, **Auth0** protecting user states, and a fluid, responsive frontend built with **Vanilla HTML, CSS, and JavaScript**.

---

# 🚀 Features

- 🤖 **AI-Powered Hardware Consultant:** Native intelligence specializing in modern computer components, thermal diagnostics, and compatibility metrics.
- 🛠️ **Deterministic Tool Calling (Function Calling):** The LLM dynamically invokes internal analytical modules based on natural language intent:
  - `pc_builder`: Evaluates hardware compatibility, structural performance bottlenecks, and balance margins relative to pricing limits.
  - `fps_estimator`: Forecasts runtime rendering performance based on targeted CPU, GPU, resolution scaling, and graphical quality choices.
- 💬 **Real-Time Response Streams:** Sub-second token delivery powered by the Groq SDK inference engine.
- 🔐 **Secure Authentication Layer:** User account onboarding and runtime access tokens handled via Auth0 hooks.
- 💾 **Persistent Session Histories:** Automatically initializes multiple isolated chat profiles bound to unique relational rows inside Supabase.
- 📱 **Fluid Responsive Viewports:** Custom media query boundaries optimized from desktop dimensions down to ultra-small mobile displays, eliminating layout shifting or scaling bugs.

---

# 🛠️ Tech Stack

### Backend
- **FastAPI:** Asynchronous routing framework.
- **Groq SDK:** Execution layer for Llama 3.3 70B Versatile.
- **Supabase Python SDK:** Relational record sync layer.
- **Python-Jose:** Secure cryptographic authentication validation.

### Frontend
- **HTML5 & Modern CSS3:** Custom variable architecture utilizing smooth panel transitions.
- **Vanilla JavaScript:** Asynchronous DOM stream updating and unified fetch routing layers.

### Database & Hosting
- **Supabase PostgreSQL:** Dynamic schema housing data entities across users, sessions, and records.
- **Vercel Cloud Infrastructure:** Global serverless runtime execution environments.

---

# 🏗️ Project Architecture

```text
                        ┌─────────────────────┐
                        │     Web Browser     │
                        │ HTML • CSS • JS     │
                        └──────────┬──────────┘
                                   │
                                   │ HTTP / Serverless Route
                                   │
                        ┌──────────▼──────────┐
                        │       FastAPI       │
                        │    REST Endpoints   │
                        └──────────┬──────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
         │                         │                         │
┌────────▼────────┐       ┌────────▼────────┐       ┌────────▼────────┐
│ Authentication  │       │  Groq Service   │       │ Database Service│
│     Auth0       │       │ (Tool Calling)  │       │    Supabase     │
└─────────────────┘       └────────┬────────┘       └────────┬────────┘
                                   │                         │
                     ┌─────────────┴─────────────┐           │
                     │    Local Python Tools     │           │
                     │ • pc_builder              │           │
                     │ • fps_estimator           │           │
                     └───────────────────────────┘           │
                                                             │
                                             ┌───────────────▼──────────────┐
                                             │          PostgreSQL          │
                                             │                              │
                                             │ • Users                      │
                                             │ • Chat Sessions              │
                                             │ • Messages                   │
                                             └──────────────────────────────┘

```

---

# 📂 Project Structure

```text
PC-Game-Consultant/
│
├── app/
│   ├── schemas/
│   │   └── chat.py
│   ├── services/
│   │   ├── database_service.py
│   │   └── groq_service.py
│   ├── main.py
│   └── tools.py         # Specialized Tool Modules (pc_builder, fps_estimator)
│
├── static/
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   ├── sidebar.css
│   ├── landingpage.css
│   └── responsive.css
│
├── requirements.txt
├── vercel.json          # Production Serverless Distribution Matrix
├── .env
└── README.md

```

---

# ⚙️ Installation & Local Development

## 1. Clone Repository

```bash
git clone [https://github.com/Asad11-byte/PcGameConsultantChatbot.git](https://github.com/Asad11-byte/PcGameConsultantChatbot.git)
cd PcGameConsultantChatbot

```

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

## 3. Install Core Requirements

```bash
pip install -r requirements.txt

```

> **Note on Requirements Syntax:** Ensure your `requirements.txt` features explicit strings without structural spacing:
> `python-jose[cryptography]==3.3`

## 4. Configure Environment Variables

Create a `.env` file in the root execution path:

```env
GROQ_API_KEY=your_groq_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

```

Configure your target Auth0 client domain configurations within your local `static/app.js` file.

## 5. Launch Local Dev Node

```bash
uvicorn app.main:app --reload

```

Navigate to your local browser layout at: `http://127.0.0.1:8000`

---

# ☁️ Cloud Deployment on Vercel

The production runtime maps its directory execution pathways via the explicit configuration rules defined inside your `vercel.json` file:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app/main.py",
      "use": "@vercel/python"
    },
    {
      "src": "static/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/api/(.*)",
      "dest": "app/main.py"
    },
    {
      "src": "/(.*)",
      "dest": "app/main.py"
    }
  ]
}

```

### Push Deployment Steps

1. Ensure cloud keys matching your `.env` structure are configured directly within the **Project Settings -> Environment Variables** section of your Vercel Dashboard.
2. Trigger the platform pipeline updates safely using clean Git structures:

```bash
git add .
git commit -m "feat: optimize responsive layout matrices and configure serverless rules"
git push origin main

```

---

# 🔑 Authentication Flow

```text
User ──► Auth0 Client Login ──► JWT Issued ──► FastAPI Router Bearer Verification ──► Supabase Table Sync

```

---

# 📡 Primary API Endpoints

### Database Integration Test

```http
GET /api/test-db

```

### Session Creation Anchor

```http
POST /api/chat/new

```

### Direct Agent Query Stream

```http
POST /api/chat

```

*Evaluates structural conversational logs, determines tool selection matches, pushes new records to Supabase, and opens a text chunk delivery pipeline back to the frontend.*

---

# 💡 Interactive Prompts to Try

* "Build me a high-performance gaming PC focused on architectural streaming under $1500."
* "Calculate the rough frame metrics for a system combining an RTX 4070 with a Ryzen 5 5600 at 1440p running Cyberpunk 2077."
* "Why is my layout freezing up when rendering resource loops in modern shooters? Let's check for component bottlenecks."

---

# 👨‍💻 Author

**Asad Ali**

* **GitHub:** [Asad11-byte](https://github.com/Asad11-byte)
* **LinkedIn:** [Your LinkedIn Profile](https://linkedin.com/in/your-linkedin)

---

# ⭐ Support

If this custom tool routing architecture or layout guide helped optimize your development flow, drop a ⭐ on the repository!

---

# 📄 License

This project is open-source and licensed under the terms of the MIT License.

```

```
