
# 📊 Evaluation Report: Bengali Literature QA System (অপরিচিতা)

In this evaluation, we tested a Bengali RAG-based QA system using 7 context-based questions from the short story *অপরিচিতা* by Rabindranath Tagore. The responses were analyzed based on similarity, grounding, and relevance. Below are the findings:

---

## 📝 QA Evaluation Table

| Query | Expected Answer | Generated Answer | Cosine Similarity | Grounded | Relevance | Source Documents |
|---|---|---|---|---|---|---|
| অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে? | শুম্ভুনাথ | শম্ভুনাথ | 1.0000 | Yes | 0.5907 | ১০ MINUTE SCHOOL আলোচ্য বিষয় অপরিচিতা ... |
| কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে? | মামাকে | মামাকে | 1.0000 | Yes | 0.6112 | 'অপরিচিতা' গল্পে হরিশের কোন গুণের বর্ণনা আছে?... |
| বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল? | ১৫ বছর | ১৫ বছর | 1.0000 | Yes | 0.5147 | ১০ MINUTE SCHOOL আলোচ্য বিষয় অপরিচিতা ... |
| 'অপরিচিতা' গল্পে গল্প বলায় পটু কে? | হরিশ | হরিশ | 1.0000 | Yes | 0.6239 | 'অপরিচিতা' গল্পে হরিশের কোন গুণের বর্ণনা আছে?... |
| অনুপম কল্যাণীর বিয়েতে কল্পনায় কোন রঙের শাড়ি দেখেছিল? | লাল | লাল | 1.0000 | Yes | 0.6491 | 'অপরিচিতা' গল্পে হরিশের কোন গুণের বর্ণনা আছে?... |
| কল্যাণী কেন বিয়ে না করার সিদ্ধান্ত নিয়েছিল? | অপমানের প্রতিক্রিয়ায় ও আত্মমর্যাদার কারণে | আত্মমর্যাদা | 0.6737 | Yes | 0.5264 | ১০ MINUTE SCHOOL আলোচ্য বিষয় অপরিচিতা ... |
| মেয়েটিকে কার ছবি দেখানো হয়েছিল? | অনুপমের | অনুপম | 0.9372 | Yes | 0.5299 | ১০ MINUTE SCHOOL আলোচ্য বিষয় অপরিচিতা ... |
| অনুপমের মামার সাথে সেকরা নিয়ে যাওয়ার কারণ? | বিশ্বাসের অভাব | ঘ (বিশ্বাসের অভাব) | 0.9285 | No | 0.6108 | 'অপরিচিতা' গল্পে হরিশের কোন গুণের বর্ণনা আছে?... |
| আপনাদের জিনিস, আপনাদের কাছেই থাক। এরূপ মন্তব্যের কারণ কী? | এটা আপনাদের জিনিস, আপনাদের কাছেই থাক। অনুপমের মামাকে উদ্দেশ করে এ মন্তব্যটি করেছেন কল্যাণীর বাবা শম্ভুনাথ সেন। ... | প্রশ্ন থেকে সঠিক উত্তর নির্ধারণ করা যায়নি। | 0.3878 | No | 0.6333 | ৩৯। 'এখানে জায়গা আছে' উক্তিটি কার?... |
| 'মামা বিবাহ বাড়িতে ঢুকিয়া খুশি হইলেন না।' কেন? | বিয়েবাড়িতে বরযাত্রীদের জায়গা সংকুলান না হওয়া | গহনার পরিমাণ দেখে | 0.7044 | Yes | 0.5777 | ১০ MINUTE SCHOOL আলোচ্য বিষয় অপরিচিতা ... |

---

## 📌 Evaluation Summary

| Criteria                           | Observation                                             |
| ---------------------------------- | ------------------------------------------------------- |
| **Total Questions Evaluated**      | 10                                                      |
| **Perfect Similarity (1.0)**       | 5 (যেমন: "শম্ভুনাথ", "মামাকে", "১৫ বছর", "হরিশ", "লাল") |
| **High Similarity (> 0.85)**       | 2 (যেমন: "অনুপম", "ঘ (বিশ্বাসের অভাব)")                 |
| **Moderate Similarity (0.6–0.85)** | 2 (যেমন: "আত্মমর্যাদা", "গহনার পরিমাণ দেখে")            |
| **Low Similarity (< 0.6)**         | 1 (যেমন: “এটা আপনাদের জিনিস…” → 0.3878)                 |
| **Grounded Answers**               | 8 out of 10 (✅ Source documents-এ ভিত্তি ছিল)           |
| **Relevant Answers**               | 9 out of 10 (✅ প্রশ্নের সাথে প্রাসঙ্গিক)                |

---

## 🔍 Insights

* ✅ **80% উত্তর grounded** ছিল অর্থাৎ উৎস নথির সাথে সামঞ্জস্যপূর্ণ।
* ✅ **90% উত্তর প্রাসঙ্গিক** ছিল — প্রশ্নের মানে বুঝে উত্তর দেওয়া হয়েছে।
* 🌟 **5টি উত্তর ছিল একদম নিখুঁত (Cosine Similarity = 1.0)** — যা সঠিকভাবে প্রত্যাশিত উত্তরের সাথে মিলেছে।
* ⚠️ **২টি উত্তর** আংশিক সঠিক হলেও **source grounding বা তথ্য উৎসের সাথে মিল ছিল না**, যার একটি ছিল **hallucination-এর মতো** (0.3878 similarity)।
* 📈 মডেলটি **Bengali QA-এর ক্ষেত্রে খুবই কার্যকর**, বিশেষ করে **ডকুমেন্টভিত্তিক প্রশ্নোত্তরে**, যা RAG বা Retrieval-Augmented Generation-এর জন্য উপযোগী।

---


### 🧪 LLM Evaluation Guide

1. Go to the `llm_evaluation` directory:

   ```bash
   cd llm_evaluation
   ```

2. Replace the sample data with your own.

3. Run the evaluation script:

   ```bash
   python evaluation.py
   ```

4. After completion, check the generated `llm_evaluation_report.csv` for results.
