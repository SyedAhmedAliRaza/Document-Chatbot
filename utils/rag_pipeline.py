from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain.prompts import PromptTemplate
from huggingface_hub import login
import torch
import os

os.environ["HF_HOME"] = "/content/cache"
try:
    login(token=os.environ["HUGGINGFACEHUB_API_TOKEN"])
except KeyError:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN not set in environment or Colab Secrets")

def initialize_model():
    try:
        model_name = "meta-llama/Llama-3.2-1B-Instruct"
        tokenizer = AutoTokenizer.from_pretrained(model_name, token=os.environ["HUGGINGFACEHUB_API_TOKEN"])
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,  # Use FP16 without quantization
            device_map="auto",
            token=os.environ["HUGGINGFACEHUB_API_TOKEN"],
            cache_dir="/content/cache"
        )
        text_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=700,
            temperature=0.7,
            do_sample=True,
            device_map="auto"
        )
        llm = HuggingFacePipeline(pipeline=text_pipeline)
        return llm
    except Exception as e:
        raise RuntimeError(f"Failed to initialize model: {e}")

def query_rag(vector_store, llm, question):
    try:
        docs = vector_store.similarity_search(question, k=10)
        context = "\n".join([doc.page_content for doc in docs])
        prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="Context: {context}\n\nQuestion: {question}\nAnswer:"
        )
        prompt = prompt_template.format(context=context, question=question)
        response = llm.invoke(prompt)
        return response
    except Exception as e:
        return f"Error generating response: {e}"
