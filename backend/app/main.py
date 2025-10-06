from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.routers import ingest, tasks, llm, brief

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Project Builder API",
    version="0.1.0",
    description="Backend for the AI agent coordinator and sub-agents.",
)

# CORS configuration
origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(brief.router, prefix="/api/brief")
app.include_router(brief.router, prefix="/api")
app.include_router(ingest.router, prefix="/api/ingest", tags=["Ingestion"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(llm.router, prefix="/api/llm", tags=["LLM"])
app.include_router(brief.router, prefix="/api/brief", tags=["Project Brief"])

@app.get("/")
def root():
    return {"message": "AI Agent Backend is running!"}
app.include_router(brief.router, prefix="/api/brief", tags=["Project Brief"])
