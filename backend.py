from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from modules.chatbot import PaperChatbot
from modules.pdf_extractor import extract_text_from_pdf


app = FastAPI(title="BriefScholar API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

documents: dict[str, str] = {}


class ChatRequest(BaseModel):
    document_id: str
    question: str


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)) -> dict[str, str | int]:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    try:
        text = extract_text_from_pdf(file.file)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if not text:
        raise HTTPException(status_code=400, detail="No readable text was found in this PDF.")

    document_id = str(uuid4())
    documents[document_id] = text

    return {
        "document_id": document_id,
        "filename": file.filename or "uploaded.pdf",
        "characters": len(text),
        "preview": text[:500],
    }


@app.post("/chat")
def chat(request: ChatRequest) -> dict[str, str]:
    paper_text = documents.get(request.document_id)
    if not paper_text:
        raise HTTPException(status_code=404, detail="Uploaded paper was not found.")

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    chatbot = PaperChatbot()
    answer = chatbot.answer_question(request.question, paper_text)

    return {"answer": answer}
