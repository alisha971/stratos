# 🚀 **STRATOS — End-to-End AI Research & Analysis System**

Stratos is a full-stack, multi-agent research automation platform consisting of:

### **🧠 Backend (FastAPI)**

* Multi-agent pipeline (Planner → Researcher → Analyst → Critic → Strategist)
* MCP Tool Governor (Tavily, GNews, ArXiv, WebReader, PDF-RAG)
* Structured reporting, JSON output
* Critique–repair loop
* Deep-Dive RAG endpoint
* Fully typed FastAPI server

### **🌐 Frontend (Next.js)**

* Clean UI to submit topics
* View structured report
* Deep-dive follow-up querying
* Connects directly to FastAPI backend

### **🔒 Private GitHub Repo Integration**

Allows you to resume development from **any computer** with minimal setup.

---

# 📁 **Project Structure**

```
stratos/
│
├── backend/
│   ├── agents/               # Planner, Researcher, Analyst, Critic, Strategist
│   ├── orchestrator/         # Graph, state, agent routing
│   ├── mcp/                  # Governor + tool adapters
│   │   ├── adapters/
│   │   └── config.yml
│   ├── backend/              # FastAPI routes + schema
│   ├── tests/
│   ├── requirements.txt
│   ├── .env                  # Backend secrets (ignored)
│   └── api.py
│
├── ui-stratos/               # Next.js frontend
│   ├── app/
│   ├── components/
│   ├── public/
│   ├── package.json
│   ├── next.config.js
│   └── .env.local            # Frontend env (ignored)
│
├── .gitignore
└── README.md
```

---

# 🔑 Environment Variables

## **Backend: `/backend/.env`**

```
GOOGLE_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key  # optional but recommended
TAVILY_API_KEY=your_tavily_key
```

---

## **Frontend: `/ui-stratos/.env.local`**

```
NEXT_PUBLIC_BACKEND_URL=http://127.0.0.1:8000
```

---

# 🛠 Installation — On ANY Computer

## 1️⃣ Clone your private repo

```
git clone https://github.com/YOUR_USERNAME/stratos.git
cd stratos
```

---

# 2️⃣ Backend Setup

```
cd backend
python -m venv venv
```

Activate venv:

**Windows**

```
venv\Scripts\activate
```

**Mac/Linux**

```
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Create `.env` (copy/paste):

```
GOOGLE_API_KEY=xxxxx
TAVILY_API_KEY=xxxxx
```

Run backend:

```
uvicorn backend.api:app --reload --port 8000
```

Open docs:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

# 3️⃣ Frontend Setup

Open another terminal:

```
cd ui-stratos
npm install
```

Create `.env.local`:

```
NEXT_PUBLIC_BACKEND_URL=http://127.0.0.1:8000
```

Run frontend:

```
npm run dev
```

Open UI:
[http://localhost:3000](http://localhost:3000)

---

# ▶️ Running the Entire System

Backend:

```
uvicorn backend.api:app --reload
```

Frontend:

```
npm run dev
```

---

# 🧪 Testing Endpoints

From `/backend`:

```
python tests/test_analyze_topic.py
python tests/test_pdf_rag.py
pytest
```

---

# 🔄 GitHub Workflow

### Save your work:

```
git add .
git commit -m "update"
git push
```

### Resume on another PC:

```
git pull
```

If conflicts:

```
git pull --rebase
```

---

# 🧰 Dev Command Cheat-Sheet

### Backend

```
cd backend
venv\Scripts\activate
uvicorn backend.api:app --reload
```

### Frontend

```
cd ui-stratos
npm run dev
```

### Git

```
git add .
git commit -m "message"
git push
```

### Install deps

```
pip install -r requirements.txt
npm install
```

---

# ⚠️ Common Issues & Fixes

### **1. Gemini "429 RESOURCE_EXHAUSTED"**

You exceeded free-tier requests.

Fix:

* Wait 60 seconds
* OR switch to OpenAI models
* OR upgrade credit tier

---

### **2. .env not loading**

Make sure:

* Backend `.env` is inside `/backend`
* Frontend `.env.local` is inside `/ui-stratos`
* Restart servers

---

### **3. Node version too old**

Next.js requires Node ≥ 18.

Check:

```
node -v
```

---

# 🚀 **STRATOS — End-to-End AI Research & Analysis System**

Stratos is a private full-stack project combining:

* **FastAPI Backend** (multi-agent LLM workflow)
* **Next.js Frontend** (UI for topic analysis & PDF deep dive)
* **MCP Tool Governor** (Tavily, GNews, ArXiv, WebReader, PDF-RAG)
* **GitHub Workflow** to resume development from ANY PC

---

# 📁 Project Structure

```
stratos/
│
├── backend/
│   ├── agents/
│   ├── orchestrator/
│   ├── mcp/
│   ├── backend/
│   ├── tests/
│   ├── requirements.txt
│   └── .env
│
├── ui-stratos/        # Next.js frontend
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── node_modules/   (generated automatically)
│   ├── package.json
│   ├── package-lock.json
│   ├── next.config.mjs
│   ├── tsconfig.json
│   ├── postcss.config.mjs
│   ├── tailwind.config.ts
│   ├── .env.local
│   └── .gitignore
│
└── README.md
```

---

# 🔒 .gitignore — What is NOT Synced?

Your frontend `.gitignore` contains:

```
node_modules/
.next/
.env.local
```

This is PERFECT.
It means:

* **Huge folders** like `node_modules` & `.next` are NOT uploaded.
* Secrets like **NEXT_PUBLIC_BACKEND_URL** are NOT uploaded.

When you move to another PC, these folders will regenerate automatically after install.

---

# 🧑‍💻 Setup Instructions — From ANY New Computer

Below is the **complete setup** for BOTH frontend and backend.

---

# 1️⃣ Clone the Private Repository

```
git clone https://github.com/YOUR_USERNAME/stratos.git
cd stratos
```

---

# 2️⃣ Backend Setup (FastAPI)

Navigate:

```
cd backend
```

### Create virtual environment:

**Windows**

```
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux**

```
python3 -m venv venv
source venv/bin/activate
```

### Install Python requirements:

```
pip install -r requirements.txt
```

### Create `/backend/.env`

```
GOOGLE_API_KEY=your_key
TAVILY_API_KEY=your_key
OPENAI_API_KEY=optional
```

### Run backend:

```
uvicorn backend.api:app --reload --port 8000
```

Open API docs:
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

# 3️⃣ Frontend Setup (Next.js UI)

Navigate:

```
cd ui-stratos
```

### Install Node.js (only once per PC)

You must have:

```
node >= 18
npm >= 8
```

Check versions:

```
node -v
npm -v
```

---

### Install frontend dependencies:

```
npm install
```

This creates:

* `node_modules/`
* `.next/`

These folders are ignored in GitHub — that's correct.

---

### Create `/ui-stratos/.env.local`

Paste:

```
NEXT_PUBLIC_BACKEND_URL=http://127.0.0.1:8000
```

---

### Run frontend:

```
npm run dev
```

Open UI:
👉 [http://localhost:3000](http://localhost:3000)

---

# 4️⃣ GitHub Workflow — Continue Anywhere

### Save progress

```
git add .
git commit -m "update"
git push
```

### Resume on another PC

```
git pull
```

---

# 5️⃣ Commands Cheat Sheet

### Backend

```
cd backend
venv\Scripts\activate
uvicorn backend.api:app --reload
```

### Frontend

```
cd ui-stratos
npm install
npm run dev
```

### Git

```
git add .
git commit -m "..."
git push
```

---

# 6️⃣ Troubleshooting

### ❌ Missing packages?

```
npm install
pip install -r requirements.txt
```

### ❌ .env not loading?

Make sure:

* Backend env file → `/backend/.env`
* Frontend env file → `/ui-stratos/.env.local`

### ❌ Next.js "module not found"?

Delete and reinstall:

```
rm -rf node_modules package-lock.json
npm install
```

### ❌ Python errors?

Try reinstalling:

```
pip install -r requirements.txt
```

---

# 🎉 You can now continue Stratos development from ANY computer

The README now covers:

✔ Frontend setup
✔ Backend setup
✔ Node & npm installation
✔ Environment variable setup
✔ GitHub workflow
✔ Everything needed to fully resume work


