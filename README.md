''AI Clinical Decision Support Lite''

An evidence-grounded Clinical Decision Support System built using Retrieval-Augmented Generation (RAG) to provide reliable medical answers based on trusted sources.

The system retrieves relevant evidence from WHO Hypertension Guidelines and MedlinePlus, then uses Google Gemini to generate structured, grounded responses with citations and confidence levels.

---

Key Features

-  Clinical Decision Support — Answers medical questions using retrieved evidence.
-  Trusted Sources — WHO Guidelines + MedlinePlus.
-  RAG Pipeline — Retrieval with ChromaDB followed by grounded generation with Gemini.
-  Multilingual Support — Supports 11 languages including Arabic, English, French, Spanish, German, Italian, Turkish, Portuguese, Hindi, Chinese, and Japanese.
-  Smart Autocomplete — Suggests relevant medical questions while typing.
-  Grounding & Safe Refusal — Answers are based on retrieved evidence and the system refuses when evidence is insufficient.
-  Citations & Supporting Evidence — Displays evidence and source links for generated answers.
-  Dark / Light Mode — Professional medical dashboard with theme switching.
-  Analytics Dashboard — Question history, confidence statistics, source usage, and language usage.

---

Architecture

Medical Sources
     ↓
Document Ingestion
     ↓
Chunking + Metadata
     ↓
Local Embeddings (FastEmbed)
     ↓
ChromaDB
     ↓
Retrieval
     ↓
Context / Evidence
     ↓
Google Gemini
     ↓
Grounded Structured Response
     ↓
Streamlit Dashboard

---

Project Structure

File / Folder| Purpose
"app.py"| Streamlit application and user interface
"config.py"| Central project configuration
"ingest.py"| Document loading, chunking, embeddings, and indexing
"query.py"| Retrieval from ChromaDB
"generate.py"| Grounded response generation using Gemini
"pipeline.py"| End-to-end RAG pipeline
"medlineplus_api.py"| MedlinePlus API integration
"api_data.py"| Processing external API data
"suggestions.py"| Smart question autocomplete
"schema/"| Structured response schema
"data/"| Medical source documents
"eval/"| Evaluation and benchmark datasets
"notebooks/"| Development and evaluation notebooks
"requirements.txt"| Python dependencies

---

Technology Stack

- Python
- Streamlit — Frontend & dashboard
- ChromaDB — Vector database
- FastEmbed — Local embeddings
- LangChain — Document processing
- Google Gemini API — Grounded response generation
- MedlinePlus API — Additional medical evidence

---

Setup

1. Create a virtual environment

python -m venv venv

2. Activate it

Windows:

venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Configure environment variables

Create a ".env" file based on ".env.example" and add your Gemini API key:

GEMINI_API_KEY=YOUR_GEMINI_API_KEY

«Never commit ".env" or expose your API key.»

5. Build the vector database

python ingest.py

6. Run the application

streamlit run app.py

---

Safety & Grounding

The system follows a grounded generation approach:

1. Retrieve relevant medical evidence from trusted sources.
2. Provide the retrieved context to Gemini.
3. Generate the response only from the available evidence.
4. Provide citations and confidence information.
5. Refuse to provide an answer when sufficient evidence is unavailable.

«Disclaimer: This system is an AI-assisted clinical information tool and is not a substitute for professional medical advice, diagnosis, or treatment.»

---

Project Goal

The goal of AI Clinical Decision Support Lite is to make medical information retrieval faster, more transparent, multilingual, and evidence-grounded, while reducing the risk of unsupported AI-generated medical information.