# backend/app/services/coordinator.py
import os
from datetime import datetime
from app.services.task_builder import (
    generate_tasks_from_brief,
    generate_project_structure,
)

def run_project_brief(brief: str):
    """
    Synchronous coordinator: generate tasks (LLM or fallback) and create project files.
    Returns a dict (serializable) that the router returns directly.
    """
    # 1) generate tasks (this is synchronous wrapper around your LLM/fallback logic)
    tasks = generate_tasks_from_brief(brief)

    # 2) generate actual project structure (writes files to disk)
    project_info = generate_project_structure(brief)

    # 3) attach tasks and metadata and return
    project_info["tasks"] = tasks
    project_info["message"] = "Project generated successfully"
    project_info["generated_at"] = datetime.utcnow().isoformat() + "Z"
    return project_info
