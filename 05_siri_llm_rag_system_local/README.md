# Personal AI Assistant RAG System for Searching My Documents

## Project Question

**Can a local RAG assistant answer questions from private documents without sending data to paid cloud APIs?**

This project converts a cloud/API-dependent LLM app into a **local-first RAG system**. It uses:

- **Ollama** for a local LLM
- **sentence-transformers** for free local embeddings
- **FAISS** for a local vector database
- **Streamlit** for the web app
- **PDF/text ingestion**
- **document upload**
- **citations and source chunks**
- **retrieval evaluation page**
- **sample documents folder**

No Hugging Face token, OpenAI key, or subscription API is required.

---

## Why this is a strong portfolio project

This project shows practical applied AI skills:

- local/private AI architecture
- RAG pipeline design
- document ingestion
- vector database search
- source-grounded LLM answers
- evaluation of retrieval quality
- Streamlit app development
- privacy-aware AI system design

Portfolio framing:

> Built a local RAG assistant that searches private documents and answers questions with citations using Ollama, sentence-transformers, FAISS, and Streamlit, avoiding paid cloud APIs and preserving document privacy.

---

## Project Structure

```text
05_siri_llm_rag_system/
├── app/
│   └── streamlit_app.py
├── rag/
│   ├── document_loader.py
│   ├── vector_store.py
│   └── ollama_client.py
├── data/
│   ├── sample_documents/
│   └── uploaded_documents/
├── evaluation/
│   ├── evaluate_retrieval.py
│   └── sample_eval_questions.csv
├── notebooks/
│   └── Local_RAG_Assistant_Demo.ipynb
├── vector_store/
├── outputs/
│   └── screenshots/
├── build_index.py
├── query_rag.py
├── requirements.txt
└── README.md
```

---

## Step 1: Install Ollama

Download and install Ollama:

```text
https://ollama.com
```

Pull a local model:

```bash
ollama pull llama3.2
```

You can also use another local model:

```bash
ollama pull mistral
ollama pull phi3
```

Start Ollama:

```bash
ollama run llama3.2
```

Keep Ollama available while running the app.

---

## Step 2: Create Python environment

From the project folder:

```bash
cd 05_siri_llm_rag_system
```

### Mac / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Step 3: Build vector database from sample documents

```bash
python build_index.py --input-dir data/sample_documents --index-dir vector_store
```

Expected output:

```text
Loaded documents: 3
Created chunks: ...
Saved vector store to: ...
```

---

## Step 4: Ask a question from command line

```bash
python query_rag.py --question "What is the project question?"
```

More examples:

```bash
python query_rag.py --question "Why is this RAG system private?"
python query_rag.py --question "What tools does this system use?"
python query_rag.py --question "How can retrieval quality be evaluated?"
```

The answer includes source filenames and chunk numbers.

---

## Step 5: Run the Streamlit app

```bash
streamlit run app/streamlit_app.py
```

The app includes:

### 1. Upload & Index Documents

Upload `.txt` or `.pdf` files.  
Click **Build / Rebuild FAISS Index**.

### 2. Ask Questions

Ask a question.  
The app retrieves relevant document chunks and uses Ollama to answer with citations.

### 3. Retrieval Evaluation

Test whether the correct source appears in the top-k retrieved chunks.

---

## Step 6: Use your own private documents

Put files here:

```text
data/uploaded_documents/
```

Supported file types:

- `.txt`
- `.pdf`

Build the index:

```bash
python build_index.py --input-dir data/uploaded_documents --index-dir vector_store
```

Run the app:

```bash
streamlit run app/streamlit_app.py
```

---

## Step 7: Evaluate retrieval quality

Use the sample evaluation file:

```text
evaluation/sample_eval_questions.csv
```

Run:

```bash
python evaluation/evaluate_retrieval.py --eval-file evaluation/sample_eval_questions.csv --index-dir vector_store --top-k 5
```

Output file:

```text
evaluation/retrieval_evaluation_results.csv
```

---

## How the system works

### 1. Document ingestion

`rag/document_loader.py` loads local `.txt` and `.pdf` documents.

### 2. Chunking

Documents are split into overlapping chunks.

### 3. Embeddings

`sentence-transformers` converts chunks into vector embeddings using:

```text
all-MiniLM-L6-v2
```

### 4. Vector search

FAISS stores embeddings locally and retrieves relevant chunks.

### 5. Local LLM answering

Ollama receives only the retrieved context and the user question.  
The answer is generated locally and includes source citations.

---

## Why no Hugging Face token is needed

This project does not call Hugging Face Inference API.

Embeddings are generated locally using `sentence-transformers`.  
LLM responses are generated locally using Ollama.  
The vector database is stored locally with FAISS.

---

## Recommended screenshots for GitHub

Add screenshots to:

```text
outputs/screenshots/
```

Recommended screenshots:

1. Streamlit upload/index page
2. Question-answer page with citations
3. Retrieved sources table
4. Retrieval evaluation page
5. Terminal output showing successful local run

Then add them to this README:

```markdown
![App Screenshot](outputs/screenshots/app_demo.png)
```

---

## Limitations

This is a portfolio-level RAG system, not a production security system.

Limitations:

- local model quality depends on the Ollama model selected
- PDF extraction quality can vary
- retrieval quality depends on chunking and embedding model
- no user authentication is included
- not optimized for very large enterprise document collections

---

## Future improvements

- add DOCX support
- add chat history
- add metadata filters
- add document deletion/reset button
- add hybrid keyword + vector search
- add reranking
- add source highlighting
- add exportable Q&A logs
- add Docker deployment

---

## Resume bullet

Built a local-first RAG assistant for private document search using Ollama, sentence-transformers, FAISS, and Streamlit, enabling users to upload PDFs/text files, build a local vector database, ask source-grounded questions, and evaluate retrieval quality without paid cloud APIs.
