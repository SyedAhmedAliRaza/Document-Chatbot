# Importing necessary libraries for the RAG pipeline
from langchain_community.llms import HuggingFacePipeline  # For HuggingFace models usage with LangChain
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline  # For loading models and tokenizers
from langchain.prompts import PromptTemplate  # For creating prompt templates
from huggingface_hub import login  # For authenticating with HuggingFace
import torch  # For handling model computations

# HuggingFace token for model use validation
login(token="HUGGINGFACEHUB_API_TOKEN", add_to_git_credential=True)

def initialize_model():

    # Defining the model 
    model_name = "mistralai/Mistral-7B-Instruct-v0.2"
    
    # Loading the tokenizer for the model 
    tokenizer = AutoTokenizer.from_pretrained(model_name, token="HUGGINGFACEHUB_API_TOKEN")
    
    # Using oprimizations
   
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32, #torch_dtype=torch.float32 for CPU 
        device_map="auto", # device_map="auto" places the model on GPU/CPU 
        token="HUGGINGFACEHUB_API_TOKEN"
    )

    # Create a text generation pipeline with the model and tokenizer
   
    text_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=200,   # max_new_tokens limits the response length 
        temperature=0.7,     # temperature controls randomness
        do_sample=True  # do_sample=True enables creative responses
    )
    
    # Pipeline placement in a LangChain-compatible object
    llm = HuggingFacePipeline(pipeline=text_pipeline)
    return llm

def query_rag(vector_store, llm, question):
  
    # Searching the vector store for the top 3 most relevant documents
    docs = vector_store.similarity_search(question, k=3)
    
    # Combining the content of retrieved documents into a single context string
    context = "\n".join([doc.page_content for doc in docs])

    # Creating a prompt template to structure the input for the model
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="Context: {context}\n\nQuestion: {question}\nAnswer:"
    )

    # Formatting the prompt with the context and question
    prompt = prompt_template.format(context=context, question=question)
    
    # Generating a response using the language model
    response = llm.invoke(prompt)
    return response