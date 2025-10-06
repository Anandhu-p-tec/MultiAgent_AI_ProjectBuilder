from app.services.vectorizer import process_and_vectorize_document

def test_vectorizer_creates_vectors():
    sample_text = "This is a test document."
    result = process_and_vectorize_document(sample_text)
    assert isinstance(result, list)
    assert len(result) == 1
    assert "id" in result[0]
