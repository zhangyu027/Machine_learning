# Enterprise AI Knowledge Agent Platform

## Project Question

**Can a private enterprise AI agent platform answer questions across documents, SQL tables, and image notes with citations, confidence scoring, and hallucination checks?**

This package upgrades a local RAG chatbot into an **Enterprise AI Knowledge Agent Platform**.

It is tailored to Yu Zhang's portfolio background in healthcare AI, education/public-sector analytics, data governance, RAG systems, data engineering, SQL analytics, and enterprise AI.

---

## What This Project Includes

- agent orchestration
- multi-agent workflow
- document RAG agent
- SQL analytics agent
- image-note agent
- local/private deployment
- Ollama support
- FAISS vector search
- local embeddings
- PDF/TXT ingestion
- SQL over local CSV data
- citation confidence scoring
- hallucination risk detection
- evaluation benchmark
- Streamlit app
- Jupyter notebook

---

## Architecture

```text
User question
     ↓
Agent Router
     ↓
Document RAG Agent / SQL Agent / Image Notes Agent
     ↓
Evidence Aggregator
     ↓
Local Ollama LLM
     ↓
Citation Confidence Scoring
     ↓
Hallucination Risk Check
     ↓
Final Answer + Sources + Risk Report
```

---

## Step-by-Step Run Instructions

### Step 1: Create environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Build vector store and SQL database

```bash
python build_index.py
```

This creates:

```text
vector_store/index.faiss
vector_store/metadata.json
data/sql/enterprise_agent.db
```

### Step 4: Run the agent from terminal

```bash
python run_agent.py
```

### Step 5: Run benchmark evaluation

```bash
python evaluation/evaluate_agent.py
```

Outputs:

```text
outputs/tables/agent_evaluation_results.csv
outputs/tables/agent_evaluation_summary.csv
```

### Step 6: Open notebook

```bash
jupyter notebook notebooks/Enterprise_AI_Knowledge_Agent_Demo.ipynb
```

### Step 7: Launch Streamlit app

```bash
streamlit run app/streamlit_app.py
```

If Streamlit has a watcher warning:

```bash
streamlit run app/streamlit_app.py --server.fileWatcherType none
```

---

## Optional Ollama Setup

Install Ollama:

```text
https://ollama.com
```

Pull a model:

```bash
ollama pull llama3.2
```

Then in the Streamlit app, check:

```text
Use Ollama
```

Without Ollama, the platform still demonstrates routing, retrieval, SQL, confidence scoring, hallucination checks, and evaluation.

---

## Example Questions

```text
What should healthcare AI governance include?
```

```text
Why is de-identification important for public-sector analytics?
```

```text
Which portfolio projects have the highest priority and why?
```

```text
What does the platform architecture diagram show?
```

---

## Why This Is More Than a Chatbot

A chatbot usually produces a direct text answer.

This platform:

1. routes questions,
2. chooses tools,
3. retrieves evidence,
4. queries structured data,
5. cites sources,
6. scores confidence,
7. checks hallucination risk,
8. stores evaluation outputs.

That is closer to enterprise AI platform work.

---

## Resume Bullet

Built a local/private Enterprise AI Knowledge Agent Platform with document RAG, SQL analytics, image-note retrieval, tool orchestration, FAISS vector search, Ollama integration, citation confidence scoring, hallucination risk checks, and benchmark evaluation for healthcare, public-sector, and enterprise data use cases.
