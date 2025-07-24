import os
import re
from dotenv import load_dotenv
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from text_preprocessing import text_extractor ,markdown_page_split

load_dotenv()

VECTOR_STORE_DIR = "vector_store"


def build_vectorstore(pdf_path: str, api_key: str, language: str):

    text = text_extractor(pdf_path, api_key, language)
    if not text:
        raise ValueError("❌ No text extracted from the PDF.")

    docs = markdown_page_split(text, source=os.path.basename(pdf_path))

    splitter = RecursiveCharacterTextSplitter(chunk_size=4096, chunk_overlap=300)
    chunks = splitter.split_documents(docs)
    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
    with open(os.path.join(VECTOR_STORE_DIR, "all_chunks.txt"), "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk.page_content + "\n" + "+" * 50 + "\n")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embedding=embeddings)
    vectorstore.save_local(VECTOR_STORE_DIR)

    print(f"✅ Vector store saved to: {VECTOR_STORE_DIR}")
    return vectorstore


# def load_vectorstore():

#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#     vectorstore = FAISS.load_local(
#         VECTOR_STORE_DIR,
#         embeddings,
#         allow_dangerous_deserialization=True,
#     )
#     print(f"✅ Vector store loaded from: {VECTOR_STORE_DIR}")
#     return vectorstore
