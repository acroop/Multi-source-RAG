import streamlit as st
from dotenv import load_dotenv
load_dotenv()

def sidebar():
    st.sidebar.title("Documents")

    
    
    selected_doc = st.sidebar.selectbox(
        "Select a document",
        options=["None", "Doc 1", "Doc 2"]
    )
    return selected_doc