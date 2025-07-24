from embedder import build_vectorstore
from dotenv import load_dotenv
import os

load_dotenv()  
script_dir = os.path.dirname(os.path.abspath(__file__))

mistral_api_key = os.getenv("MISTRAL_API_KEY")

print("MISTRAL API Key loaded:", bool(mistral_api_key))
if __name__ == "__main__":
    pdf_file_path = os.path.join(script_dir, "../data/HSC26-Bangla1st-Paper.pdf")

    build_vectorstore(pdf_file_path, mistral_api_key , language='ben')
