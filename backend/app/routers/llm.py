from fastapi import APIRouter, HTTPException
from app.services.llm_adapter import query_llm

router = APIRouter()

@router.post("/query")
async def query_model(request: dict):
    """Send a prompt to the configured LLM (Gemini / Ollama / HuggingFace)."""
    if "prompt" not in request:
        raise HTTPException(status_code=400, detail="Missing 'prompt' field.")

    try:
        response = await query_llm(request["prompt"])
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
