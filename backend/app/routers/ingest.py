import os
import pytesseract
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import tempfile

from app.services.vectorizer import process_and_vectorize_document

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Handles PDF or image uploads for text extraction and vectorization."""
    if not file.filename.lower().endswith((".pdf", ".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 10MB).")

    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        text_output = pytesseract.image_to_string(Image.open(tmp_path))
        vectors = process_and_vectorize_document(text_output)

        os.unlink(tmp_path)
        return JSONResponse(content={"filename": file.filename, "text": text_output, "vectors": len(vectors)})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
