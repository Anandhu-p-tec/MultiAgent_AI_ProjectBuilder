import os
import httpx
from tenacity import retry, stop_after_attempt, wait_fixed
from app.config import settings

# Simple cache (in-memory)
_cache = {}

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def query_llm(prompt: str) -> str:
    """Unified interface for Gemini / Ollama / HuggingFace models."""

    if prompt in _cache:
        return _cache[prompt]

    backend = settings.LLM_BACKEND.lower()

    if backend == "gemini":
        response = await _call_gemini(prompt)
    elif backend == "ollama":
        response = await _call_ollama(prompt)
    elif backend == "hf":
        response = await _call_huggingface(prompt)
    else:
        raise ValueError(f"Unsupported backend: {backend}")

    _cache[prompt] = response
    return response


async def _call_gemini(prompt: str) -> str:
    """Send a prompt to Google Gemini via REST API."""
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()
        data = r.json()
        return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No output")


async def _call_ollama(prompt: str) -> str:
    """Call a locally running Ollama model."""
    url = f"{settings.OLLAMA_URL}/api/generate"
    payload = {"model": "llama3", "prompt": prompt}
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()
        for line in r.text.splitlines():
            if line.strip():
                try:
                    return line
                except Exception:
                    continue
    return "No response from Ollama."


async def _call_huggingface(prompt: str) -> str:
    """Call Hugging Face Inference endpoint (free-tier models)."""
    api_key = settings.HUGGINGFACE_API_KEY
    if not api_key:
        raise ValueError("Missing HUGGINGFACE_API_KEY")

    url = "https://api-inference.huggingface.co/models/google/flan-t5-base"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"inputs": prompt}

    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(url, headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()
        return data[0]["generated_text"] if isinstance(data, list) else str(data)
