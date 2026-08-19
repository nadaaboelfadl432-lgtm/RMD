# AI Clinical Decision Support Lite — Grounded RAG System

A beginner-friendly **Retrieval-Augmented Generation (RAG)** system for the **AI Clinical Decision Support Lite Hackathon**.

The system retrieves medical evidence from trusted sources, stores the information in a vector database, and uses Google Gemini to generate grounded clinical answers with source citations.

The project combines:

- WHO hypertension guideline PDF documents
- MedlinePlus API data
- Local embeddings using FastEmbed
- ChromaDB vector database
- Google Gemini for grounded generation
- Citation validation
- Safe refusal for insufficient evidence
- Streamlit web interface

---

## Project Overview

The system is designed to answer clinical questions using only the evidence retrieved from the indexed medical sources.

Instead of allowing the language model to answer from its general knowledge, the system follows this pipeline:

```text
Medical Sources
      │
      ├── WHO Hypertension Guideline PDF
      │
      └── MedlinePlus API
              │
              ▼
        Data Ingestion
              │
              ▼
           Chunking
              │
              ▼
          Embeddings
              │
              ▼
           ChromaDB
              │
              ▼
          Retrieval
              │
              ▼
     Retrieved Evidence
              │
              ▼
       Grounded Prompt
              │
              ▼
        Google Gemini
              │
              ▼
     Citation Validation
              │
              ▼
     Structured Response
              │
              ▼
        Streamlit UI