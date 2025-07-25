# llm_evaluation/evaluation.py
import sys
import os
import csv
from datetime import datetime

# Add 'app' directory to sys.path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'bn_rag_app'))) 

from load_vectordb import load_vectorstore
from rag_pipeline import llm_evalution 
from sentence_transformers import SentenceTransformer, util

# Load models once
embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
vectordb = load_vectorstore()


samples = [
    {
        "query": "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?",
        "expected_answer": "শুম্ভুনাথ",
    },
    {
        "query": "কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?",
        "expected_answer": "মামাকে",
    },
    {
        "query": "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?",
        "expected_answer": "১৫ বছর",
    },
    {
        "query": "'অপরিচিতা' গল্পে গল্প বলায় পটু কে?",
        "expected_answer": "হরিশ",
    },
    {
        "query": "অনুপম কল্যাণীর বিয়েতে তার কল্পনায় কোন রঙের শাড়ি পরতে দেখেছিল?",
        "expected_answer": "লাল",
    },
    {
        "query": "কল্যাণী কেন বিয়ে না করার সিদ্ধান্ত নিয়েছিল?",
        "expected_answer": "অপমানের প্রতিক্রিয়ায় এবং আত্মমর্যাদার কারণে",
    },
    {
        "query": "মেয়েটিকে কার ছবি দেখানো হয়েছিল?",
        "expected_answer": "অনুপমের",
    },
    {

        "query": "অনুপমের মামার সাথে করে সেকরা নিয়ে যাওয়ার কারণ?",
        "expected_answer": "বিশ্বাসের অভাব",
    },
    {
        "query": "এটা আপনাদের জিনিস, আপনাদের কাছেই থাক। এরূপ মন্তব্যের কারণ কী?",
        "expected_answer":  "এটা আপনাদের জিনিস, আপনাদের কাছেই থাক। অনুপমের মামাকে উদ্দেশ করে এ মন্তব্যটি করেছেন কল্যাণীর বাবা শম্ভুনাথ সেন। 'অপরিচিতা' গল্পে কল্যাণীর পিতা যখন দেখেন যে বরের মামা কন্যার গহনা যাচাই করার জন্য সঙ্গে করে সেকরা নিয়ে এসেছেন তখনই মেয়ের বাবা শম্ভুনাথ সেন সিদ্ধান্ত নেন যে, এমন লোভী ও হীন মানসিকতাসম্পন্ন মানুষের ঘরে মেয়ে দেবেন না। কন্যাপক্ষের সমস্ত গহনা একে একে পরীক্ষা করা শেষ হলে|  শম্ভুনাথ সেন একজোড়া কানের দুল সেকরাকে পরীক্ষা করতে বলেন। সেকরা জানায় এ দুলে সোনার পরিমাণ অনেক কম আছে। ঐ কানের দুল অনুপমের মামা মেয়েকে আশীর্বাদ করার সময় দিয়েছিলেন। শম্ভুনাথ সেন অনুপমের মামার হাতে কানের দুল জোড়া দিয়ে প্রশ্নোক্ত কথাটি বলেন। এ ঘটনায় অনুপমের মামা অপমানিত বোধ করেন। "

    },
    {
        "query": "'মামা বিবাহ বাড়িতে ঢুকিয়া খুশি হইলেন না।' কেন?",
        "expected_answer": "বিয়েবাড়িতে বরযাত্রীদের জায়গা সংকুলান না হওয়া এবং বিয়ের সমস্ত আয়োজন ও আতিথেয়তা প্রত্যাশিত না হওয়ায় মামা বিয়েবাড়িতে ঢুকে খুশি হলেন না।"
   }
  
]

def cosine_similarity_score(a: str, b: str) -> float:
    embeddings = embedder.encode([a, b], convert_to_tensor=True)
    return util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

def is_answer_grounded(answer: str, sources: list) -> bool:
    # Check if answer or its keywords appear in any retrieved context
    answer_lower = answer.lower()
    for doc in sources:
        if answer_lower in doc.page_content.lower():
            return True
    return False

def avg_relevance_score(query: str, sources: list) -> float:
    query_emb = embedder.encode(query, convert_to_tensor=True)
    scores = []
    for doc in sources:
        doc_emb = embedder.encode(doc.page_content, convert_to_tensor=True)
        sim = util.pytorch_cos_sim(query_emb, doc_emb).item()
        scores.append(sim)
    if not scores:
        return 0.0
    return sum(scores) / len(scores)

def run_evaluation(samples):
    results = []
    for sample in samples:
        query = sample["query"]
        expected = sample["expected_answer"]

        answer, sources = llm_evalution(query, vectordb)

        cos_sim = cosine_similarity_score(answer, expected)
        grounded = is_answer_grounded(answer, sources)
        relevance = avg_relevance_score(query, sources)

        results.append({
            "query": query,
            "expected_answer": expected,
            "generated_answer": answer,
            "cosine_similarity": cos_sim,
            "grounded": grounded,
            "relevance": relevance,
            "source_documents": " | ".join([doc.page_content[:100].replace('\n',' ') for doc in sources])  # snippet for reference
        })
    return results

def save_results_to_csv(results, filename="llm_evaluation_report.csv"):
    keys = [
        "query", "expected_answer", "generated_answer",
        "cosine_similarity", "grounded", "relevance", "source_documents"
    ]
    with open(filename, mode='w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        for row in results:
            # Convert boolean to Yes/No string for CSV
            row['grounded'] = "Yes" if row['grounded'] else "No"
            # Round float fields for better readability
            row['cosine_similarity'] = f"{row['cosine_similarity']:.4f}"
            row['relevance'] = f"{row['relevance']:.4f}"
            writer.writerow(row)
    print(f"Results saved to {filename}")

if __name__ == "__main__":
    results = run_evaluation(samples)
    save_results_to_csv(results)
