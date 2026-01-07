import streamlit as st
from dotenv import load_dotenv
load_dotenv()
def chat():
    st.subheader("Ask a Question")

    question = st.text_input("Your question")

    ask = st.button("Ask")

    return question, ask
