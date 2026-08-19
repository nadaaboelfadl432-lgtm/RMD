"""
Clinical RAG Assistant - Streamlit Web Interface
------------------------------------------------
A clean, trustworthy, modern medical UI for the Clinical RAG system.
Displays evidence-grounded recommendations, confidence levels, 
supporting evidence, and citation details from WHO Guidelines & MedlinePlus.
"""
import sys
from pathlib import Path
import streamlit as st

# Ensure current directory is in Python path for module imports
CURRENT_DIR = Path(__file__).parent.resolve()
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

try:
    from pipeline import run_pipeline
except Exception as import_err:
    run_pipeline = None
    _import_error_msg = str(import_err)

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Clinical RAG Assistant",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom Medical CSS Design System ---
st.markdown(
    """
    <style>
    /* Global Page Styling */
    .stApp {
        background-color: #F5F9FC;
        color: #1F2937;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Main Layout Alignment */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 800px;
    }

    /* Header Component */
    .clinical-header {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(23, 105, 170, 0.05);
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .clinical-header-icon {
        font-size: 38px;
        background: #EBF3FA;
        border-radius: 12px;
        width: 56px;
        height: 56px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .clinical-header-title {
        color: #1769AA;
        font-size: 26px;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
    }
    .clinical-header-subtitle {
        color: #64748B;
        font-size: 14px;
        font-weight: 500;
        margin-top: 4px;
        margin-bottom: 0;
    }

    /* Input Card Container */
    .input-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 24px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(23, 105, 170, 0.04);
    }
    
    .input-label {
        font-size: 15px;
        font-weight: 600;
        color: #1F2937;
        margin-bottom: 8px;
    }

    /* Style Text Area and Button */
    .stTextArea textarea {
        border-radius: 10px !important;
        border: 1px solid #CBD5E1 !important;
        background-color: #FAFAFA !important;
        color: #1F2937 !important;
        font-size: 15px !important;
    }
    .stTextArea textarea:focus {
        border-color: #1769AA !important;
        box-shadow: 0 0 0 2px rgba(23, 105, 170, 0.15) !important;
        background-color: #FFFFFF !important;
    }
    
    .stButton button {
        background-color: #1769AA !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        border: none !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 6px rgba(23, 105, 170, 0.2) !important;
    }
    .stButton button:hover {
        background-color: #125488 !important;
        box-shadow: 0 4px 10px rgba(23, 105, 170, 0.3) !important;
    }

    /* Empty State Card */
    .empty-state-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 36px 28px;
        text-align: center;
        border: 1px dashed #CBD5E1;
        margin-bottom: 24px;
    }
    .empty-state-icon {
        font-size: 40px;
        margin-bottom: 12px;
    }
    .empty-state-text {
        color: #64748B;
        font-size: 15px;
        max-width: 520px;
        margin: 0 auto 20px auto;
        line-height: 1.5;
    }

    /* Section Headings */
    .section-title {
        font-size: 17px;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* Main Answer Card */
    .answer-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 14px rgba(23, 105, 170, 0.05);
    }
    .recommendation-text {
        font-size: 16px;
        line-height: 1.65;
        color: #1F2937;
        font-weight: 450;
        white-space: pre-wrap;
    }

    /* Confidence Badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .badge-high {
        background-color: #E8F5E9;
        color: #2E7D32;
        border: 1px solid #A5D6A7;
    }
    .badge-medium {
        background-color: #FFF8E1;
        color: #D97706;
        border: 1px solid #FDE68A;
    }
    .badge-low {
        background-color: #FFEBEE;
        color: #D32F2F;
        border: 1px solid #FFCDD2;
    }
    .badge-insufficient {
        background-color: #F1F5F9;
        color: #64748B;
        border: 1px solid #CBD5E1;
    }

    /* Evidence Block */
    .evidence-card {
        background: #F8FAFC;
        border-left: 4px solid #2A9D8F;
        border-radius: 8px 12px 12px 8px;
        padding: 18px 22px;
        margin-bottom: 20px;
        border-top: 1px solid #E2E8F0;
        border-right: 1px solid #E2E8F0;
        border-bottom: 1px solid #E2E8F0;
    }
    .evidence-text {
        font-size: 14px;
        line-height: 1.6;
        color: #334155;
        font-style: italic;
    }

    /* Citation Cards */
    .citation-grid {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-bottom: 24px;
    }
    .citation-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 14px 18px;
        border: 1px solid #E2E8F0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
    }
    .citation-main {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    .citation-doc {
        font-size: 14px;
        font-weight: 600;
        color: #1F2937;
    }
    .citation-meta {
        font-size: 13px;
        color: #64748B;
    }
    .citation-link {
        color: #1769AA;
        text-decoration: none;
        font-size: 13px;
        font-weight: 600;
        padding: 4px 12px;
        background: #EBF3FA;
        border-radius: 6px;
        transition: background 0.2s ease;
    }
    .citation-link:hover {
        background: #D6E8F7;
        text-decoration: underline;
    }

    /* Warning / Insufficient Box */
    .insufficient-box {
        background-color: #FEF2F2;
        border: 1px solid #FCA5A5;
        border-radius: 12px;
        padding: 18px 22px;
        color: #991B1B;
        font-size: 15px;
        line-height: 1.5;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    /* Disclaimer Footer */
    .disclaimer-box {
        margin-top: 40px;
        padding-top: 16px;
        border-top: 1px solid #E2E8F0;
        text-align: center;
        color: #94A3B8;
        font-size: 12px;
        line-height: 1.5;
    }

    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Session State Initialization ---
if "submitted_question" not in st.session_state:
    st.session_state["submitted_question"] = ""
if "pipeline_result" not in st.session_state:
    st.session_state["pipeline_result"] = None
if "is_loading" not in st.session_state:
    st.session_state["is_loading"] = False
if "error_message" not in st.session_state:
    st.session_state["error_message"] = None


def handle_sample_click(question_text: str):
    """Callback for sample query buttons."""
    st.session_state["submitted_question"] = question_text
    st.session_state["should_run"] = True


# --- 1. HEADER SECTION ---
st.markdown(
    """
    <div class="clinical-header">
        <div class="clinical-header-icon">🩺</div>
        <div>
            <h1 class="clinical-header-title">Clinical RAG Assistant</h1>
            <p class="clinical-header-subtitle">Evidence-Grounded Clinical Information Assistant</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- 2. QUESTION INPUT SECTION ---
# Sample questions list
SAMPLE_QUESTIONS = [
    "What are the symptoms of high blood pressure?",
    "What blood pressure level does WHO recommend for starting treatment?",
    "What is the target blood pressure according to the WHO guideline?"
]

# Check if a sample button triggered execution
default_text = st.session_state.get("submitted_question", "")

with st.container():
    question_input = st.text_area(
        label="Ask a clinical question",
        value=default_text,
        placeholder="e.g., What blood pressure level does WHO recommend for starting treatment?",
        height=100,
        key="clinical_query_input"
    )

    col_btn, _ = st.columns([1, 2])
    with col_btn:
        ask_clicked = st.button("Ask Question", use_container_width=True)

# Determine if query should be processed
should_run = ask_clicked or st.session_state.pop("should_run", False)

if should_run and question_input.strip():
    query_to_process = question_input.strip()
    st.session_state["submitted_question"] = query_to_process
    st.session_state["error_message"] = None
    st.session_state["pipeline_result"] = None

    # --- 3. LOADING STATE & EXECUTION ---
    if run_pipeline is None:
        st.session_state["error_message"] = f"Backend pipeline import failed: {_import_error_msg}"
    else:
        with st.spinner("Searching clinical sources and generating an evidence-grounded answer..."):
            try:
                response_obj = run_pipeline(query_to_process)
                st.session_state["pipeline_result"] = response_obj
            except Exception as ex:
                st.session_state["error_message"] = (
                    "An unexpected error occurred while processing your clinical request. "
                    "Please check the server logs for technical details."
                )

# --- DISPLAY RESULTS OR EMPTY STATE ---
result = st.session_state.get("pipeline_result")
error_msg = st.session_state.get("error_message")

# --- 9. ERROR HANDLING ---
if error_msg:
    st.error(error_msg, icon="⚠️")

elif result is not None:
    recommendation = result.get("recommendation", "")
    evidence = result.get("evidence", "")
    citations = result.get("citations", [])
    confidence = str(result.get("confidence", "insufficient")).lower()

    # Badge HTML mapping
    badge_classes = {
        "high": "badge-high",
        "medium": "badge-medium",
        "low": "badge-low",
        "insufficient": "badge-insufficient"
    }
    badge_class = badge_classes.get(confidence, "badge-insufficient")
    badge_html = f'<span class="badge {badge_class}">{confidence.upper()} CONFIDENCE</span>'

    # --- 10. INSUFFICIENT EVIDENCE STATE ---
    if confidence == "insufficient":
        st.markdown(
            f"""
            <div class="insufficient-box">
                <span style="font-size: 20px;">ℹ️</span>
                <div>
                    <strong>Insufficient Evidence</strong><br/>
                    Insufficient evidence was found in the retrieved sources to answer this question.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --- 4. CLINICAL ANSWER SECTION ---
    st.markdown(
        f"""
        <div class="answer-card">
            <div class="section-title">
                <span>Clinical Answer</span>
                {badge_html}
            </div>
            <div class="recommendation-text">{recommendation}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- 6. SUPPORTING EVIDENCE SECTION ---
    if evidence and confidence != "insufficient":
        st.markdown(
            f"""
            <div class="section-title" style="margin-top: 24px;">Supporting Evidence</div>
            <div class="evidence-card">
                <div class="evidence-text">"{evidence}"</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --- 7. SOURCES / CITATIONS SECTION ---
    if citations and confidence != "insufficient":
        st.markdown('<div class="section-title" style="margin-top: 24px;">Sources</div>', unsafe_allow_html=True)
        st.markdown('<div class="citation-grid">', unsafe_allow_html=True)

        for cit in citations:
            doc_name = cit.get("document", "Unknown Source")
            section = cit.get("section")
            page = cit.get("page")
            url = cit.get("url")

            # PDF Source vs MedlinePlus Source handling
            meta_parts = []
            
            # Check for MedlinePlus / URL source
            if url:
                meta_parts.append("Source: MedlinePlus")
                if section and section != "N/A":
                    meta_parts.append(f"Section: {section}")
                meta_str = " • ".join(meta_parts)

                st.markdown(
                    f"""
                    <div class="citation-card">
                        <div class="citation-main">
                            <span class="citation-doc">📄 {doc_name}</span>
                            <span class="citation-meta">{meta_str}</span>
                        </div>
                        <a href="{url}" target="_blank" class="citation-link">Open Source ↗</a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                # PDF Source
                if page is not None and str(page).strip() not in ["None", "null", ""]:
                    meta_parts.append(f"Page {page}")
                if section and section != "N/A":
                    meta_parts.append(f"Section: {section}")
                
                meta_str = " • ".join(meta_parts) if meta_parts else "PDF Document"

                st.markdown(
                    f"""
                    <div class="citation-card">
                        <div class="citation-main">
                            <span class="citation-doc">📘 {doc_name}</span>
                            <span class="citation-meta">{meta_str}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown('</div>', unsafe_allow_html=True)

# --- 8. EMPTY STATE ---
else:
    st.markdown(
        """
        <div class="empty-state-card">
            <div class="empty-state-icon">📋</div>
            <div style="font-weight: 600; font-size: 17px; color: #1F2937; margin-bottom: 6px;">
                Welcome to the Clinical RAG Assistant
            </div>
            <div class="empty-state-text">
                Ask a clinical question to retrieve evidence-grounded information from trusted sources.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="input-label" style="margin-bottom: 10px;">Suggested Questions:</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    for idx, q_text in enumerate(SAMPLE_QUESTIONS):
        with cols[idx]:
            st.button(
                q_text,
                key=f"sample_q_{idx}",
                use_container_width=True,
                on_click=handle_sample_click,
                args=(q_text,)
            )

# --- 11. DISCLAIMER FOOTER ---
st.markdown(
    """
    <div class="disclaimer-box">
        ⚠️ <strong>Clinical Notice:</strong> This system provides information grounded strictly in retrieved clinical sources and is not a substitute for professional medical advice, diagnosis, or treatment.
    </div>
    """,
    unsafe_allow_html=True
)
