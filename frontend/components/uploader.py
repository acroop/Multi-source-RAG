import streamlit as st
from dotenv import load_dotenv
load_dotenv()

def uploader():
    st.subheader("Upload Document")

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"],
        accept_multiple_files=True
    )
    upload_clicked = st.button("Upload")
    

    return uploaded_file, upload_clicked