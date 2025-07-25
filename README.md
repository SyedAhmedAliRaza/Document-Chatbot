# 📄 AI Document Chatbot

AI Document Chatbot is a Streamlit-based web application that allows users to upload documents (PDF, DOCX, TXT) and interact with them using natural language queries. The app leverages a Retrieval-Augmented Generation (RAG) pipeline powered by the Mistral-7B-Instruct model to provide accurate answers from the uploaded files.

## 🚀 Features

- Upload multiple documents and chat with them
- Extracts text from documents using advanced NLP techniques
- Contextual question-answering using RAG pipeline
- Clean and responsive user interface with chat history
- Powered by open-source Hugging Face models

## 🛠️ Tech Stack

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [Transformers](https://huggingface.co/docs/transformers/)
- [PyTorch](https://pytorch.org/)
- [Hugging Face Hub](https://huggingface.co/)
- Mistral-7B-Instruct-v0.2 (LLM)

## 💻 How to Run Locally

Follow these steps to run the project on your local machine:

### 1. **Clone the repository**<br>

   -> git clone https://github.com/SyedAhmedAliRaza/Document-Chatbot.git<br>
   -> cd Document-Chatbot

### 2. **Create a virtual environment**<br>

   -> python -m venv venv<br>
   -> source venv/bin/activate
          
### 3. **Install dependencies**<br>

   -> pip install -r requirements.txt

 ### 4. **Login to Hugging Face CLI**<br>
 
   -> huggingface-cli login --token <your_token>

 ### 5. **Run the app**<br>
 
   -> streamlit run app.py<br>
   Open [http://localhost:8501](http://localhost:8501) with your browser to see the result.


