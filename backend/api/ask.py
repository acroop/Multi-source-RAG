from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from rag.vector_store import get_vector_store
from rag.generate_answer import generate_final_answer


router = APIRouter()

class AskRequest(BaseModel):
    question: str
    # document: str | None = None

@router.post("/ask")
def ask_question(request: AskRequest):
    try:
        print(" ASK CALLED")
        print("Question:", request.question)
        # print("Document:", request.document)

        # Placeholder for actual question-answering logic
        db = get_vector_store()
        print("Total vectors", db._collection.count())
        retriever = db.as_retriever()
        chunks = retriever.invoke(request.question)

        answer = generate_final_answer( chunks, request.question)

        print(" Question answered")

        return {
            "status": "success",
            "question": request.question,
            "answer": answer
        }

    except Exception as e:
        print(" ASK FAILED:", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Question answering failed: {str(e)}"
        )