from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from rag.loaders import partition_document_from_url
from rag.processor import create_chunk_by_title, summarise_chunks
from rag.vector_store import create_vector_store

router = APIRouter()

class IngestRequest(BaseModel):
    filename: str
    file_path: str
    pdf_url: str


@router.post("/ingest")
def ingest_document(request: IngestRequest):
    try:
        print("📥 INGEST CALLED")
        print("Filename:", request.filename)
        print("File Path:", request.file_path)
        print("URL:", request.pdf_url)

        # 1️⃣ Partition document (multimodal extraction)
        elements = partition_document_from_url(request.pdf_url)
        print(f" Partitioned into {len(elements)} elements")

        if not elements:
            raise ValueError("No elements extracted from PDF")

        # 2️⃣ Chunking
        chunks = create_chunk_by_title(elements)
        print(f" Created {len(chunks)} chunks")

        # 3️⃣ AI-enhanced summarisation
        processed_chunks = summarise_chunks(chunks)
        print(f"Processed {len(processed_chunks)} chunks")

        # 4️⃣ Vector store creation
        create_vector_store(processed_chunks)
        print(" Vector store updated")

        return {
            "status": "success",
            "filename": request.filename,
            "chunks": len(processed_chunks)
        }

    except Exception as e:
        print(" INGEST FAILED:", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Ingestion failed: {str(e)}"
        )
