# 🚀 Project Setup Guide

---

## CLone Git Repository:

```bash
git clone https://github.com/raselmeya94/retrieval-augmented-qa-bangla.git
cd retrieval-augmented-qa-bangla
```
After cloning the repo, you'll see the following directory structure.

## 📁 Project Structure

```
retrieval-augmented-qa-bangla
├── bn_rag_app/
│   ├── main.py                # FastAPI application entrypoint
│   ├── load_vectordb.py       # Vector store loading utilities
│   ├── rag_pipeline.py        # RAG system pipeline logic
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
### Configure Environment Variables:

You'll need to configure environment variables for things like the `Mistral API key`, `MongoDB connection`, and some system settings.

1. Open the `.env` file you created in the root directory of your project.

2. Update the values with your actual information. Here’s what the updated `.env` file might look like:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
TOP_K=15
SHORT_TERM_MEMORY_RETRIEVE=2
MONGODB_URI=mongodb://localhost:"<Port Number>"
MONGODB_DB=rag_short_memory
MONGODB_COLLECTION=qa_logs
```

#### Explanation of the Environment Variables:

* **MISTRAL\_API\_KEY**: Your Mistral API key for OCR/embedding.
* **TOP\_K**: The number of top results to retrieve from the model.
* **SHORT\_TERM\_MEMORY\_RETRIEVE**: Number of previous queries to retain for context.
* **MONGODB\_URI**: URI for your MongoDB database.
* **MONGODB\_DB**: The database name for storing data.
* **MONGODB\_COLLECTION**: Collection name for storing QA logs.

Once this is configured, the system will be ready for use.

---

## 📦 Requirements

* **Python**: version **3.10** (recommended)
* **MongoDB**: Local or remote instance running
* **Mistral API**: Valid API key from [Mistral](https://docs.mistral.ai)

---

### 2. Create Virtual Environment (venv)

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

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Create Vector Store (VectorDB)

Run the vector store creation script to generate embeddings and build the vector database:

```bash
python pdf_to_vectordb/create_vectordb.py
```

> After completion, you will see a `vector_store` directory containing vector embedding data, and a `chunks.txt` file with the processed PDF chunks for observation. IF Chunks.txt are present text that means vectordb created..
**Note:** This step for single times.
---

### 5. Run FastAPI Application

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

### 6. API Testing

Follow the instructions in [API Documentation](API_Documentation.md) to test and interact with the API endpoints.


