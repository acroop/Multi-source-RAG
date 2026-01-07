from dotenv import load_dotenv

import os
import requests
from supabase import create_client

load_dotenv()


supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)



def upload_pdfs_to_supabase(uploaded_files):
    results = []

    for file in uploaded_files:
        if file.type != "application/pdf":
            raise ValueError(f"{file.name} is not a PDF")

        file_bytes = file.getvalue()  
        file_path = f"documents/{file.name}"

        supabase.storage.from_("rag-documents").upload(
            file_path,
            file_bytes,
            file_options={
                "content-type": "application/pdf",
                "upsert": "true"  
            }
        )

        public_url = supabase.storage.from_("rag-documents").get_public_url(file_path)

        results.append({
            "filename": file.name,
            "path": file_path,
            "public_url": public_url
        })

    return results


BACKEND_URL = "http://127.0.0.1:8000"

def send_to_backend(upload_results):
    for doc in upload_results:
        requests.post(
            f"{BACKEND_URL}/ingest",
            json={
                "filename": doc["filename"],
                "file_path": doc["path"],        # Supabase path
                "pdf_url": doc["public_url"]     # Supabase public URL
            }
        )

def ask_to_backend(question: str):
    response = requests.post(
        f"{BACKEND_URL}/ask",
        json={
            "question": question,
        }
    )

    if response.status_code == 200:
        return response.json().get("answer", "No answer found.")
    else:
        return f"Error: {response.status_code} - {response.text}"