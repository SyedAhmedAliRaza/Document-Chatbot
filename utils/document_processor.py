%%writefile utils/document_processor.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import pdfplumber
from docx import Document
import os
import uuid

def extract_text(file_path):
    try:
        ext = os.path.splitext(file_path)[1].lower()
        text = ""
        if ext == ".pdf":
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        elif ext == ".docx":
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
        return text
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return ""

def process_documents(uploaded_files):
    texts = []
    temp_dir = "/content/temp_files"
    os.makedirs(temp_dir, exist_ok=True)
    try:
        for file in uploaded_files:
            file_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.name}")
            with open(file_path, "wb") as f:
                f.write(file.read())
            text = extract_text(file_path)
            if text:
                texts.append(text)
            os.remove(file_path)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=50)
        chunks = []
        for text in texts:
            chunks.extend(text_splitter.split_text(text))
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")
        vector_store = FAISS.from_texts(chunks, embeddings)
        return vector_store
    finally:
        if os.path.exists(temp_dir):
            for f in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, f))
