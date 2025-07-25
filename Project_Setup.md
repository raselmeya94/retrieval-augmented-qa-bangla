# 🚀 Project Setup Guide

---

## 1. Clone Git Repository:

```bash
git clone https://github.com/raselmeya94/retrieval-augmented-qa-bangla.git
cd retrieval-augmented-qa-bangla
```
After cloning the repo, you'll see the following directory structure.

### 📁 Project Structure

```
retrieval-augmented-qa-bangla
├── bn_rag_app/
│   ├── main.py                # FastAPI application entrypoint
│   ├── load_vectordb.py       # Vector store loading utilities
│   └── rag_pipeline.py        # RAG system pipeline logic
├── data/
│   └── HSC26_Bangla.pdf       # Source PDF document(s)
├── llm_evaluation/
│   └── evaluation.py          # Model evaluation scripts
├── pdf_to_vectordb/
│   ├── embedder.py            # Embedding model logic
│   ├── mistral_ocr.py         # OCR processing utilities
│   ├── text_preprocessing.py  # Text preprocessing scripts
│   ├── vectordb.py            # Vector DB creation and management
│   └── advanced_preprocessing.py  # Optional advanced text preprocessing
├── vector_store/              # Generated vector store files
├── .env                      # Environment variables
├── requirements.txt           # Python dependencies list
├── API_Documentation.md       # API usage documentation
├── Evaluation_RAG_System.md   # Evaluation report
├── Project_Setup.md           # Project setup instructions
└── README.md                  # Project overview and instructions
```
---

### ✅ Configure Environment Variables

A `.env` file is already present in the root directory of **this project**. You only need to update a few values like the **`Mistral API key`**, **`MongoDB URI/Port`**, and other configuration parameters.

#### 📝 Steps to Update:

1. Open the existing `.env` file located at the root of this project.
2. Replace the placeholder values with the actual configuration details.

Here is an example of the updated `.env` file:

```env
MISTRAL_API_KEY=your_actual_mistral_api_key
TOP_K=15
SHORT_TERM_MEMORY_RETRIEVE=2
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=rag_short_memory
MONGODB_COLLECTION=qa_logs
```

#### 📌 Explanation of Environment Variables:

* **`MISTRAL_API_KEY`**: API key for using Mistral's services such as embeddings or OCR.
* **`TOP_K`**: Number of top relevant results to fetch from the vector store.
* **`SHORT_TERM_MEMORY_RETRIEVE`**: Number of recent queries to include in the conversational context.
* **`MONGODB_URI`**: MongoDB connection string with host and port.
* **`MONGODB_DB`**: Database name for storing application data.
* **`MONGODB_COLLECTION`**: Collection where question-answer logs will be stored.

---

Once the `.env` file is correctly updated, **this project** will be ready to run with the appropriate settings. ✅

## 📦 Requirements

* **Python**: version **3.10** (recommended)
* **MongoDB**: Local or remote instance running
* **Mistral API**: Valid API key from [Mistral AI](https://docs.mistral.ai)

---

## 2. Create Virtual Environment (venv)

```bash
# Create virtual environment named 'venv'
python3.10 -m venv venv

# Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create Vector Store (VectorDB)

Run the vector store creation script to generate embeddings and build the vector database:

```bash
python pdf_to_vectordb/create_vectordb.py
```

> After completion, you will see a `vector_store` directory containing vector embedding data, and a `chunks.txt` file with the processed PDF chunks for observation. If Chunks.txt is present, it means VectorDB was created.
**Note:** This step is for a single time.
---

## 5. Run FastAPI Application

Navigate to the `bn_rag_app` directory:

```bash
cd bn_rag_app
```

Start the FastAPI server with:

```bash
uvicorn main:app --reload
```

By default, the server runs at:
[http://localhost:8000](http://localhost:8000)

* API documentation is available at:
  [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 6. API Testing

Follow the instructions in [API Documentation](API_Documentation.md) to test and interact with the API endpoints.


