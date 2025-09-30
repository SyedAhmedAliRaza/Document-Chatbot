%%writefile app.py
import streamlit as st
from utils.document_processor import process_documents
from utils.rag_pipeline import initialize_model, query_rag
from utils.ui_components import render_chat_interface, display_message

def main():
    st.set_page_config(page_title="AI Document Chatbot", page_icon="📄", layout="wide")
    uploaded_files, user_input = render_chat_interface()
    if "llm" not in st.session_state:
        with st.spinner("Initializing AI model..."):
            try:
                st.session_state.llm = initialize_model()
            except Exception as e:
                st.error(f"Model initialization failed: {e}")
                return
    if uploaded_files:
        with st.spinner("Processing documents..."):
            try:
                st.session_state.vector_store = process_documents(uploaded_files)
                display_message("assistant", "Documents processed successfully!")
            except Exception as e:
                st.error(f"Document processing failed: {e}")
                return
    if user_input and st.session_state.vector_store is not None:
        display_message("user", user_input)
        with st.spinner("Generating response..."):
            try:
                response = query_rag(st.session_state.vector_store, st.session_state.llm, user_input)
                display_message("assistant", response)
            except Exception as e:
                display_message("assistant", f"Error: {e}")

if __name__ == "__main__":
    main()
