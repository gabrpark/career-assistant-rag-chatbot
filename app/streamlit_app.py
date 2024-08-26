import streamlit as st
import requests

st.title("RAG Chatbot")

query = st.text_input("Enter your question:")

if st.button("Submit"):
    response = requests.post(
        "http://localhost:8000/query/", json={"question": query})
    st.write("Answer:", response.json().get("answer"))
