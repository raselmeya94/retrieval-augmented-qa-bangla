
# # # app.py

# # from fastapi import FastAPI
# # from fastapi import FastAPI, Query
# # from fastapi.middleware.cors import CORSMiddleware
# # from load_vectordb import load_vectorstore
# # from rag_pipeline import answer_question

# # # app = FastAPI()
# # # # CORS (optional)
# # # app.add_middleware(
# # #     CORSMiddleware,
# # #     allow_origins=["*"], allow_credentials=True,
# # #     allow_methods=["*"], allow_headers=["*"],
# # # )


# # vectordb = load_vectorstore()

# # # @app.get("/ping")
# # # def ping():
# # #     return {"message": "pong"}

# # # @app.get("/ask")
# # # def ask_question(query: str):
# # #     from rag_pipeline import get_rag_chain

# # #     qa_chain, _ = get_rag_chain(vectorstore) 

# # #     answer = qa_chain.run(query)
# # #     return {"answer": answer}


# # # if __name__ == "__main__":
# # #     while True:
# # #         query = input("❓ প্রশ্ন দিন (Bengali/English): ")
# # #         answer = answer_question(query, vectordb)
# # #         print("\n✅ Answer:", answer)
# # #         if query=="clear":
# # #             break


# # app.py

# from fastapi import FastAPI, Query
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from datetime import datetime
# from pymongo import MongoClient
# from load_vectordb import load_vectorstore
# from rag_pipeline import answer_question

# # Initialize FastAPI
# app = FastAPI()

# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], allow_credentials=True,
#     allow_methods=["*"], allow_headers=["*"],
# )

# # Load vector database
# vectordb = load_vectorstore()

# # MongoDB short-term memory setup
# client = MongoClient("mongodb://localhost:27017")
# db = client["rag_short_memory"]
# collection = db["qa_logs"]

# # Request model
# class QueryRequest(BaseModel):
#     query: str
#     user_id: str = "anonymous"  # optional user tracking


# # Ask endpoint
# @app.post("/ask")
# def ask_question(request: QueryRequest):
#     query = request.query
#     user_id = request.user_id

#     # Get answer from RAG pipeline
#     answer = answer_question(query, vectordb)

#     # Log into MongoDB (Short-term memory)
#     log = {
#         "query": query,
#         "answer": answer,
#         "timestamp": datetime.utcnow()
#     }
#     collection.insert_one(log)

#     return {
#         "query": query,
#         "answer": answer
#     }
# import uuid
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from datetime import datetime
# from pymongo import MongoClient, ReturnDocument
# from load_vectordb import load_vectorstore
# from rag_pipeline import answer_question

# app = FastAPI()

# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], allow_credentials=True,
#     allow_methods=["*"], allow_headers=["*"],
# )

# # Load vector database
# vectordb = load_vectorstore()

# # MongoDB setup (single collection for logs and counter)
# client = MongoClient("mongodb://localhost:27017")
# db = client["rag_short_memory"]
# logs_collection = db["qa_logs"]


# # Request model
# class QueryRequest(BaseModel):
#     query: str
# def get_or_create_session_id(session_id: str = None) -> str:
#     if session_id is None:
#         return str(uuid.uuid4())
#     return session_id
# SHORT_TERM_MEMORY_RETRIEVE = 2

# def get_recent_short_term_memory(session_number: int, limit=SHORT_TERM_MEMORY_RETRIEVE):
#     # Fetch last N interactions for this session ordered by time descending
#     recent_logs = logs_collection.find(
#         {"session_number": session_number}
#     ).sort("timestamp", -1).limit(limit)
#     # Reverse so oldest first
#     return list(recent_logs)[::-1]


# @app.post("/ask")
# def ask_question(request: QueryRequest):
#     session_id = get_or_create_session_id(request.session_id)
#     query = request.query

#     # Get answer from RAG pipeline
#     answer = answer_question(query, vectordb)

#     # Log into MongoDB short-term memory with session_id
#     log = {
#         "session_id": session_id,
#         "query": query,
#         "answer": answer,
#         "timestamp": datetime.utcnow()
#     }
#     logs_collection.insert_one(log)

#     return {
#         "session_id": session_id,
#         "query": query,
#         "answer": answer,
#     }

import os
import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from pymongo import MongoClient
from load_vectordb import load_vectorstore
from rag_pipeline import answer_question
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load vector database
vectordb = load_vectorstore()

SHORT_TERM_MEMORY_RETRIEVE = int(os.getenv("SHORT_TERM_MEMORY_RETRIEVE", 2)) 


# MongoDB for Short-Term Memory( Chating History Store)
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "rag_short_memory")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "qa_logs")

# MongoDB setup
client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB]
logs_collection = db[MONGODB_COLLECTION]


# Request model with optional session_id
class QueryRequest(BaseModel):
    query: str
    session_id: str = None  # Optional - client can pass existing session id

def get_or_create_session_id(session_id: str = None) -> str:
    """Return existing session_id or generate a new UUID if None."""
    if session_id is None:
        return str(uuid.uuid4())
    return session_id


def get_recent_short_term_memory(limit):
    """Fetch last N interactions from all logs ordered by time descending."""
    recent_logs = logs_collection.find().sort("timestamp", -1).limit(limit)
    return list(recent_logs)[::-1]  # reverse to get oldest first


@app.post("/ask")
def ask_question(request: QueryRequest):
    # Use passed session_id or create new one
    session_id = get_or_create_session_id(request.session_id)
    query = request.query

    # Retrieve recent short-term memory for session
    recent_memory = get_recent_short_term_memory(SHORT_TERM_MEMORY_RETRIEVE)
    
    prev_conversations = ""
    for log in recent_memory:
        prev_conversations += f"Q: {log['query']}\nA: {log['answer']}\n\n"
    print("Previous Conversations:: ",prev_conversations )

    answer = answer_question(query,prev_conversations,  vectordb) 

    # Log this Q&A with session id
    logs_collection.insert_one({
        "session_id": session_id,
        "query": query,
        "answer": answer,
        "timestamp": datetime.utcnow()
    })

    return {
        "query": query,
        "answer": answer,
    }
