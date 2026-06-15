import streamlit as st
from OptiResume.main import (
    OptimiseResume, BulletPointAnalysis, SkillsAnalysis,
    ATSAnalysis, MetricAnalysis, CoverLetterGenerator, _init_session_state, _sidebar_settings,
)

# Page Configurations
st.set_page_config(
    page_title="Opti-Resume: AI-Powered Resume Optimizer",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
_init_session_state()

# Sidebar navigation
st.sidebar.title("Opti-Resume")
st.sidebar.caption("AI-Powered Resume Toolkit")

page = st.sidebar.radio(
    "Tools",
    [
        "Resume Optimization",
        "ATS Score Analysis",
        "Bullet-Point Analysis",
        "Skills Analysis",
        "Metric Suggestions",
        "Cover Letter Generator",
    ],
)

# LLM settings in sidebar
_sidebar_settings()

# Load CSS
@st.cache_data
def load_css():
    with open("static/styles.css") as f:
        return f.read()

st.markdown(f"<style>{load_css()}</style>", unsafe_allow_html=True)

# Route to page
if page == "Resume Optimization":
    OptimiseResume()
elif page == "Bullet-Point Analysis":
    BulletPointAnalysis()
elif page == "Skills Analysis":
    SkillsAnalysis()
elif page == "ATS Score Analysis":
    ATSAnalysis()
elif page == "Metric Suggestions":
    MetricAnalysis()
elif page == "Cover Letter Generator":
    CoverLetterGenerator()
