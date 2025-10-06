# MultiAgent AI Project Builder

This project implements an **AI Agent System** that converts a short, high-level project brief into a set of concrete technical tasks, then uses specialized sub-agents to generate code for each component.

## 🧠 Architecture Overview

- **Coordinator Agent:**  
  Receives the project brief, decomposes it into backend and frontend tasks, dispatches to specialized sub-agents, and reviews outputs.

- **Backend Agent (Python / FastAPI):**  
  Creates APIs, database models, and business logic workflows.

- **Frontend Agent (React + TypeScript):**  
  Generates responsive UI components using Tailwind CSS and Vite.

## ⚙️ Tech Stack

| Layer        | Technology                                                             |
| ------------ | ---------------------------------------------------------------------- |
| Backend      | FastAPI (Python), SQLite / ChromaDB, RQ Worker                         |
| Frontend     | React + Vite + TypeScript + Tailwind CSS                               |
| LLM          | Gemini API (default), Ollama (local fallback), Hugging Face (optional) |
| Vector Store | Chroma (default) / FAISS (fallback)                                    |
| Job Queue    | Redis + RQ (or APScheduler fallback)                                   |

---

## 🚀 Quick Start (Windows)

See `README-QUICKSTART.md` for PowerShell setup instructions.

After setup:

- Run backend: `uvicorn backend.app.main:app --reload`
- Run frontend: `npm run dev`
- Open browser: http://localhost:5173

---

## 🧩 Folder Overview

backend/ → FastAPI app, LLM logic, vector DB, worker
frontend/ → React app (Vite + TS)
.vscode/ → Recommended VS Code workspace setup
.github/ → CI workflows

---

## 🔐 Environment

All configuration via `.env` file:

```bash
GEMINI_API_KEY=your_key_here
OLLAMA_URL=http://localhost:11434
HF_API_KEY=
DATABASE_URL=sqlite:///./backend.db
```

🧰 Developer Tools

Linting & formatting: Black (Python), ESLint + Prettier (JS)

Unit tests: pytest / vitest

Docker Compose: optional Redis container

Pre-commit hooks: recommended for CI parity
🪶 License

MIT — see LICENSE

---

/README-QUICKSTART.md

````markdown
# Quickstart — Windows PowerShell Setup

Follow these steps to run the MultiAgent AI Project Builder locally.

---

## 1️⃣ Create & activate Python environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
pip install --upgrade pip
pip install -r backend/requirements.txt
```
````
