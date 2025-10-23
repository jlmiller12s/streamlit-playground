import streamlit as st
import requests

st.title("API Test – Streamlit Sandbox")

if st.button("Fetch Tasks"):
    r = requests.get("https://jsonplaceholder.typicode.com/todos")
    data = r.json()[:10]  # limit for demo
    st.write("✅ Success! Showing sample data:")
    st.dataframe(data)
