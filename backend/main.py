from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.modules.chatbot import PaperChatbot
from backend.modules.core_insights import CoreInsightsBrief
from backend.modules.core_viva import CoreViva
from backend.modules.pdf_extractor import extract_text_from_pdf


app = FastAPI(title="BriefScholar API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

documents: dict[str, str] = {}

chatbots: dict[str, PaperChatbot] = {}

class ChatRequest(BaseModel):
    document_id: str
    question: str


class InsightsRequest(BaseModel):
    document_id: str


class VivaRequest(BaseModel):
    document_id: str


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

    # Store extracted text
    documents[document_id] = text

    # Create RAG chatbot for this specific document
    chatbot = PaperChatbot()
    rag_status = chatbot.prepare_paper(text)

    # Store chatbot object using document_id
    chatbots[document_id] = chatbot

    return {
        "document_id": document_id,
        "filename": file.filename or "uploaded.pdf",
        "characters": len(text),
        "preview": text[:500],
        "chunks": rag_status["total_chunks"],
    }


@app.post("/chat")
def chat(request: ChatRequest) -> dict[str, str]:
    if request.document_id not in documents:
        raise HTTPException(status_code=404, detail="Uploaded paper was not found.")

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    chatbot = chatbots.get(request.document_id)

    if chatbot is None:
        raise HTTPException(status_code=500, detail="RAG chatbot was not initialized for this paper.")

    answer = chatbot.answer_question(request.question)

    return {"answer": answer}


@app.post("/insights")
def insights(request: InsightsRequest) -> dict[str, str | list[str]]:
    paper_text = documents.get(request.document_id)
    if not paper_text:
        raise HTTPException(status_code=404, detail="Uploaded paper was not found.")

    brief = CoreInsightsBrief()
    return brief.generate(paper_text)


@app.post("/viva")
def viva(request: VivaRequest) -> dict[str, list[dict[str, str | int]]]:
    paper_text = documents.get(request.document_id)
    if not paper_text:
        raise HTTPException(status_code=404, detail="Uploaded paper was not found.")

    viva_generator = CoreViva()
    return {"questions": viva_generator.generate(paper_text)}
