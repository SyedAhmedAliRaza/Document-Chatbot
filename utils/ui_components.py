%%writefile utils/ui_components.py
import streamlit as st
from datetime import datetime

def render_chat_interface():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #FFFFFF 0%, #FFC107 30%, #FFFFFF 100%);
        }
        .stTitle {
            color: #FFFFFF !important;
            font-weight: bold;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.8), 0 0 20px rgba(255, 98, 0, 0.5);
            animation: glow 1.5s ease-in-out infinite alternate;
            background: #FF6200;
            padding: 10px 20px;
            border-radius: 10px;
            display: inline-block;
        }
        @keyframes glow {
            from { text-shadow: 0 0 5px rgba(255, 255, 255, 0.8), 0 0 10px rgba(255, 98, 0, 0.5); }
            to { text-shadow: 0 0 15px rgba(255, 255, 255, 1.0), 0 0 25px rgba(255, 98, 0, 0.7); }
        }
        .stFileUploader {
            background: #FFC107;
            border-radius: 12px;
            padding: 15px;
            border: 2px solid #FF6200;
            transition: all 0.3s ease;
        }
        .stFileUploader:hover {
            border-color: #FFFFFF;
            box-shadow: 0 0 12px rgba(255, 98, 0, 0.5);
        }
        .file-type-badge {
            background: #FF6200;
            color: #FFFFFF;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 12px;
            margin-left: 10px;
        }
        .stChatMessage {
            border-radius: 12px !important;
            padding: 15px !important;
            margin: 5px 0 !important;
            background: #FFC107 !important;
            border: 1px solid #FF6200 !important;
            color: #FFFFFF !important;
        }
        .stChatMessage.user {
            background: #FF6200 !important;
            color: #FFFFFF !important;
            border: 1px solid #FFC107 !important;
        }
        .timestamp {
            font-size: 10px;
            color: #FFFFFF;
            margin-top: 5px;
        }
        .stButton > button {
            background: #FF6200;
            color: #FFFFFF;
            border-radius: 12px;
            border: none;
            padding: 10px 20px;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background: #FFC107;
            box-shadow: 0 0 10px rgba(255, 98, 0, 0.5);
        }
        .chat-container {
            max-height: 400px;
            overflow-y: auto;
            padding: 15px;
            border-radius: 12px;
            background: #FFC107;
            border: 1px solid #FF6200;
        }
        .sidebar .stButton > button {
            width: 100%;
            margin-bottom: 10px;
        }
        .sidebar-content {
            background: #FFFFFF;
            padding: 15px;
            border-radius: 12px;
            border: 1px solid #FF6200;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
       
        st.markdown("<h1 style='color: #FF6200;'>Settings</h1>", unsafe_allow_html=True)
        if st.button("Clear Chat History", key="clear_history"):
            st.session_state.chat_history = []
            st.session_state.vector_store = None
            st.markdown("<span style='color: #FF6200;'>Chat history cleared!</span>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color: #FF6200;'>", unsafe_allow_html=True)
        st.markdown("<p style='color: #FF6200;'>AI Document Chatbot v2.0<br>Powered by Llama</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<h1 class='stTitle' >📄 AI Document Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #FF6200;'>Upload documents and ask questions with AI assistance.</p>", unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload Documents",
        accept_multiple_files=True,
        type=["pdf", "docx", "txt"],
        help="Supported formats: PDF, DOCX, TXT"
    )
    if uploaded_files:
        st.markdown("<div style='margin-top: 10px;'>", unsafe_allow_html=True)
        for file in uploaded_files:
            file_type = file.name.split('.')[-1].upper()
            st.markdown(f"<span style='color: #FF6200;'>{file.name}</span> <span class='file-type-badge'>{file_type}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None

    st.subheader("Chat History", divider="orange")
    chat_container = st.container(border=True)
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                st.markdown(f"<div class='timestamp'>{message['timestamp']}</div>", unsafe_allow_html=True)

    user_input = st.chat_input("Type your question here...")
    return uploaded_files, user_input

def display_message(role, content):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with st.chat_message(role):
        st.markdown(content)
        st.markdown(f"<div class='timestamp'>{timestamp}</div>", unsafe_allow_html=True)
    st.session_state.chat_history.append({"role": role, "content": content, "timestamp": timestamp})
