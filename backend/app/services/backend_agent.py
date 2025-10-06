import os
from datetime import datetime

def generate_backend_code(brief: str, project_dir: str) -> str:
    os.makedirs(project_dir, exist_ok=True)

    main_py = f"""
from fastapi import FastAPI

app = FastAPI(title="{brief}")

@app.get("/")
def root():
    return {{"message": "Backend for {brief} is running!"}}
"""

    with open(os.path.join(project_dir, "main.py"), "w", encoding="utf-8") as f:
        f.write(main_py.strip())

    readme = f"# Backend for {brief}\nGenerated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    with open(os.path.join(project_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme.strip())

    return f"Backend code generated at: {project_dir}"
