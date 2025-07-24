import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

VECTOR_STORE_DIR = "../vector_store"

def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(
        VECTOR_STORE_DIR,
        embeddings,
        allow_dangerous_deserialization=True,
    )
    print(f"Vector store loaded from: {VECTOR_STORE_DIR}")
    return vectorstore
