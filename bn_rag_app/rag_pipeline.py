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

If the context is in Bengali, respond in Bengali — even if the question is in English. If the context is in English, respond in English. If the question and context are in different languages, prioritize the language of the context for your response.

Do not use outside knowledge. Only use the information from the context to generate a helpful and accurate answer.

✍️ Answer Format Rules:

1. For short or factual questions (e.g., names, dates, numbers, terms):
   - Provide a concise, direct answer.
   - Example:
     প্রশ্ন: 'অপরিচিতা' গল্পের নায়কের নাম কী?
     উত্তর: অনুপম

2. For reasoning, discussion, or descriptive questions (e.g., “বর্ণনা করো”, “কেন”, “কিভাবে”, “ব্যাখ্যা করো”):
   - Use the context to infer and explain the answer briefly.
   - If the context provides partial hints, use reasoning to construct the answer from the given information.
   - Keep the tone informative and focused.
   - Do not guess using outside knowledge.

If the question is short or direct, provide a concise answer without unnecessary elaboration. Only provide explanations if the question requires more detail.

Based on the context, try your best to answer every question.

If the correct answer is not present or clearly missing in the context:
Return: "প্রসঙ্গ থেকে সঠিক উত্তর নির্ধারণ করা যায়নি।"
"""),

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
