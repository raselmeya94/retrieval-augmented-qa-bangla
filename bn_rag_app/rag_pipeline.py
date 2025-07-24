import os
from load_vectordb import load_vectorstore
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
import asyncio
from googletrans import Translator

load_dotenv()
top_k = int(os.getenv("TOP_K", 3)) 


QA_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system",
         """You are an intelligent assistant tasked with answering questions strictly based on the provided context.

If the context is in Bengali, answer in Bengali — even if the question is in English. If the context is in English, answer in English. If the question and context are in different languages, prioritize the language of the context for your response.

Do not use outside knowledge. Only use the information from the context to generate a helpful and accurate answer.

If the question is short or direct, provide a concise answer without extra explanations. Only add explanations if the question requires it.
If the answer is in multiple-choice format (e.g., ক, খ, গ, ঘ), make sure to include the corresponding option value exactly as it appears in the options. Example: 
৬। 'অপরিচিতা' গল্পে রেলকর্মচারী কতটি টিকিট বেঞ্চে ঝুলিয়েছিল? [য. বো. '২২]
(ক) একটি
(খ) দুইটি
(গ) তিনটি
(ঘ) চারটি
উত্তর: খ (দুইটি)
If the answer is not clearly found in the context, say so honestly."""),

        ("human", "Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer:"),
    ]
)



def get_rag_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})

    llm = ChatMistralAI(
        model="mistral-large-latest",
        temperature=0,
        max_retries=2,
        api_key=os.getenv("MISTRAL_API_KEY")
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": QA_PROMPT},
        return_source_documents=True  # 👈 enables returning retrieved chunks
    )

    return qa_chain, retriever



async def translate_query_to_bengali(query: str) -> str:
    # If query contains English letters, translate asynchronously
    if any('a' <= c.lower() <= 'z' for c in query):
        async with Translator() as translator:
            translation = await translator.translate(query, src='en', dest='bn')
            return translation.text
    else:
        return query

# def answer_question(query, prev_conversations,  vectordb):
#     # Translate query if needed
#     # Run async function from sync context
#     translated_query = asyncio.run(translate_query_to_bengali(query))
#     print("question:",translated_query )

#     qa_chain, retriever = get_rag_chain(vectordb)

#     # Use the Bengali query for retrieval & QA
#     result = qa_chain(translated_query)  # returns dict with answer and source_documents
#     answer = result["result"]
#     # sources = result["source_documents"]

#     # print("\n🔎 Retrieved Chunks:")
#     # for i, doc in enumerate(sources, start=1):
#     #     print(f"\n--- Chunk {i} ---")
#     #     print(doc.page_content)

#     return answer

# def answer_question(query, prev_conversations, vectordb):
#     # Translate user query (if English → Bangla)
#     translated_query = asyncio.run(translate_query_to_bengali(query))
#     print("🔍 Translated Query:", translated_query)

#     # For retrieval: Use only the current translated query
#     qa_chain, retriever = get_rag_chain(vectordb)
#     retrieved_docs = retriever.get_relevant_documents(translated_query)

#     # For generation: Add short-term memory (recent turns + current query)
#     short_term_context = f"Previous Conversations: {prev_conversations} \n Current Question: {translated_query}"

#     # Manually run the chain with custom input
#     result = qa_chain.combine_documents_chain.run(
#         input_documents=retrieved_docs,
#         question=short_term_context
#     )

#     return result

def answer_question(query, prev_conversations, vectordb):
    translated_query = asyncio.run(translate_query_to_bengali(query))
    print("🔍 Translated Query:", translated_query)

    qa_chain, retriever = get_rag_chain(vectordb)

    # Step 1: Only retrieve based on the query (not the prev conv)
    retrieved_docs = retriever.invoke(translated_query)
    # print("Pre_Cons:", prev_conversations)

    # Step 2: Prepare a custom prompt for LLM using both retrieved context and previous chats
    short_term_context = f"Previous Conversations: {prev_conversations}\nCurrent Question: {translated_query}"

    formatted_prompt = QA_PROMPT.format(
        context="\n\n".join([doc.page_content for doc in retrieved_docs]),
        question=short_term_context
    )

    # Step 3: Use LLM directly with the custom prompt
    response = qa_chain.combine_documents_chain.llm_chain.llm.invoke(formatted_prompt)

    return response.content



def llm_evalution(query, vectordb):

    translated_query = asyncio.run(translate_query_to_bengali(query))
    print("question:",translated_query )

    qa_chain, retriever = get_rag_chain(vectordb)

    # Use the Bengali query for retrieval & QA
    result = qa_chain(translated_query)  
    answer = result["result"]
    sources = result["source_documents"]



    return answer , sources



# import os
# from dotenv import load_dotenv
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain_community.vectorstores import Chroma
# from text_prepare import text_extractor, markdown_page_split

# load_dotenv()

# VECTOR_STORE_DIR = "vector_store"


# def build_vectorstore(pdf_path: str, api_key: str, language: str):
#     text = text_extractor(pdf_path, api_key, language)
#     if not text:
#         raise ValueError("❌ No text extracted from the PDF.")

#     docs = markdown_page_split(text, source=os.path.basename(pdf_path))

#     splitter = RecursiveCharacterTextSplitter(chunk_size=4096, chunk_overlap=300)
#     chunks = splitter.split_documents(docs)

#     os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
#     with open(os.path.join(VECTOR_STORE_DIR, "all_chunks.txt"), "w", encoding="utf-8") as f:
#         for chunk in chunks:
#             f.write(chunk.page_content + "\n" + "+" * 50 + "\n")

#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#     vectorstore = Chroma.from_documents(
#         documents=chunks,
#         embedding=embeddings,
#         persist_directory=VECTOR_STORE_DIR,
#     )

#     vectorstore.persist()
#     print(f"✅ Vector store saved to: {VECTOR_STORE_DIR}")
#     return vectorstore


# def load_vectorstore():
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#     vectorstore = Chroma(
#         persist_directory=VECTOR_STORE_DIR,
#         embedding_function=embeddings
#     )

#     print(f"✅ Vector store loaded from: {VECTOR_STORE_DIR}")
#     return vectorstore
