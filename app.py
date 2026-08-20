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

LANGUAGE_FLAGS = {
    "English": "EN",
    "Arabic": "AR",
    "French": "FR",
    "Spanish": "ES",
    "German": "DE",
    "Italian": "IT",
    "Turkish": "TR",
    "Portuguese": "PT",
    "Hindi": "HI",
    "Chinese": "ZH",
    "Japanese": "JA",
}


def format_language_option(lang_name: str) -> str:
    code = LANGUAGE_FLAGS.get(lang_name, "")
    return f"[{code}] {lang_name}" 

# Declare custom Streamlit component from local folder
COMPONENT_DIR = CURRENT_DIR / "google_search_component"
google_autocomplete_component = components.declare_component(
    "google_autocomplete_component",
    path=str(COMPONENT_DIR)
)


def render_autocomplete_search(initial_val: str, theme: str = "dark"):
    """Renders the Google Search Autocomplete component safely,
    returning dictionary or string component output.
    """
    if not isinstance(initial_val, str):
        initial_val = ""

    component_result = google_autocomplete_component(
        initial_value=initial_val,
        theme=theme,
        key="google_autocomplete_widget_instance",
        default={"query": initial_val, "submitted": False}
    )

    if isinstance(component_result, dict):
        return component_result
    elif isinstance(component_result, str):
        return component_result
    return {"query": initial_val, "submitted": False}


# --- Dynamic Medical Theme CSS System (Dark & Light Modes) ---
current_theme = st.session_state.get("theme", "dark")

if current_theme == "light":
    theme_css = """
    .stApp {
        background-color: #F8FAFC;
        background-image: 
            radial-gradient(circle at 85% 8%, rgba(37, 99, 235, 0.05) 0%, transparent 45%),
            radial-gradient(circle at 12% 90%, rgba(14, 165, 233, 0.05) 0%, transparent 45%);
        color: #0F172A;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1220px;
    }
    .clinical-hero-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 22px 32px;
        margin-bottom: 24px;
        box-shadow: 0 6px 24px rgba(15, 23, 42, 0.06);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
        background-image: radial-gradient(circle at 90% 10%, rgba(37, 99, 235, 0.06) 0%, transparent 60%),
                          radial-gradient(circle at 10% 90%, rgba(14, 165, 233, 0.06) 0%, transparent 60%);
    }
    .hero-content-left {
        display: flex;
        align-items: center;
        gap: 16px;
        flex: 1;
    }
    .hero-stethoscope-art {
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .hero-title {
        color: #0F172A;
        font-size: 24px;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
        letter-spacing: -0.3px;
    }
    .hero-subtitle {
        color: #64748B;
        font-size: 14px;
        font-weight: 450;
        margin-top: 4px;
        margin-bottom: 0;
    }
    .hero-ai-badge {
        background: rgba(2, 132, 199, 0.08);
        border: 1px solid rgba(2, 132, 199, 0.25);
        color: #0284C7;
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
    .unified-nav-box {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 12px;
        padding: 6px 10px;
        display: flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
        margin-bottom: 0px;
    }
    div.st-key-top_nav_language_selector,
    div.st-key-top_nav_language_selector > div,
    div.st-key-top_nav_language_selector [data-testid="stSelectbox"] {
        margin-bottom: 0px !important;
    }
    div.st-key-top_nav_language_selector [data-baseweb="select"],
    div.st-key-top_nav_language_selector [data-baseweb="select"] > div,
    div.st-key-top_nav_language_selector > div > div {
        background-color: transparent !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 4px 8px !important;
        min-height: 38px !important;
        height: 38px !important;
        color: #0F172A !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        box-shadow: none !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    div.st-key-top_nav_language_selector [data-baseweb="select"]:hover,
    div.st-key-top_nav_language_selector [data-baseweb="select"] > div:hover {
        background-color: #F1F5F9 !important;
    }
    div.st-key-top_nav_language_selector [data-baseweb="select"] *,
    div.st-key-top_nav_language_selector [data-testid="stSelectbox"] * {
        color: #0F172A !important;
        background-color: transparent !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        opacity: 1 !important;
    }
    div.st-key-top_nav_language_selector svg,
    div.st-key-top_nav_language_selector svg path {
        fill: #0284C7 !important;
        color: #0284C7 !important;
        width: 16px !important;
        height: 16px !important;
        opacity: 1 !important;
    }
    [data-baseweb="popover"] [data-baseweb="menu"],
    [data-baseweb="popover"] ul[role="listbox"] {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
    }
    [data-baseweb="popover"] li[role="option"],
    [data-baseweb="popover"] [role="option"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    [data-baseweb="popover"] li[role="option"]:hover,
    [data-baseweb="popover"] [role="option"]:hover,
    [data-baseweb="popover"] li[role="option"][aria-selected="true"],
    [data-baseweb="popover"] [role="option"][aria-selected="true"] {
        background-color: #F8FAFC !important;
        color: #0284C7 !important;
    }
    .unified-nav-box .nav-divider {
        width: 1px;
        height: 24px;
        background: #CBD5E1;
        flex-shrink: 0;
    }
    div.st-key-top_nav_theme_toggle {
        margin-bottom: 0px !important;
    }
    div.st-key-top_nav_theme_toggle > button,
    div.st-key-top_nav_theme_toggle button {
        background-color: #F1F5F9 !important;
        border: none !important;
        color: #0F172A !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        padding: 4px 14px !important;
        min-height: 38px !important;
        height: 38px !important;
        box-shadow: none !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    div.st-key-top_nav_theme_toggle > button:hover,
    div.st-key-top_nav_theme_toggle button:hover {
        background-color: #E2E8F0 !important;
        color: #0F172A !important;
    }
    div.st-key-top_nav_theme_toggle button *,
    div.st-key-top_nav_theme_toggle button p,
    div.st-key-top_nav_theme_toggle button span {
        color: #0F172A !important;
        opacity: 1 !important;
        font-weight: 600 !important;
    }
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
        color: #6D28D9;
    }
    .panel-title-right {
        color: #0284C7;
    }
    .answer-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 26px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(15, 23, 42, 0.06);
    }
    .card-header-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid #F1F5F9;
    }
    .card-header-label {
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1px;
        color: #64748B;
        text-transform: uppercase;
    }
    .recommendation-text {
        font-size: 16px;
        line-height: 1.7;
        color: #0F172A;
        font-weight: 400;
        white-space: pre-wrap;
    }
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
        background-color: #DCFCE7;
        color: #15803D;
        border: 1px solid #86EFAC;
    }
    .badge-medium {
        background-color: #FEF3C7;
        color: #B45309;
        border: 1px solid #FDE68A;
    }
    .badge-low {
        background-color: #FEE2E2;
        color: #B91C1C;
        border: 1px solid #FCA5A5;
    }
    .badge-insufficient {
        background-color: #FEE2E2;
        color: #B91C1C;
        border: 1px solid #FCA5A5;
    }
    .evidence-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 22px 26px;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);
    }
    .evidence-text {
        font-size: 14.5px;
        line-height: 1.65;
        color: #475569;
        white-space: pre-wrap;
    }
    .citation-grid {
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-bottom: 24px;
    }
    .citation-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 14px 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        transition: border-color 0.15s ease;
    }
    .citation-card:hover {
        border-color: rgba(37, 99, 235, 0.4);
    }
    .citation-main {
        display: flex;
        flex-direction: column;
        gap: 3px;
    }
    .citation-doc {
        font-size: 14px;
        font-weight: 600;
        color: #0F172A;
    }
    .citation-meta {
        font-size: 13px;
        color: #64748B;
    }
    .citation-link {
        color: #0284C7;
        text-decoration: none;
        font-size: 13px;
        font-weight: 600;
        padding: 5px 12px;
        background: rgba(2, 132, 199, 0.08);
        border: 1px solid rgba(2, 132, 199, 0.25);
        border-radius: 8px;
        transition: all 0.15s ease;
    }
    .citation-link:hover {
        background: rgba(2, 132, 199, 0.18);
        color: #0369A1;
    }
    .insufficient-box {
        background-color: #FEF2F2;
        border: 1px solid #FCA5A5;
        border-radius: 12px;
        padding: 18px 22px;
        color: #991B1B;
        font-size: 14.5px;
        line-height: 1.5;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .disclaimer-card {
        background: #F0F9FF;
        border: 1px solid #BAE6FD;
        border-radius: 12px;
        padding: 14px 18px;
        margin-top: 24px;
        color: #334155;
        font-size: 12.5px;
        line-height: 1.55;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .stat-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);
    }
    .stat-number {
        font-size: 42px;
        font-weight: 700;
        margin: 8px 0 4px 0;
    }
    .stat-label {
        font-size: 14px;
        color: #64748B;
        font-weight: 500;
    }
    .section-title {
        font-size: 18px;
        font-weight: 700;
        color: #0F172A;
        margin: 24px 0 16px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    """
else:
    theme_css = """
    .stApp {
        background-color: #06111F;
        background-image: 
            radial-gradient(circle at 85% 8%, rgba(47, 128, 237, 0.08) 0%, transparent 45%),
            radial-gradient(circle at 12% 90%, rgba(139, 92, 246, 0.07) 0%, transparent 45%);
        color: #F8FAFC;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1220px;
    }
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
        flex: 1;
    }
    .hero-stethoscope-art {
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
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
    .unified-nav-box {
        background: #0D1D30;
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 12px;
        padding: 6px 10px;
        display: flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        margin-bottom: 0px;
    }
    div.st-key-top_nav_language_selector,
    div.st-key-top_nav_language_selector > div,
    div.st-key-top_nav_language_selector [data-testid="stSelectbox"] {
        margin-bottom: 0px !important;
    }
    div.st-key-top_nav_language_selector [data-baseweb="select"],
    div.st-key-top_nav_language_selector [data-baseweb="select"] > div,
    div.st-key-top_nav_language_selector > div > div {
        background-color: transparent !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 4px 8px !important;
        min-height: 38px !important;
        height: 38px !important;
        color: #F8FAFC !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        box-shadow: none !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    div.st-key-top_nav_language_selector [data-baseweb="select"]:hover,
    div.st-key-top_nav_language_selector [data-baseweb="select"] > div:hover {
        background-color: rgba(148, 163, 184, 0.1) !important;
    }
    div.st-key-top_nav_language_selector [data-baseweb="select"] *,
    div.st-key-top_nav_language_selector [data-testid="stSelectbox"] * {
        color: #F8FAFC !important;
        background-color: transparent !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        opacity: 1 !important;
    }
    div.st-key-top_nav_language_selector svg,
    div.st-key-top_nav_language_selector svg path {
        fill: #22D3EE !important;
        color: #22D3EE !important;
        width: 16px !important;
        height: 16px !important;
        opacity: 1 !important;
    }
    [data-baseweb="popover"] [data-baseweb="menu"],
    [data-baseweb="popover"] ul[role="listbox"] {
        background-color: #0B192C !important;
        border: 1px solid rgba(148, 163, 184, 0.25) !important;
        border-radius: 10px !important;
    }
    [data-baseweb="popover"] li[role="option"],
    [data-baseweb="popover"] [role="option"] {
        background-color: #0B192C !important;
        color: #F8FAFC !important;
    }
    [data-baseweb="popover"] li[role="option"]:hover,
    [data-baseweb="popover"] [role="option"]:hover,
    [data-baseweb="popover"] li[role="option"][aria-selected="true"],
    [data-baseweb="popover"] [role="option"][aria-selected="true"] {
        background-color: #0E223D !important;
        color: #22D3EE !important;
    }
    .unified-nav-box .nav-divider {
        width: 1px;
        height: 24px;
        background: rgba(148, 163, 184, 0.2);
        flex-shrink: 0;
    }
    div.st-key-top_nav_theme_toggle {
        margin-bottom: 0px !important;
    }
    div.st-key-top_nav_theme_toggle > button,
    div.st-key-top_nav_theme_toggle button {
        background-color: rgba(148, 163, 184, 0.1) !important;
        border: none !important;
        color: #F8FAFC !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        padding: 4px 14px !important;
        min-height: 38px !important;
        height: 38px !important;
        box-shadow: none !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    div.st-key-top_nav_theme_toggle > button:hover,
    div.st-key-top_nav_theme_toggle button:hover {
        background-color: rgba(148, 163, 184, 0.2) !important;
        color: #F8FAFC !important;
    }
    div.st-key-top_nav_theme_toggle button *,
    div.st-key-top_nav_theme_toggle button p,
    div.st-key-top_nav_theme_toggle button span {
        color: #F8FAFC !important;
        opacity: 1 !important;
        font-weight: 600 !important;
    }
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
    .stat-card {
        background: #0D1D30;
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    .stat-number {
        font-size: 42px;
        font-weight: 700;
        margin: 8px 0 4px 0;
    }
    .stat-label {
        font-size: 14px;
        color: #94A3B8;
        font-weight: 500;
    }
    .section-title {
        font-size: 18px;
        font-weight: 700;
        color: #F8FAFC;
        margin: 24px 0 16px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    """

st.markdown(f"<style>{theme_css}</style>", unsafe_allow_html=True)


# --- Session State Initialization ---
if "current_search_query" not in st.session_state or not isinstance(st.session_state["current_search_query"], str):
    st.session_state["current_search_query"] = ""

if "selected_language" not in st.session_state:
    st.session_state["selected_language"] = "English"

if "pipeline_result" not in st.session_state:
    st.session_state["pipeline_result"] = None

if "error_message" not in st.session_state:
    st.session_state["error_message"] = None

if "query_history" not in st.session_state:
    st.session_state["query_history"] = []


# --- 1. TOP NAVIGATION AREA (Language Selector + Theme Toggle at Top-Right) ---
top_nav_col_left, top_nav_col_right = st.columns([2.3, 1.7], vertical_alignment="center")
with top_nav_col_right:
    st.markdown('<div class="unified-nav-box">', unsafe_allow_html=True)
    c_lang, c_divider, c_theme = st.columns([2, 0.05, 1], vertical_alignment="center")
    with c_lang:
        current_lang = st.session_state.get("selected_language", "English")
        lang_idx = SUPPORTED_LANGUAGES.index(current_lang) if current_lang in SUPPORTED_LANGUAGES else 0
        
        selected_language = st.selectbox(
            label="Language",
            options=SUPPORTED_LANGUAGES,
            index=lang_idx,
            format_func=format_language_option,
            key="top_nav_language_selector",
            label_visibility="collapsed"
        )
        st.session_state["selected_language"] = selected_language

    with c_divider:
        st.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)

    with c_theme:
        is_dark = st.session_state.get("theme", "dark") == "dark"
        theme_btn_label = "🌙" if is_dark else "☀️"
        if st.button(theme_btn_label, key="top_nav_theme_toggle", use_container_width=True):
            st.session_state["theme"] = "light" if is_dark else "dark"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 2. HERO HEADER CARD ---
hero_html = """
<style>
    .clinical-hero-card {
        background: #0D1D30;
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 22px 32px;
        margin-bottom: 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
        background-image: radial-gradient(circle at 90% 10%, rgba(47, 128, 237, 0.12) 0%, transparent 60%),
                          radial-gradient(circle at 10% 90%, rgba(139, 92, 246, 0.12) 0%, transparent 60%);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .hero-content-left { display: flex; align-items: center; gap: 16px; flex: 1; }
    .hero-title { color: #F8FAFC; font-size: 24px; font-weight: 700; margin: 0; line-height: 1.2; }
    .hero-subtitle { color: #94A3B8; font-size: 14px; margin-top: 4px; margin-bottom: 0; }
    .hero-stethoscope-art { flex-shrink: 0; display: flex; align-items: center; }
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
        white-space: nowrap;
    }
</style>
<div class="clinical-hero-card">
    <div class="hero-content-left">
        <div>
            <h1 class="hero-title">AI Clinical Decision Support</h1>
            <p class="hero-subtitle">Your evidence-grounded medical assistant</p>
        </div>
    </div>
    <div class="hero-stethoscope-art">
        <svg viewBox="0 0 280 130" width="280" height="130" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="tubeG" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stop-color="#06B6D4"/>
                    <stop offset="100%" stop-color="#8B5CF6"/>
                </linearGradient>
                <linearGradient id="tubeG2" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#22D3EE"/>
                    <stop offset="40%" stop-color="#6366F1"/>
                    <stop offset="100%" stop-color="#7C3AED"/>
                </linearGradient>
                <radialGradient id="chestGlow" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.9"/>
                    <stop offset="60%" stop-color="#3B82F6" stop-opacity="0.4"/>
                    <stop offset="100%" stop-color="#1E40AF" stop-opacity="0"/>
                </radialGradient>
                <linearGradient id="ecgG" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#38BDF8" stop-opacity="0"/>
                    <stop offset="15%" stop-color="#38BDF8" stop-opacity="1"/>
                    <stop offset="85%" stop-color="#60A5FA" stop-opacity="1"/>
                    <stop offset="100%" stop-color="#60A5FA" stop-opacity="0"/>
                </linearGradient>
                <filter id="neonGlow">
                    <feGaussianBlur stdDeviation="3" result="blur"/>
                    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
                </filter>
                <filter id="softGlow">
                    <feGaussianBlur stdDeviation="6" result="blur"/>
                    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
                </filter>
                <filter id="ecgGlow">
                    <feGaussianBlur stdDeviation="2" result="blur"/>
                    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
                </filter>
            </defs>
            <line x1="0" y1="65" x2="48" y2="65" stroke="url(#ecgG)" stroke-width="2" stroke-linecap="round" filter="url(#ecgGlow)"/>
            <path d="M48,65 Q55,55 62,65" fill="none" stroke="url(#ecgG)" stroke-width="2" stroke-linecap="round" filter="url(#ecgGlow)"/>
            <polyline points="62,65 70,65 75,22 85,100 95,40 100,65" fill="none" stroke="url(#ecgG)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" filter="url(#neonGlow)"/>
            <path d="M100,65 Q112,48 124,65" fill="none" stroke="url(#ecgG)" stroke-width="2" stroke-linecap="round" filter="url(#ecgGlow)"/>
            <line x1="124" y1="65" x2="148" y2="65" stroke="url(#ecgG)" stroke-width="2" stroke-linecap="round" filter="url(#ecgGlow)"/>
            <circle r="3" fill="#38BDF8" filter="url(#neonGlow)" opacity="0.9">
                <animateMotion dur="2s" repeatCount="indefinite" path="M0,65 L48,65 Q55,55 62,65 L70,65 L75,22 L85,100 L95,40 L100,65 Q112,48 124,65 L148,65"/>
            </circle>
            <ellipse cx="180" cy="14" rx="4" ry="6" fill="none" stroke="url(#tubeG2)" stroke-width="2.5" transform="rotate(-12,180,14)" filter="url(#neonGlow)"/>
            <ellipse cx="220" cy="14" rx="4" ry="6" fill="none" stroke="url(#tubeG2)" stroke-width="2.5" transform="rotate(12,220,14)" filter="url(#neonGlow)"/>
            <path d="M180,20 C180,30 178,40 180,50 C182,58 188,62 195,66" stroke="url(#tubeG)" stroke-width="2.8" fill="none" stroke-linecap="round" filter="url(#neonGlow)"/>
            <path d="M220,20 C220,30 222,40 220,50 C218,58 212,62 205,66" stroke="url(#tubeG)" stroke-width="2.8" fill="none" stroke-linecap="round" filter="url(#neonGlow)"/>
            <path d="M195,66 C198,68 202,68 205,66" stroke="url(#tubeG)" stroke-width="2.8" fill="none" stroke-linecap="round" filter="url(#neonGlow)"/>
            <path d="M200,68 C200,74 190,82 188,92 C186,102 192,112 200,112 C208,112 214,102 212,92 C210,82 200,74 200,68" stroke="url(#tubeG2)" stroke-width="3" fill="none" stroke-linecap="round" filter="url(#neonGlow)"/>
            <circle cx="200" cy="116" r="18" fill="url(#chestGlow)" filter="url(#softGlow)">
                <animate attributeName="r" values="15;20;15" dur="2.5s" repeatCount="indefinite"/>
                <animate attributeName="opacity" values="0.6;1;0.6" dur="2.5s" repeatCount="indefinite"/>
            </circle>
            <circle cx="200" cy="116" r="9" fill="none" stroke="#38BDF8" stroke-width="3" filter="url(#neonGlow)"/>
            <circle cx="200" cy="116" r="5" fill="none" stroke="#60A5FA" stroke-width="1.5" opacity="0.6"/>
            <circle cx="200" cy="116" r="2" fill="#93C5FD" opacity="0.8"/>
            <ellipse cx="197" cy="112" rx="3" ry="2" fill="white" opacity="0.2">
                <animate attributeName="opacity" values="0.1;0.3;0.1" dur="2s" repeatCount="indefinite"/>
            </ellipse>
        </svg>
    </div>
    <div class="hero-ai-badge">
        <span>✨</span> MEDICAL AI
    </div>
</div>
"""
components.html(hero_html, height=180, scrolling=False)

# --- TABS ---
tab_main, tab_dashboard = st.tabs(["🩺 Clinical Support", "📊 Dashboard Analytics"])

# ==============================================================================
# TAB 1: CLINICAL SUPPORT
# ==============================================================================
with tab_main:
    col_input, col_results = st.columns([1, 1], gap="medium")

    # ==============================================================================
    # LEFT COLUMN: INPUT PANEL
    # ==============================================================================
    with col_input:
        st.markdown('<div class="panel-header-title panel-title-left"><span>⚙️</span> INPUT PANEL</div>', unsafe_allow_html=True)

        query_data = render_autocomplete_search(st.session_state["current_search_query"], theme=st.session_state.get("theme", "dark"))

        if isinstance(query_data, dict):
            query_text_to_run = str(query_data.get("query", "")).strip()
            st.session_state["current_search_query"] = query_data.get("query", "")
            ask_clicked = bool(query_data.get("submitted", False))
        elif isinstance(query_data, str):
            query_text_to_run = query_data.strip()
            st.session_state["current_search_query"] = query_data
            ask_clicked = False
        else:
            query_text_to_run = ""
            ask_clicked = False

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
                    import datetime
                    st.session_state["query_history"].append({
                        "query": query_text_to_run,
                        "language": selected_language,
                        "confidence": response_obj.get("confidence", "insufficient"),
                        "citations_count": len(response_obj.get("citations", [])),
                        "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
                    })
                except Exception as ex:
                    st.session_state["error_message"] = (
                        "An unexpected error occurred while processing your clinical request. "
                        "Please check terminal/server logs for technical details."
                    )

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

            if confidence == "high":
                badge_html = '<span class="badge badge-high">🛡 HIGH CONFIDENCE</span>'
            elif confidence in ["medium", "low"]:
                badge_html = '<span class="badge badge-medium">⚠ MODERATE CONFIDENCE</span>'
            else:
                badge_html = '<span class="badge badge-insufficient">⚠ INSUFFICIENT EVIDENCE</span>'

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

# ==============================================================================
# TAB 2: DASHBOARD ANALYTICS
# ==============================================================================
with tab_dashboard:
    import pandas as pd

    history = st.session_state.get("query_history", [])

    if not history:
        st.markdown("""
        <div style="text-align:center; padding:60px 20px; color:#94A3B8;">
            <div style="font-size:48px; margin-bottom:16px;">📋</div>
            <div style="font-size:18px; font-weight:600; color:#F8FAFC; margin-bottom:8px;">No Data Yet</div>
            <div>Ask some questions on the Clinical Support tab to see analytics here.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        df = pd.DataFrame(history)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Total Queries</div>
                <div class="stat-number" style="color:#22D3EE;">{len(df)}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            high_count = len(df[df["confidence"] == "high"])
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">High Confidence</div>
                <div class="stat-number" style="color:#22C55E;">{high_count}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            avg_citations = round(df["citations_count"].mean(), 1)
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Avg Citations</div>
                <div class="stat-number" style="color:#A855F7;">{avg_citations}</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            languages_used = df["language"].nunique()
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Languages Used</div>
                <div class="stat-number" style="color:#F59E0B;">{languages_used}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown('<div class="section-title">🎯 Confidence Distribution</div>', unsafe_allow_html=True)
            conf_counts = df["confidence"].value_counts()
            conf_df = pd.DataFrame({"Confidence": conf_counts.index, "Count": conf_counts.values})
            st.bar_chart(conf_df.set_index("Confidence"), color="#22D3EE")

        with chart_col2:
            st.markdown('<div class="section-title">🌐 Language Usage</div>', unsafe_allow_html=True)
            lang_counts = df["language"].value_counts()
            lang_df = pd.DataFrame({"Language": lang_counts.index, "Count": lang_counts.values})
            st.bar_chart(lang_df.set_index("Language"), color="#A855F7")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div class="section-title">📝 Query History</div>', unsafe_allow_html=True)
        display_df = df[["timestamp", "language", "query", "confidence", "citations_count"]].copy()
        display_df.columns = ["Time", "Language", "Question", "Confidence", "Citations"]
        display_df = display_df.iloc[::-1].reset_index(drop=True)
        st.dataframe(display_df, use_container_width=True, hide_index=True)

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
