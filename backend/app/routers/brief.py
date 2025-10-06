from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.services.coordinator import run_project_brief
import os
import shutil
import tempfile
from pathlib import Path

router = APIRouter()

class BriefRequest(BaseModel):
    brief: str


@router.post("/", name="generate_project_brief")
def generate_project_brief_endpoint(request: BriefRequest):
    """
    Accepts a short project brief and coordinates the project generation.
    This calls a synchronous coordinator function (no await).
    """
    result = run_project_brief(request.brief)
    return result


@router.get("/download/{project_name}")
def download_project(project_name: str):
    """
    Compress the generated project folder into a ZIP file
    and send it to the frontend.
    """
    # Base folder (where projects are created)
    base_dir = Path(__file__).resolve().parents[2] / "generated_projects"
    project_dir = base_dir / project_name

    if not project_dir.exists():
        raise HTTPException(status_code=404, detail="Project not found")

    # Create a temporary zip file
    temp_dir = tempfile.gettempdir()
    zip_path = os.path.join(temp_dir, f"{project_name}.zip")

    # Remove old zip if exists
    if os.path.exists(zip_path):
        os.remove(zip_path)

    shutil.make_archive(zip_path.replace(".zip", ""), 'zip', project_dir)

    return FileResponse(
        zip_path,
        media_type='application/zip',
        filename=f"{project_name}.zip"
    )
