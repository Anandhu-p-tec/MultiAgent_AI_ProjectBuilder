import pytest
import asyncio
from app.services.llm_adapter import query_llm

@pytest.mark.asyncio
async def test_query_llm_fallback(monkeypatch):
    async def fake_gemini(prompt):
        return "Simulated task output"

    monkeypatch.setattr("app.services.llm_adapter._call_gemini", fake_gemini)
    result = await query_llm("Hello test")
    assert "Simulated" in result
