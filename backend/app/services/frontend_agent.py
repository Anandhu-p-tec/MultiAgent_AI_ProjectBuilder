import os
from datetime import datetime

def generate_frontend_code(brief: str, project_dir: str) -> str:
    os.makedirs(project_dir, exist_ok=True)

    app_tsx = f"""
import React from 'react'

export default function App() {{
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-3xl font-bold text-blue-600">Project: {brief}</h1>
      <p className="mt-4">This is an auto-generated frontend for your project.</p>
    </div>
  )
}}
"""

    with open(os.path.join(project_dir, "App.tsx"), "w", encoding="utf-8") as f:
        f.write(app_tsx.strip())

    readme = f"# Frontend for {brief}\nGenerated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    with open(os.path.join(project_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme.strip())

    return f"Frontend code generated at: {project_dir}"
