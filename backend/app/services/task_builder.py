# backend/app/services/task_builder.py
import os
import asyncio
import textwrap
from datetime import datetime
from pathlib import Path

# Try to import your LLM adapter; fallback logic used if unavailable
try:
    from app.services.llm_adapter import query_llm
except Exception:
    query_llm = None


# -------------------------
# Task generation (LLM or fallback)
# -------------------------
def _fallback_task_split(brief: str):
    """Fallback logic if LLM is unavailable."""
    return [
        {"name": "Setup Backend", "description": "Initialize FastAPI backend", "assigned_to": "Backend"},
        {"name": "Setup Frontend", "description": "Initialize React app", "assigned_to": "Frontend"},
        {"name": "Integrate APIs", "description": "Connect frontend and backend", "assigned_to": "Coordinator"},
    ]


def parse_llm_response(text: str):
    """Parse LLM task output into structured JSON (very simple)."""
    tasks = []
    for line in text.splitlines():
        text_line = line.strip()
        if not text_line:
            continue
        if text_line.startswith("-"):
            name = text_line.lstrip("- ").strip()
            tasks.append({"name": name, "description": f"Task for {name}", "assigned_to": "Auto"})
        elif text_line[0].isdigit() and (text_line[1] == "." or text_line[1] == ")"):
            name = text_line.split(".", 1)[-1].strip()
            tasks.append({"name": name, "description": f"Task for {name}", "assigned_to": "Auto"})
        else:
            tasks.append({"name": text_line, "description": f"Task for {text_line}", "assigned_to": "Auto"})
    return tasks or _fallback_task_split(text)


def generate_tasks_from_brief(brief: str):
    """Synchronously run LLM (if available) and parse output; fallback otherwise."""
    if query_llm is None:
        return _fallback_task_split(brief)

    prompt = f"Break this project idea into concrete technical tasks (short list):\n{brief}"
    try:
        raw = asyncio.run(query_llm(prompt))
        if not isinstance(raw, str):
            raw = str(raw)
        tasks = parse_llm_response(raw)
        return tasks
    except Exception:
        return _fallback_task_split(brief)


# -------------------------
# Project file generation
# -------------------------
def generate_project_structure(project_name: str, base_dir: str | None = None):
    """
    Create project folder and write minimal backend/frontend starter files.
    """

    # Compute base_dir as `backend/generated_projects`
    if base_dir is None:
        base_dir = Path(__file__).resolve().parents[2] / "generated_projects"
    else:
        base_dir = Path(base_dir)

    safe_name = (
        project_name.lower()
        .strip()
        .replace(" ", "-")
        .replace("/", "-")
    )
    project_root = base_dir / safe_name
    backend_dir = project_root / "backend"
    frontend_dir = project_root / "frontend"

    backend_dir.mkdir(parents=True, exist_ok=True)
    frontend_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------
    # Backend main.py
    # -------------------------
    backend_code = textwrap.dedent(
        f"""
        # Auto-generated FastAPI backend
        from fastapi import FastAPI

        app = FastAPI(title="{project_name}")

        @app.get("/")
        def read_root():
            return {{ "message": "Welcome to the {project_name} backend!" }}
        """
    )
    (backend_dir / "main.py").write_text(backend_code, encoding="utf-8")

    # Backend requirements.txt
    (backend_dir / "requirements.txt").write_text("fastapi\nuvicorn\n", encoding="utf-8")

    # -------------------------
    # Frontend App.tsx
    # -------------------------
    frontend_code = textwrap.dedent(
        """
        import React, { useState } from 'react';

        export default function App() {
            const [brief, setBrief] = useState('');
            const [loading, setLoading] = useState(false);
            const [message, setMessage] = useState('');

            const generateProject = async () => {
                if (!brief.trim()) {
                    alert('Please enter a project brief!');
                    return;
                }
                setLoading(true);
                setMessage('');
                try {
                    const res = await fetch('http://127.0.0.1:8000/api/brief', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ brief })
                    });
                    const data = await res.json();
                    setMessage(data.message || 'Project generated!');
                } catch (err) {
                    console.error(err);
                    setMessage('Error generating project');
                } finally {
                    setLoading(false);
                }
            };

            return (
                <div style={{ padding: '2rem', fontFamily: 'sans-serif', maxWidth: 600, margin: 'auto' }}>
                    <h1>AI Project Builder</h1>
                    <p>Enter your project brief below:</p>
                    <textarea
                        value={brief}
                        onChange={(e) => setBrief(e.target.value)}
                        placeholder="e.g., Build a task management app with authentication"
                        style={{ width: '100%', height: '100px', marginBottom: '1rem' }}
                    />
                    <button
                        onClick={generateProject}
                        disabled={loading}
                        style={{
                            backgroundColor: '#007bff',
                            color: 'white',
                            padding: '0.5rem 1rem',
                            border: 'none',
                            borderRadius: '6px',
                            cursor: 'pointer'
                        }}
                    >
                        {loading ? 'Generating...' : 'Generate Project'}
                    </button>
                    {message && <p style={{ marginTop: '1rem', color: 'green' }}>{message}</p>}
                </div>
            );
        }
        """
    )
    (frontend_dir / "App.tsx").write_text(frontend_code, encoding="utf-8")

    # -------------------------
    # README
    # -------------------------
    readme_text = f"# {project_name}\n\nGenerated on {datetime.utcnow().isoformat()}Z\n\n"
    (project_root / "README.md").write_text(readme_text, encoding="utf-8")

    return {
        "project_dir": str(project_root.resolve()),
        "backend": str(backend_dir.resolve()),
        "frontend": str(frontend_dir.resolve()),
    }
