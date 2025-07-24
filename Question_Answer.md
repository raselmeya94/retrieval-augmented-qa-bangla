# Assessment Questions Answered:

## 1. What method or library did you use to extract the text, and why? Did you face any formatting challenges?

I used **Mistral OCR** for extracting Bangla text, as it outperformed alternatives like Tesseract and EasyOCR, especially for documents with complex fonts and layouts.

### Challenges

* **PDF Extraction Issues**: Libraries like `pdfplumber`, `PyMuPDF`, and `ocrmypdf` struggled with rendering clean Bangla text due to font issues.
* **Image-Based OCR**: Attempts to convert PDF to images and then extract text didn’t yield good results.

### Solution: Mistral OCR

Mistral OCR gave better results, handling complex fonts and layout challenges. However, formatting issues like line breaks, fused characters, and inconsistent spacing were resolved through post-processing.

#### ❌ PDF Text Extraction Example:

```text
আি আমাি ব্ স সাতাি মাত্র । এ িীব্নটা না দদকঘিযি র্হসাকব্ ব়্ে , না গুকনি র্হসাকব্...
```

#### ✅ Mistral OCR Output:

```text
## মূল গল্প

আজ আমার বয়স সাতাশ মাত্র। এ জীবনটা না দৈর্ঘ্যের হিসাবে বড়, না গুনের হিসাবে...
```

---

### 2. What chunking strategy did you choose (e.g., paragraph-based, sentence-based, character limit)? Why do you think it works well for semantic retrieval?

I employed **Recursive Character-Based Chunking** via LangChain’s `RecursiveCharacterTextSplitter`, with a chunk size of around 4096 tokens and slight overlap. This method ensures that semantically complete sections (like paragraphs or sentences) are grouped logically, which improves retrieval accuracy and prevents context loss during similarity search.

---

### 3. What embedding model did you use? Why did you choose it? How does it capture the meaning of the text?

We used the `all-MiniLM-L6-v2` model from SentenceTransformers. It is compact, fast, and performs well on multilingual data, including Bangla. This transformer-based model encodes sentences into dense vector representations that capture the semantic meaning rather than just surface-level tokens, making it ideal for similarity-based retrieval tasks.

---

### 4. How are you comparing the query with your stored chunks? Why did you choose this similarity method and storage setup?

The system compares the query’s embedding with pre-computed chunk embeddings using **cosine similarity** via **FAISS**. FAISS is optimized for fast vector similarity search and scales well with large document collections. Cosine similarity effectively captures directional similarity in the embedding space, which aligns well with semantic comparisons.

---

### 5. How do you ensure that the question and the document chunks are compared meaningfully? What would happen if the query is vague or missing context?

To ensure meaningful comparisons, the system uses a top-k retrieval strategy that fetches the most semantically relevant chunks for each query. When queries are vague or ambiguous, retrieval may return loosely related content. In future improvements, we plan to implement query rephrasing or clarification prompts to handle such cases more gracefully.

---

### 6. Do the results seem relevant? If not, what might improve them (e.g., better chunking, better embedding model, larger document)?


Yes, the results are generally relevant and contextually accurate. However, there’s always room for improvement. I’ve experimented with **Gemini embedding**, but it requires an API key, which wasn’t necessary when I initially used **Mistral**. So, I opted for **Hugging Face embeddings** instead, as they provided good results without the need for an API key.

For chunking, I tested different chunk sizes and iterated several times to find the optimal value, which helped improve the context retrieval accuracy.

To further enhance performance, I plan to:

* Integrate a more robust OCR pipeline,
* Use Bangla-specific embedding models,
* Refine chunking based on document structure (headings, sections), and
* Expand the document set for broader context coverage.

For more details, you may refer to my evaluation section for a deeper understanding of my RAG system’s performance.
