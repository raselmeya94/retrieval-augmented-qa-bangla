# 🔌 API Access (Bonus)

Our Bengali Literature QA system provides a simple RESTful API to query answers from processed PDFs using a RAG-based architecture.

---

## 📮 Endpoint: `/ask`

* **Method:** `POST`
* **Content-Type:** `application/json`
* **Description:** Accepts a natural language question (Bangla/English) and returns the best answer retrieved using vector similarity and LLM generation.

---

### ✅ Sample Request

```bash
POST /ask HTTP/1.1
Host: localhost:<port>
Content-Type: application/json

{
  "query": "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?"
}
```

---

### 🧾 Sample Response

```json
{
  "query": "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?",
  "answer": "১৫ বছর"
}
```

---

## 🔍 Interactive API Docs

You can explore and test the API using the built-in Swagger UI at:

```
http://localhost:<port>/docs
```


---

## 📤 `curl` Example

```bash
curl -X POST http://localhost:<port>/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?"}'
```

> ✅ Replace `<port>` with your actual port number (e.g., `8000`).

---

### 💡 Expected Output

```json
{
  "query": "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?",
  "answer": "১৫ বছর"
}
```
