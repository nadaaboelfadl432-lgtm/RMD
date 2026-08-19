"""
Grounded Generation Module (Gemini)
-----------------------------------
Uses Google's official GenAI SDK (google-genai) with structured output
to generate grounded clinical answers based strictly on retrieved context.

Structured Output Schema:
{
  "recommendation": "...",
  "evidence": "...",
  "citations": [{"document": "...", "section": "...", "page": 1}],
  "confidence": "high | medium | low | insufficient"
}
"""
import json
import os
from pathlib import Path
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

import config

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None

try:
    import jsonschema
except ImportError:
    jsonschema = None


# --- Pydantic Schema for Gemini Structured Output ---

class CitationModel(BaseModel):
    document: str = Field(
        description="Exact document name from metadata"
    )

    section: str = Field(
        default="N/A",
        description="Exact section name from metadata, or N/A if unavailable"
    )

    page: Optional[int] = Field(
        default=None,
        description="PDF page number. Must be null for MedlinePlus sources."
    )

    url: Optional[str] = Field(
        default=None,
        description="Exact source_url for MedlinePlus sources. Must be null for PDF sources."
    )

class GroundedResponseModel(BaseModel):
    recommendation: str = Field(description="Direct clinical answer or refusal message")
    evidence: str = Field(default="", description="Exact supporting text excerpt, or empty string if insufficient")
    citations: List[CitationModel] = Field(default_factory=list, description="List of source citations, empty if insufficient")
    confidence: Literal["high", "medium", "low", "insufficient"] = Field(description="Confidence level")


# Path to project JSON schema for validation
SCHEMA_PATH = config.BASE_DIR / "schema" / "response_schema.json"


def load_response_schema() -> Optional[dict]:
    """Loads the JSON schema from schema/response_schema.json if available."""
    if SCHEMA_PATH.exists():
        try:
            with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None


def format_context_for_prompt(retrieved_results: list) -> str:
    """Formats retrieved chunks with metadata for inclusion in the prompt."""
    context_blocks = []
    for doc, score in retrieved_results:
        meta = doc.metadata
        doc_name = meta.get("document_name", "Unknown Document")
        page = meta.get("page_number", 1)
        section = meta.get("section", "N/A")
        chunk_id = meta.get("chunk_id", "N/A")

        header = f"[Source Document='{doc_name}', Page={page}, Section='{section}', ChunkID='{chunk_id}']"
        context_blocks.append(f"{header}\n{doc.page_content.strip()}")

    return "\n\n".join(context_blocks)


def create_refusal_response(reason: str) -> dict:
    """Creates a standard refusal dictionary adhering to response_schema.json."""
    return {
        "recommendation": reason,
        "evidence": "",
        "citations": [],
        "confidence": "insufficient"
    }


def validate_citations(response: dict, retrieved_results: list) -> bool:
    """Validate that every citation comes from retrieved documents."""

    if response.get("confidence") == "insufficient":
        return True

    citations = response.get("citations", [])

    if not citations:
        return True

    valid_documents = set()

    for doc, _ in retrieved_results:
        meta = doc.metadata

        document_name = meta.get("document_name")

        if document_name:
            valid_documents.add(str(document_name))

    for citation in citations:

        citation_document = str(
            citation.get("document", "")
        )

        if citation_document not in valid_documents:

            print(
                f"\n[Citation Validation Error] "
                f"Unknown document: '{citation_document}'"
            )

            return False

    return True


def generate_grounded_answer(question: str, retrieved_results: list) -> dict:
    """Generates a grounded answer using Gemini constrained by structured output
    and validates both the schema and citations before returning.
    """
    # 1. Validate API Key
    api_key = config.GEMINI_API_KEY
    if not api_key:
        print("\n[Notice] GEMINI_API_KEY is not set.")
        print("To generate answers with Gemini:")
        print("  1. Add your key to .env: GEMINI_API_KEY=your_key_here")
        print("  2. Re-run: python pipeline.py \"your question\"\n")
        return create_refusal_response("GEMINI_API_KEY is missing. Please set GEMINI_API_KEY in your .env file to enable generation.")

    # 2. Check SDK installation
    if genai is None:
        print("\n[Error] google-genai package is not installed.")
        print("Run: pip install google-genai\n")
        return create_refusal_response("google-genai package is missing. Please run 'pip install google-genai'.")

    # 3. Check for empty retrieval results
    if not retrieved_results:
        return create_refusal_response("I cannot answer this question because no relevant context was found in the indexed documents.")

    context_str = format_context_for_prompt(retrieved_results)

    # 4. Construct grounded prompt with strict instructions
    prompt = f"""You are a clinical decision support AI assistant. Your task is to answer the user's clinical question based strictly and ONLY on the provided Context below.

CRITICAL GROUNDING RULES:

1. Answer ONLY using information directly supported by the provided Context.

2. Do NOT use outside medical knowledge, general background knowledge, assumptions, personal opinions, or information that is not present in the Context.

3. Do NOT invent, infer, extrapolate, or hallucinate:
   - medical facts
   - recommendations
   - document names
   - section names
   - page numbers
   - source URLs
   - citation information

4. If the Context does NOT contain sufficient evidence to answer the question:
   - Set "confidence" to "insufficient".
   - Set "recommendation" to a concise statement explaining that the available source evidence is insufficient to answer the question.
   - Set "evidence" to "".
   - Set "citations" to [].

5. If the Context contains sufficient evidence:
   - Provide a direct answer in "recommendation".
   - Base the answer only on the retrieved Context.
   - Provide supporting text in "evidence" by quoting or lightly trimming text that is directly present in the Context.
   - Do not add information that is not supported by the Context.

6. Citation rules:

   A. For PDF sources:
      - "document" MUST exactly match the document_name in the retrieved metadata.
      - "page" MUST exactly match the page_number in the retrieved metadata.
      - "section" MUST exactly match the section metadata when available; otherwise use "N/A".
      - "url" MUST be null.

   B. For MedlinePlus sources:
      - "document" MUST exactly match the document_name in the retrieved metadata.
      - "page" MUST be null.
      - "section" MUST exactly match the section metadata when available; otherwise use "N/A".
      - "url" MUST exactly match the source_url in the retrieved metadata.

7. Every citation MUST correspond to one of the documents or chunks actually provided in the Context.

8. Never create a citation based on information outside the Context.

9. If you cannot verify the document name, page number, or URL from the Context metadata, do not create that citation.

10. Confidence levels:
    - "high": The Context directly and clearly supports the answer.
    - "medium": The Context supports the answer but the evidence is limited or incomplete.
    - "low": The Context provides only weak or partial support.
    - "insufficient": The Context does not provide enough evidence to answer safely.

11. If confidence is "insufficient":
    - recommendation must clearly state that the retrieved evidence is insufficient.
    - evidence must be "".
    - citations must be [].

12. Return ONLY the requested structured JSON response. Do not add explanations outside the JSON structure.

Context:
{context_str}

Question: {question}"""

    # 5. Execute Gemini call using google-genai SDK with structured output
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=config.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.0,
                response_mime_type="application/json",
                response_schema=GroundedResponseModel,
            )
        )

        response_text = response.text.strip()
        result = json.loads(response_text)

        # 6. Validate against JSON schema — fail safely if invalid
        schema = load_response_schema()
        if schema and jsonschema:
            try:
                jsonschema.validate(instance=result, schema=schema)
            except jsonschema.ValidationError as ve:
                print(f"\n[Validation Error] LLM output failed schema validation: {ve.message}")
                return create_refusal_response("The model response did not meet the required JSON schema.")

        # 7. Programmatic Citation Validation — reject hallucinated citations
        if not validate_citations(result, retrieved_results):
            return create_refusal_response(
                "The generated response contained citation metadata that was not present in the retrieved evidence."
            )

        return result

    except json.JSONDecodeError:
        print("[Error] Could not parse Gemini output as JSON.")
        return create_refusal_response("The model generated an invalid response format.")
    except Exception as e:
        error_msg = str(e)
        print(f"\n[Error] Gemini API Error: {error_msg}")
        if "API_KEY" in error_msg or "INVALID_ARGUMENT" in error_msg:
            print("Please check that your GEMINI_API_KEY in .env is valid.")
        elif "429" in error_msg or "QUOTA" in error_msg.upper():
            print("Gemini API rate limit / quota exceeded. Please try again later.")
        return create_refusal_response(f"Gemini API request failed: {error_msg}")


if __name__ == "__main__":
    print("generate.py is a module. Run pipeline.py to test the full end-to-end flow.")
