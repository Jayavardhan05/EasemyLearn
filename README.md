# EaseMyLearn

EaseMyLearn is an AI-powered learning assistant that helps users learn from their own PDF and DOCX documents.

Users can upload a document and ask questions about its content. The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant sections from the uploaded document and generate answers using Google Gemini.

## Live Demo

**Frontend:**
https://easemylearn.streamlit.app/

## Features

* Upload PDF and DOCX documents
* Extract text from uploaded documents
* Split documents into smaller chunks
* Store document chunks in ChromaDB
* Retrieve relevant chunks using semantic search
* Ask questions about the uploaded document
* Generate answers using Google Gemini
* Answers are restricted to the uploaded document context
* Reject questions when the required information cannot be found
* Maintain chat history during the current session
* Unique `document_id` keeps documents isolated from each other
* FastAPI backend and Streamlit frontend
* Deployed frontend and backend

## Tech Stack

### Frontend

* Streamlit
* Python
* Requests

### Backend

* FastAPI
* Uvicorn
* Python

### Document Processing

* PyPDF
* python-docx

### Vector Database

* ChromaDB

### AI

* Google Gemini

### Deployment

* Streamlit Community Cloud
* Render

## Architecture

```text
                    User
                     |
                     v
          Streamlit Frontend
                     |
                     | HTTP / HTTPS
                     v
             FastAPI Backend
                     |
          +----------+----------+
          |                     |
          v                     v
   Document Processing      ChromaDB
          |                     |
          |                     |
          +----------+----------+
                     |
                     v
               Gemini API
                     |
                     v
               AI Response
```

## RAG Workflow

When a document is uploaded:

```text
PDF / DOCX
    |
    v
Text Extraction
    |
    v
Text Chunking
    |
    v
ChromaDB
    |
    v
Store chunks with document_id
```

When the user asks a question:

```text
User Question
      |
      v
ChromaDB Semantic Search
      |
      v
Relevant Document Chunks
      |
      v
Gemini
      |
      v
Answer based only on retrieved context
```

The application also uses a relevance threshold so that unrelated questions can return:

```text
I couldn't find this information in the uploaded document.
```

## Project Structure

```text
EaseMyLearn/
│
├── backend/
│   ├── .gitignore
│   ├── main.py
│   ├── requirements.txt
│   │
│   └── services/
│       ├── document_processor.py
│       ├── gemini_service.py
│       ├── text_chunk.py
│       └── vector_store.py
│
└── frontend/
    ├── app.py
    └── requirements.txt
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Jayavardhan05/EasemyLearn.git
cd EasemyLearn
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\activate
```

### 3. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure Gemini API

Create:

```text
backend/.env
```

Add:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Do not commit the `.env` file to GitHub.

### 5. Start the backend

From the `backend` directory:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Install frontend dependencies

Open another terminal:

```bash
cd frontend
pip install -r requirements.txt
```

Create:

```text
frontend/.env
```

For local development:

```env
BACKEND_URL=http://127.0.0.1:8000
```

### 7. Start Streamlit

```bash
streamlit run app.py
```

The frontend will normally be available at:

```text
http://localhost:8501
```

## Environment Variables

### Backend

```env
GEMINI_API_KEY=your_gemini_api_key
```

### Frontend

For local development:

```env
BACKEND_URL=http://127.0.0.1:8000
```

For production:

```env
BACKEND_URL=https://your-render-backend-url.onrender.com
```

The production environment variable should be configured through the deployment platform rather than committed to the repository.

## API Endpoints

### `GET /`

Checks whether the API is running.

### `GET /hello`

Returns a simple test response.

### `POST /upload`

Uploads and processes a PDF or DOCX document.

The backend:

1. Validates the file type.
2. Saves the document.
3. Extracts its text.
4. Splits the text into chunks.
5. Stores the chunks in ChromaDB.
6. Generates a unique `document_id`.

### `POST /ask`

Accepts:

```json
{
  "question": "What technologies are used?",
  "document_id": "document-id"
}
```

The backend retrieves relevant chunks belonging to that document and sends them as context to Gemini.

## Document Isolation

Each uploaded document receives a unique:

```text
document_id
```

The ID is stored as metadata alongside the document chunks in ChromaDB.

When searching, the backend filters using:

```text
document_id
```

This prevents questions from retrieving chunks belonging to another uploaded document.

## Deployment

The current deployment uses:

```text
Streamlit Community Cloud
        |
        v
Render
        |
        v
FastAPI Backend
```

The Streamlit frontend uses the `BACKEND_URL` environment variable to communicate with the deployed FastAPI backend.

This allows the same frontend code to work in both environments:

```text
Local:
BACKEND_URL=http://127.0.0.1:8000

Production:
BACKEND_URL=https://your-render-backend.onrender.com
```

## Current Limitations

* No user authentication
* No persistent user accounts
* ChromaDB currently uses filesystem-based persistence
* No background job queue for long-running AI requests
* No document management interface
* No multi-user account system
* Scanned/image-only PDFs may require OCR support
* Production storage architecture can be improved for larger scale

## Future Improvements

Possible future improvements include:

* User authentication
* Redis and background job queues
* Rate limiting
* Cloud-based persistent vector storage
* Document management
* Multiple document collections
* Learning paths and personalized study schedules
* Voice-based learning and mock interviews
* Better document processing and OCR
* Streaming AI responses
* Docker-based deployment

## License

This project is currently intended as a personal/educational project.
