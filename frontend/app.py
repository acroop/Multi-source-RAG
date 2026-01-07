import streamlit as st
from utils.app_client import ask_to_backend
from components.uploader import uploader
from components.sidebar import sidebar
from components.chat import chat
from utils.app_client import send_to_backend, upload_pdfs_to_supabase
from dotenv import load_dotenv
load_dotenv()

st.title("Multi-Source RAG")

# Sidebar (document search & selection)
selected_doc = sidebar()

# Upload section
uploaded_files, upload_clicked = uploader()

if upload_clicked and uploaded_files:
    results = upload_pdfs_to_supabase(uploaded_files)

    send_to_backend(results)

    st.success("Files uploaded successfully!")

    for r in results:
        st.write(f"{r['filename']}")
        st.write(r["public_url"])

# Chat section
question, ask_clicked = chat()

if ask_clicked and question:
    st.write(f"You asked: {question}")

    answer = ask_to_backend(question)

    st.write("Answer:", answer)
