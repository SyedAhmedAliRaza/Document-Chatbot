# Importing Streamlit and utility functions
import streamlit as st # From streamlit folder -> config.toml
from utils.document_processor import process_documents  # For processing uploaded files
from utils.rag_pipeline import initialize_model, query_rag  # For model and RAG pipeline
from utils.ui_components import render_chat_interface, display_message  # For UI rendering

def main():
 
    # Setting up the Streamlit page configuration
    st.set_page_config(page_title="AI Document Chatbot", page_icon="📄", layout="wide")
    
    # Rendering the chat interface and get user inputs
    uploaded_files, user_input = render_chat_interface()
    
    # Initializing the language model if not already done
    if "llm" not in st.session_state:
        with st.spinner("Initializing AI model..."):
            st.session_state.llm = initialize_model()
    
    # Processing uploaded files and create a vector store
    if uploaded_files and st.session_state.vector_store is False:
        with st.spinner("Processing documents..."):
            st.session_state.vector_store = process_documents(uploaded_files)
        display_message("assistant", "Documents processed successfully!")
    
    # Handling user queries using the RAG pipeline
    if user_input and st.session_state.vector_store:
        display_message("user", user_input)
        with st.spinner("Generating response..."):
            response = query_rag(st.session_state.vector_store, st.session_state.llm, user_input)
            display_message("assistant", response)

# Running the app
if __name__ == "__main__":
    main()