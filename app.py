"""
AI Clinical Decision Support - Premium Dark Medical AI Dashboard
----------------------------------------------------------------
A high-performance, dark-themed healthcare SaaS dashboard for evidence-grounded medical QA.
Features multilingual generation, dark-themed attached autocomplete search,
and concise explanatory supporting evidence summaries.
"""
import sys
import json
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

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
    page_title="AI Clinical Decision Support — Clinical AI Dashboard",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

SUPPORTED_LANGUAGES = [
    "English",
    "Arabic",
    "French",
    "Spanish",
    "German",
    "Italian",
    "Turkish",
    "Portuguese",
    "Hindi",
    "Chinese",
    "Japanese"
]

# Declare custom Streamlit component from local folder
COMPONENT_DIR = CURRENT_DIR / "google_search_component"
google_autocomplete_component = components.declare_component(
    "google_autocomplete_component",
    path=str(COMPONENT_DIR)
)


def render_autocomplete_search(initial_val: str) -> str:
    """Renders the dark Google Search Autocomplete component safely,
    guaranteeing that initial_val is always a string.
    """
    if not isinstance(initial_val, str):
        initial_val = ""

    component_result = google_autocomplete_component(
        initial_value=initial_val,
        key="google_autocomplete_widget_instance"
    )

    if isinstance(component_result, str):
        return component_result
    return initial_val


# --- Custom Medical CSS Design System (Premium Dark SaaS Theme) ---
st.markdown(
    """
    <style>
    /* Global Background & Base Theme */
    .stApp {
        background-color: #06111F;
        background-image: 
            radial-gradient(circle at 85% 8%, rgba(47, 128, 237, 0.08) 0%, transparent 45%),
            radial-gradient(circle at 12% 90%, rgba(139, 92, 246, 0.07) 0%, transparent 45%);
        color: #F8FAFC;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    
    /* Layout Container Alignment */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1220px;
    }

    /* 1. Header Hero Card */
    .clinical-hero-card {
        background: #0D1D30;
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 22px 32px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
        background-image: radial-gradient(circle at 90% 10%, rgba(47, 128, 237, 0.12) 0%, transparent 60%),
                          radial-gradient(circle at 10% 90%, rgba(139, 92, 246, 0.12) 0%, transparent 60%);
    }
    .hero-content-left {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .hero-icon-box {
        font-size: 32px;
        background: rgba(47, 128, 237, 0.12);
        border: 1px solid rgba(47, 128, 237, 0.25);
        border-radius: 12px;
        width: 54px;
        height: 54px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .hero-title {
        color: #F8FAFC;
        font-size: 24px;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
        letter-spacing: -0.3px;
    }
    .hero-subtitle {
        color: #94A3B8;
        font-size: 14px;
        font-weight: 450;
        margin-top: 4px;
        margin-bottom: 0;
    }
    .hero-ai-badge {
        background: rgba(34, 211, 238, 0.1);
        border: 1px solid rgba(34, 211, 238, 0.25);
        color: #22D3EE;
        font-size: 12px;
        font-weight: 600;
        padding: 6px 14px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        gap: 6px;
        letter-spacing: 0.5px;
        white-space: nowrap;
    }

    /* Column Panel Titles */
    .panel-header-title {
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .panel-title-left {
        color: #8B5CF6;
    }
    .panel-title-right {
        color: #22D3EE;
    }

    /* Input Card Container */
    .input-panel-card {
        background: #0D1D30;
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        margin-bottom: 20px;
    }

    .input-field-label {
        font-size: 13.5px;
        font-weight: 600;
        color: #94A3B8;
        margin-bottom: 8px;
    }

    /* Selectbox Main Control Dark Theme */
    .stSelectbox > div > div {
        border-radius: 10px !important;
        border: 1px solid rgba(148, 163, 184, 0.25) !important;
        background-color: #081728 !important;
        color: #F8FAFC !important;
    }
    .stSelectbox label {
        color: #94A3B8 !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
    }
    .stSelectbox svg {
        fill: #22D3EE !important;
    }

    /* BaseWeb Selectbox Popover Dropdown Menu List */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[role="listbox"] {
        background-color: #0D1D30 !important;
        border: 1px solid rgba(148, 163, 184, 0.25) !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
    }

    /* Individual Dropdown Menu Options */
    li[role="option"],
    div[role="option"],
    ul[role="listbox"] li,
    div[data-baseweb="menu"] div {
        background-color: #0D1D30 !important;
        color: #F8FAFC !important;
        font-size: 14px !important;
        padding: 10px 16px !important;
        border-radius: 6px !important;
        cursor: pointer !important;
        transition: background-color 0.15s ease, color 0.15s ease !important;
    }

    /* Hover & Active Selected State for Language Options */
    li[role="option"]:hover,
    li[role="option"][aria-selected="true"],
    div[role="option"]:hover,
    div[role="option"][aria-selected="true"],
    ul[role="listbox"] li:hover {
        background-color: #0A1728 !important;
        color: #22D3EE !important;
    }

    /* Primary Submit Button "[ ✦ Ask ]" */
    div.stButton > button.ask-primary-btn, div.stButton > button {
        background: linear-gradient(135deg, #2F80ED 0%, #7C3AED 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 15.5px !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        border: none !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 14px rgba(47, 128, 237, 0.3) !important;
        width: 100% !important;
        letter-spacing: 0.3px !important;
        min-height: 52px !important;
    }
    div.stButton > button:hover {
        opacity: 0.92 !important;
        box-shadow: 0 6px 18px rgba(47, 128, 237, 0.45) !important;
        transform: translateY(-1px);
    }

    /* Final Answer Card */
    .answer-card {
        background: #0D1D30;
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 26px;
        margin-bottom: 20px;
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.3);
    }
    .card-header-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    }
    .card-header-label {
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1px;
        color: #94A3B8;
        text-transform: uppercase;
    }

    .recommendation-text {
        font-size: 16px;
        line-height: 1.7;
        color: #F8FAFC;
        font-weight: 400;
        white-space: pre-wrap;
    }

    /* Confidence Badges (Mapping Backend Confidence Output) */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .badge-high {
        background-color: #052E16;
        color: #22C55E;
        border: 1px solid rgba(34, 197, 94, 0.35);
    }
    .badge-medium {
        background-color: #451A03;
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }
    .badge-low {
        background-color: #450A0A;
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.35);
    }
    .badge-insufficient {
        background-color: #450A0A;
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.35);
    }

    /* Supporting Evidence Card */
    .evidence-card {
        background: #0D1D30;
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 22px 26px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .evidence-text {
        font-size: 14.5px;
        line-height: 1.65;
        color: #94A3B8;
        white-space: pre-wrap;
    }

    /* Sources Cards Grid */
    .citation-grid {
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-bottom: 24px;
    }
    .citation-card {
        background: #0D1D30;
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 12px;
        padding: 14px 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        transition: border-color 0.15s ease;
    }
    .citation-card:hover {
        border-color: rgba(139, 92, 246, 0.4);
    }
    .citation-main {
        display: flex;
        flex-direction: column;
        gap: 3px;
    }
    .citation-doc {
        font-size: 14px;
        font-weight: 600;
        color: #F8FAFC;
    }
    .citation-meta {
        font-size: 13px;
        color: #94A3B8;
    }
    .citation-link {
        color: #22D3EE;
        text-decoration: none;
        font-size: 13px;
        font-weight: 600;
        padding: 5px 12px;
        background: rgba(34, 211, 238, 0.1);
        border: 1px solid rgba(34, 211, 238, 0.25);
        border-radius: 8px;
        transition: all 0.15s ease;
    }
    .citation-link:hover {
        background: rgba(34, 211, 238, 0.2);
        color: #FFFFFF;
    }

    /* Refusal Box */
    .insufficient-box {
        background-color: #2A0808;
        border: 1px solid #EF4444;
        border-radius: 12px;
        padding: 18px 22px;
        color: #FCA5A5;
        font-size: 14.5px;
        line-height: 1.5;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    /* Clinical Disclaimer Notice */
    .disclaimer-card {
        background: #0A1728;
        border: 1px solid rgba(47, 128, 237, 0.25);
        border-radius: 12px;
        padding: 14px 18px;
        margin-top: 24px;
        color: #94A3B8;
        font-size: 12.5px;
        line-height: 1.55;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    /* Hide Default Streamlit Chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Session State Initialization ---
if "current_search_query" not in st.session_state or not isinstance(st.session_state["current_search_query"], str):
    st.session_state["current_search_query"] = ""

if "selected_language" not in st.session_state:
    st.session_state["selected_language"] = "English"

if "pipeline_result" not in st.session_state:
    st.session_state["pipeline_result"] = None

if "error_message" not in st.session_state:
    st.session_state["error_message"] = None


# --- 1. HERO HEADER CARD ---
st.markdown(
    """
    <div class="clinical-hero-card">
        <div class="hero-content-left">
            <div class="hero-icon-box">🩺</div>
            <div>
                <h1 class="hero-title">AI Clinical Decision Support</h1>
                <p class="hero-subtitle">Your evidence-grounded medical assistant</p>
            </div>
        </div>
        <div class="hero-ai-badge">
            <span>✨</span> MEDICAL AI
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- 2. TWO-COLUMN DASHBOARD LAYOUT (30% / 70%) ---
col_input, col_results = st.columns([1, 2.2])

# ==============================================================================
# LEFT COLUMN: INPUT PANEL (~30%)
# ==============================================================================
with col_input:
    st.markdown('<div class="panel-header-title panel-title-left"><span>⚙️</span> INPUT PANEL</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="input-panel-card">', unsafe_allow_html=True)
        
        # Response Language Selector (Positioned ABOVE Search Component)
        selected_language = st.selectbox(
            label="Response Language",
            options=SUPPORTED_LANGUAGES,
            index=SUPPORTED_LANGUAGES.index(st.session_state.get("selected_language", "English")),
            key="language_selector_key"
        )
        st.session_state["selected_language"] = selected_language

        st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)

        # Custom Google Autocomplete Component (Full-Width, 54px Height)
        st.session_state["current_search_query"] = render_autocomplete_search(st.session_state["current_search_query"])

        st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)

        # Primary Submit Button "[ ✦ Ask ]"
        ask_clicked = st.button("✦ Ask", use_container_width=True, key="ask_submit_btn")

        st.markdown('</div>', unsafe_allow_html=True)

# Process query trigger
query_text_to_run = st.session_state["current_search_query"].strip() if isinstance(st.session_state.get("current_search_query"), str) else ""

if ask_clicked and query_text_to_run:
    st.session_state["error_message"] = None
    st.session_state["pipeline_result"] = None

    if run_pipeline is None:
        st.session_state["error_message"] = f"Backend pipeline import failed: {_import_error_msg}"
    else:
        with st.spinner(f"Searching clinical sources and generating answer in {selected_language}..."):
            try:
                response_obj = run_pipeline(query_text_to_run, language=selected_language)
                st.session_state["pipeline_result"] = response_obj
            except Exception as ex:
                st.session_state["error_message"] = (
                    "An unexpected error occurred while processing your clinical request. "
                    "Please check terminal/server logs for technical details."
                )

# ==============================================================================
# RIGHT COLUMN: RESULTS PANEL (~70%)
# ==============================================================================
with col_results:
    st.markdown('<div class="panel-header-title panel-title-right"><span>📊</span> RESULTS PANEL</div>', unsafe_allow_html=True)

    result = st.session_state.get("pipeline_result")
    error_msg = st.session_state.get("error_message")

    if error_msg:
        st.error(error_msg, icon="⚠️")

    elif result is not None:
        recommendation = result.get("recommendation", "")
        evidence = result.get("evidence", "")
        citations = result.get("citations", [])
        confidence = str(result.get("confidence", "insufficient")).lower()

        # Confidence Badge Mapping
        if confidence == "high":
            badge_html = '<span class="badge badge-high">🛡 HIGH CONFIDENCE</span>'
        elif confidence in ["medium", "low"]:
            badge_html = '<span class="badge badge-medium">⚠ MODERATE CONFIDENCE</span>'
        else:
            badge_html = '<span class="badge badge-insufficient">⚠ INSUFFICIENT EVIDENCE</span>'

        # Safe Refusal Box when confidence is insufficient
        if confidence == "insufficient":
            st.markdown(
                f"""
                <div class="insufficient-box">
                    <span style="font-size: 22px;">⚠️</span>
                    <div>
                        <strong>Insufficient Evidence</strong><br/>
                        Insufficient evidence was found in the retrieved sources to answer this question.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # FINAL ANSWER CARD
        st.markdown(
            f"""
            <div class="answer-card">
                <div class="card-header-row">
                    <span class="card-header-label">FINAL ANSWER ({selected_language})</span>
                    {badge_html}
                </div>
                <div class="recommendation-text">{recommendation}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # SUPPORTING EVIDENCE CARD
        if evidence and confidence != "insufficient":
            st.markdown(
                f"""
                <div class="evidence-card">
                    <div class="card-header-row" style="margin-bottom: 12px; padding-bottom: 8px;">
                        <span class="card-header-label" style="color: #8B5CF6;">📚 SUPPORTING EVIDENCE</span>
                    </div>
                    <div class="evidence-text">{evidence}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # SOURCES / CITATIONS SECTION
        if citations and confidence != "insufficient":
            st.markdown(
                """
                <div class="card-header-label" style="margin-bottom: 10px; margin-top: 18px;">SOURCES & CITATIONS</div>
                <div class="citation-grid">
                """,
                unsafe_allow_html=True
            )

            for cit in citations:
                doc_name = cit.get("document", "Unknown Source")
                section = cit.get("section")
                page = cit.get("page")
                url = cit.get("url")

                meta_parts = []
                
                # MedlinePlus / URL source
                if url and str(url).strip() not in ["None", "null", ""]:
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

    else:
        # Default Empty State in Results Panel
        st.markdown(
            """
            <div class="answer-card" style="text-align: center; padding: 48px 28px;">
                <div style="font-size: 36px; margin-bottom: 12px;">📋</div>
                <div style="font-weight: 700; font-size: 18px; color: #F8FAFC; margin-bottom: 8px;">
                    Clinical Decision Support System
                </div>
                <div style="color: #94A3B8; font-size: 14px; max-width: 480px; margin: 0 auto; line-height: 1.6;">
                    Select your response language and ask a clinical question to retrieve evidence-grounded medical information from WHO Guidelines and MedlinePlus.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# --- CLINICAL DISCLAIMER NOTICE ---
st.markdown(
    """
    <div class="disclaimer-card">
        <span style="font-size: 18px; color: #2F80ED;">ℹ️</span>
        <div>
            <strong>Clinical Notice:</strong> This system provides information grounded strictly in retrieved clinical sources and is not a substitute for professional medical advice, diagnosis, or treatment.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
