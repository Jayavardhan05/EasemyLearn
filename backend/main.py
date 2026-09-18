from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import shutil
from services.document_processor import extract_text
from services.text_chunk import chunk_text
from services.vector_store import add_chunks
import uuid
from pydantic import BaseModel
from services.vector_store import search_chunks
from services.gemini_service import generate_answer
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

# Folder where uploaded documents will be stored
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Allowed document extensions
ALLOWED_EXTENSIONS = {".pdf", ".docx"}


@app.get("/")
def home():
    return {
        "message": "AI Learning Assistant API is running"
    }


@app.get("/hello")
def hello():
    return {
        "message": "Hello from EaseMyLearn"
    }


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    # Get file extension
    file_extension = Path(file.filename).suffix.lower()

    # Validate file extension
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed"
        )

    # Create file path
    file_path = UPLOAD_DIR / file.filename
    document_id = str(uuid.uuid4())
    # Save uploaded file
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    try:
        text = extract_text(str(file_path))
        chunks = chunk_text(text)
        add_chunks(chunks, document_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract text: {str(e)}"
        )

    return {
    "message": "File uploaded and processed successfully",
    "document_id": document_id,
    "filename": file.filename,
    "content_type": file.content_type,
    "characters": len(text),
    "number_of_chunks": len(chunks)
}
class Question(BaseModel):
    question: str
    document_id: str


@app.post("/ask")
def ask_question(data: Question):
    chunks = search_chunks(
        data.question,
        data.document_id
    )

    if not chunks:
        return {
            "question": data.question,
            "answer": "I couldn't find this information in the uploaded document."
        }

    answer = generate_answer(
        data.question,
        chunks
    )

    return {
        "question": data.question,
        "answer": answer
    }