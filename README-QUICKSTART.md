# Quickstart

This workspace contains a scaffold for the Multiagent AI Project Builder with a backend (FastAPI) and a frontend (Vite + React + TypeScript).

What I created for you in this session:

- Top-level files: `LICENSE`, `CONTRIBUTING.md`, `CHANGELOG.md`, `.editorconfig`, `.gitignore`, `.env.example`, `Make.ps1`, `docker-compose.windows.yml`
- CI: `.github/workflows/ci.yml`
- VS Code helpers: `.vscode/*`
- Backend: `backend/` with `pyproject.toml`, `requirements.txt`, `Dockerfile`, `.env.sample`, `sample_data/sample.pdf`, and `app/` package with minimal routes, services, worker, and tests.
- Frontend: `frontend/` with `index.html`, `package.json`, `tsconfig.json`, `vite.config.ts`, `tailwind.config.ts`, `postcss.config.js`, `src/` (App, main, components, pages, api, tests), and `public/sample.gltf`.

Quick run (locally):

- Backend (Windows PowerShell):

```powershell
python -m pip install -r backend/requirements.txt
python backend/app/main.py
```

- Frontend:

```powershell
cd frontend
npm install
npm run dev
```

Notes:

- The scaffold files are minimal placeholders to get started. Install project dependencies for the frontend and backend before running.
- Tests included are basic stubs (pytest for backend).

Next steps you might want:

- Implement real OCR/vectorization/LLM integrations in `backend/app/services`.
- Wire API routes to services.
- Add proper environment management and secrets.
- Replace placeholder tests with real tests.
