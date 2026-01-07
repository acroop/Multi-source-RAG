# 📄 Multi-Source RAG System (Cloud-Ready)

A **Retrieval-Augmented Generation (RAG)** system that allows users to upload multiple PDF documents, store them in the cloud, and ask natural language questions grounded strictly in the uploaded content.

This project demonstrates **end-to-end RAG architecture**, combining document ingestion, vector embeddings, semantic search, and LLM-based answer generation.

---

## 🚀 Key Features

- 📤 Upload **multiple PDFs**
- ☁️ PDFs stored in **Supabase Storage (cloud)**
- 🧠 Intelligent document parsing using **Unstructured**
- ✂️ Title-aware and semantic **chunking**
- 🔎 Vector-based retrieval using **ChromaDB**
- 💬 Natural language Q&A grounded in document context
- 🪟 Clean UI built with **Streamlit**
- 🔌 Backend powered by **FastAPI**
- 🧩 Modular, extensible architecture
- ⚙️ Designed for **easy cloud migration**

---

## 🏗️ Architecture Overview

Frontend (Streamlit)
│
▼
Backend (FastAPI)
│
├── PDF Downloader (from Supabase)
├── Document Parser (Unstructured)
├── Chunking Logic
├── Embedding Generator
├── Vector Store (ChromaDB)
└── Answer Generator (LLM)

Cloud Services:

Supabase Storage → PDFs

> **Note:**  
> During development, embeddings are stored locally using ChromaDB.  
> The system is designed so the vector database can be migrated to a **cloud-hosted vector store** (Chroma Server / pgvector) without changing core RAG logic.

---

## 🧠 Tech Stack

### Frontend
- **Streamlit** – interactive UI

### Backend
- **FastAPI** – REST API
- **Uvicorn** – ASGI server

### Document Processing
- **Unstructured** – PDF partitioning
- **Poppler + Tesseract** (for hi-res parsing)

### Embeddings & Retrieval
- **ChromaDB**
- **HuggingFace Embeddings**
  - `sentence-transformers/all-MiniLM-L6-v2`

### Cloud
- **Supabase Storage** – PDF storage
- **Environment Variables** – secrets management


---

## 🔄 Data Flow

### 1️⃣ PDF Upload
- User uploads PDFs via Streamlit
- Files are uploaded to **Supabase Storage**
- Public (or signed) URLs are generated

### 2️⃣ Ingestion Pipeline
- Backend downloads PDFs from Supabase
- Documents are partitioned using Unstructured
- Content is chunked intelligently
- Embeddings are generated
- Vectors are stored in ChromaDB

### 3️⃣ Question Answering
- User asks a question
- Relevant chunks retrieved via vector similarity
- Context passed to LLM
- Grounded answer generated and returned

---

## 🧪 Example API Endpoints

### 📥 Ingest Documents
POST /ingest

**Payload**
```json
{
  "filename": "attention-is-all-you-need.pdf",
  "pdf_url": "<supabase_url>"
}
```

Ask a Question
POST /ask

**Payload**

```json
{
  "question": "What is self-attention?",
}
```

## 🛠️ Setup Instructions
1️⃣ Clone Repository

```
git clone <repo-url>
cd Multi-Source-RAG
```

2️⃣ Create Virtual Environment

```
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

3️⃣ Install Dependencies

```
pip install -r backend/requirements.txt
```

4️⃣ Environment Variables

Create .env:
```
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_key
```

5️⃣ Run Backend
```
cd backend
uvicorn main:app --reload
```

6️⃣ Run Frontend
```
cd frontend
streamlit run app.py
```


## 🔮 Future Enhancements

- ☁️ Cloud-hosted vector DB (Chroma Server / pgvector)
- 📑 Multi-document filtering & global search
- 🧠 Conversation memory
- 🔐 Authentication & user isolation
- ⚡ Streaming LLM responses
- 📊 Evaluation & confidence scoring
- 🐳 Dockerized deployment
- 🔄 CI/CD pipeline

## 👨‍💻 Author
**Supratik Das**

Engineering Student | Full Stack | AI & RAG Systems


### ⭐ Acknowledgements
- LangChain
- HuggingFace
- Supabase
- Unstructured
- ChromaDB

>If you find this project useful, feel free to ⭐ the repo!
