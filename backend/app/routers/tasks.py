from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import ProjectTask
from app.database import get_db
from fastapi import Depends
from app.services.task_builder import generate_tasks_from_brief

router = APIRouter()

@router.post("/generate")
async def generate_project_tasks(brief: dict, db: AsyncSession = Depends(get_db)):
    """Generate structured project tasks from a brief."""
    if "brief" not in brief:
        raise HTTPException(status_code=400, detail="Missing project brief.")

    tasks = generate_tasks_from_brief(brief["brief"])

    for t in tasks:
        task = ProjectTask(name=t["name"], description=t["description"], assigned_to=t["assigned_to"])
        db.add(task)
    await db.commit()

    return {"created": len(tasks), "tasks": tasks}

@router.get("/")
async def list_tasks(db: AsyncSession = Depends(get_db)):
    """List all project tasks."""
    result = await db.execute(select(ProjectTask))
    tasks = result.scalars().all()
    return tasks
