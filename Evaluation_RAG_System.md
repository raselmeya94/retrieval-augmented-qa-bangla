
## 📊 Evaluation Report: Bengali Literature QA System (অপরিচিতা)

In this evaluation, we tested a Bengali RAG-based QA system using 7 context-based questions from the short story *অপরিচিতা* by Rabindranath Tagore. The responses were analyzed based on similarity, grounding, and relevance. Below are the findings:

---

### 📝 QA Evaluation Table

| প্রশ্ন                                                           | উত্তর                      | Cosine Similarity | Grounded | Relevance | Source Document (সংক্ষিপ্ত)                   |
| ---------------------------------------------------------------- | -------------------------- | ----------------- | -------- | --------- | --------------------------------------------- |
| অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?                          | শুম্ভুনাথ (ঘ)              | 0.2435            | Yes      | 0.5958    | অনুপমর ভাষায় সুপুরুষ বলতে ...                 |
| কাকে অনুপমের ভাগ্য দেবতা বলা হয়েছে?                             | মামা                       | 0.9556            | Yes      | 0.6180    | অনুপমর ভাগ্য দেবতা বলতে ...                   |
| বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?                         | ১৫ বছর                     | 1.0000            | Yes      | 0.5058    | বিয়ের সময় কল্যাণীর বয়স ছিল ...             |
| 'অপরিচিতা' গল্পে গল্প বলায় পটু কে?                              | হরিশ (ঘ)                   | 0.3200            | Yes      | 0.6325    | অপরিচিতা গল্পে পটু বলতে ...                   |
| অনুপম কল্যাণীর বিয়েতে তার কল্পনায় কোন রঙের শাড়ি পরতে দেখেছিল? | লাল                        | 1.0000            | Yes      | 0.6592    | বিয়ের সময় কল্যাণী লাল শাড়ি পরেছিল ...      |
| 'অপরিচিতা' গল্পে রেলকর্মচারী কতটি টিকিট বেঞ্চে ঝুলিয়েছিল?       | দুইটি (খ)                  | 0.8635            | ❌ No     | 0.6429    | রেলকর্মচারী বেঞ্চে দুইটি টিকিট ঝুলিয়েছিল ... |
| কল্যাণী কেন বিয়ে না করার সিদ্ধান্ত নিয়েছিল?                    | অপমান ও আত্মমর্যাদার কারণে | 0.6737            | Yes      | 0.5215    | কল্যাণী বিয়ে করতে চায়নি কারণ ...            |

---

### 📌 Evaluation Summary

| Criteria                           | Observation                                 |
| ---------------------------------- | ------------------------------------------- |
| **Total Questions Evaluated**      | 7                                           |
| **Perfect Similarity (1.0)**       | 2 (e.g., "১৫ বছর", "লাল")                   |
| **High Similarity (> 0.85)**       | 1 (e.g., "মামা" → 0.9556)                   |
| **Moderate Similarity (0.6–0.85)** | 2 (Reasonable match)                        |
| **Low Similarity (< 0.6)**         | 2 (Needs improvement, e.g., 0.2435, 0.3200) |
| **Grounded Answers**               | 6 out of 7 (✅ Found in source)              |
| **Relevant Answers**               | 6 out of 7 (✅ Contextually aligned)         |

---

### 🔍 Insights

* ✅ **\~86% answers were relevant and grounded**, showing the model understands context well.
* 🧠 Even answers with low similarity still matched the **intended meaning**.
* ⚠️ Only **one answer** was **not grounded** — possible hallucination or misalignment.
* 📘 The system performs well for **Bengali Documents-Based QAs**, suitable for RAG applications.

---

