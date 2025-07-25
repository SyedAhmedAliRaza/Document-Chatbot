# Importing libraries for document processing and vector storage
from langchain.text_splitter import RecursiveCharacterTextSplitter  # For splitting text into chunks
from langchain_community.vectorstores import FAISS  # FAISS for vector store integration
from langchain_community.embeddings import HuggingFaceEmbeddings  # For generating text embeddings
from PyPDF2 import PdfReader  # For reading PDF files
from docx import Document  # For reading DOCX files
import os  # For file operations

def extract_text(file_path):
  
    # Get the file extension (e.g., .pdf, .docx, .txt)
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    # Handles PDF files
    if ext == ".pdf":
        with open(file_path, "rb") as file:  # Open in binary mode for PDFs
            reader = PdfReader(file)
            for page in reader.pages:
                # Extract text from each page, use empty string if no text
                text += page.extract_text() or ""
    
    # Handles DOCX files
    elif ext == ".docx":
        doc = Document(file_path)
        # Join all paragraph texts with newlines
        text = "\n".join([para.text for para in doc.paragraphs])
    
    # Handles TXT files
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
    
    return text

def process_documents(uploaded_files):
    
    texts = []
    # Processes each uploaded file
    for file in uploaded_files:
        # Saves the uploaded file temporarily
        file_path = f"temp_{file.name}"
        with open(file_path, "wb") as f:
            f.write(file.read())
        
        # Extracts text from the file
        text = extract_text(file_path)
        texts.append(text)
        
        # Cleans up by removing the temporary file
        os.remove(file_path)  

    # Combines all texts and split into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = text_splitter.split_text("\n".join(texts))

    # Creates embeddings using a lightweight sentence transformer model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Creates a FAISS vector store from the text chunks and embeddings
    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store