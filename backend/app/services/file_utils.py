import os
import re

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def create_project_folder(base_dir: str, name: str) -> str:
    folder = os.path.join(base_dir, slugify(name))
    os.makedirs(folder, exist_ok=True)
    return folder
