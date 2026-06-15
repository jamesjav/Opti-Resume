import streamlit as st
from OptiResume.utils import ExtractPDF, CreatePDF
from OptiResume.llm import SendRequest, get_available_providers


def _init_session_state():
    """Initialize session state defaults."""
    if "provider" not in st.session_state:
        providers = get_available_providers()
        st.session_state.provider = providers[0] if providers else "OpenAI"
    if "language" not in st.session_state:
        st.session_state.language = "English"


def _sidebar_settings():
    """Render LLM provider and language settings in the sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("Settings")

    providers = get_available_providers()
    if providers:
        st.session_state.provider = st.sidebar.selectbox(
            "LLM Provider", providers, index=providers.index(st.session_state.get("provider", providers[0]))
        )
    else:
        st.sidebar.warning("No LLM API key configured. Please set up .env file.")

    st.session_state.language = st.sidebar.radio(
        "Output Language", ["English", "Chinese"],
        index=0 if st.session_state.get("language", "English") == "English" else 1
    )

    with st.sidebar.expander("Advanced Options"):
        st.session_state.max_tokens = st.slider("Max Tokens", 500, 4000, 2000, step=100)
        st.session_state.temperature = st.slider("Temperature", 0.0, 1.0, 0.0, step=0.1)


def OptimiseResume():
    st.title("Opti-Resume: AI-Powered Resume Optimization")
    st.markdown("Upload your resume and let AI optimize it for your target role.")

    uploaded_file = st.file_uploader("Upload Your Resume (PDF only)", type=["pdf"])

    if uploaded_file is not None:
        resume_text = ExtractPDF(uploaded_file)
        st.success(f"Resume loaded ({len(resume_text)} characters)")

        if st.button("Optimize Resume", type="primary"):
            with st.spinner("Optimizing your resume..."):
                optimized_text = SendRequest(
                    "Optimisation-Prompt.txt", resume_text,
                    provider=st.session_state.provider,
                    language=st.session_state.language,
                    max_tokens=st.session_state.max_tokens,
                    temperature=st.session_state.temperature,
                )
            if optimized_text.startswith("[Error]"):
                st.error(optimized_text)
            else:
                st.text_area("Optimized Resume", optimized_text, height=300)
                input_filename = f'Artifacts/{uploaded_file.name.split(".")[0]}'
                optimized_filename = CreatePDF(
                    optimized_text, input_filename,
                    language=st.session_state.language,
                )
                if optimized_filename:
                    with open(optimized_filename, "rb") as file:
                        st.download_button(
                            "Download Optimized Resume (PDF)", file,
                            file_name=optimized_filename, mime="application/pdf",
                        )
                else:
                    st.warning("PDF generation failed. You can copy the text above manually.")


def ATSAnalysis():
    st.title("Opti-Resume: ATS Score Analysis")
    st.markdown("Find out how well your resume matches a job description.")

    uploaded_file = st.file_uploader("Upload Your Resume (PDF only)", type=["pdf"])
    job_description = st.text_area("Enter the Job Description", height=200, placeholder="Paste the full job description here...")

    if uploaded_file is not None and job_description:
        if st.button("Analyze ATS Score", type="primary"):
            with st.spinner("Analyzing ATS compatibility..."):
                resume_data = ExtractPDF(uploaded_file)
                req_text = "Resume:\n" + resume_data + "\n\nJob Description:\n" + job_description
                ats_result = SendRequest(
                    "ATS_Check.txt", req_text,
                    provider=st.session_state.provider,
                    language=st.session_state.language,
                    max_tokens=st.session_state.max_tokens,
                    temperature=st.session_state.temperature,
                )
            if ats_result.startswith("[Error]"):
                st.error(ats_result)
            else:
                st.markdown("### ATS Analysis Result")
                st.markdown(ats_result)


def SkillsAnalysis():
    st.title("Opti-Resume: Skills Analysis")
    st.markdown("Extract and categorize the key skills from a job description.")

    job_description = st.text_area("Enter the Job Description", height=200, placeholder="Paste the full job description here...")

    if st.button("Analyze Keywords", type="primary"):
        if job_description:
            with st.spinner("Extracting skills from job description..."):
                analysis_result = SendRequest(
                    "Keyword_Prompt.txt", job_description,
                    provider=st.session_state.provider,
                    language=st.session_state.language,
                    max_tokens=st.session_state.max_tokens,
                    temperature=st.session_state.temperature,
                )
            if analysis_result.startswith("[Error]"):
                st.error(analysis_result)
            else:
                st.subheader("Skills Categorized from Job Description")
                st.markdown(analysis_result)
        else:
            st.error("Please enter a job description to analyze.")


def BulletPointAnalysis():
    st.title("Opti-Resume: Bullet Point Optimization")
    st.markdown("Transform weak bullet points into impactful, quantified achievements.")

    bullet_ = st.text_area("Enter Your Bullet Point", height=100, placeholder="e.g., Managed a team and improved performance")

    if st.button("Optimize Bullet Points", type="primary"):
        if bullet_:
            with st.spinner("Optimizing bullet points..."):
                bullet_analysis = SendRequest(
                    "Bullet_Prompt.txt", bullet_,
                    provider=st.session_state.provider,
                    language=st.session_state.language,
                    max_tokens=st.session_state.max_tokens,
                    temperature=st.session_state.temperature,
                )
            if bullet_analysis.startswith("[Error]"):
                st.error(bullet_analysis)
            else:
                st.markdown("### Optimized Bullet Points")
                st.markdown(bullet_analysis)
        else:
            st.error("Please enter a bullet point to analyze.")


def MetricAnalysis():
    st.title("Opti-Resume: Metric Analysis")
    st.markdown("Get suggestions for quantifiable metrics to strengthen your resume bullets.")

    bullet = st.text_area("Enter Your Bullet Point", height=100, placeholder="Describe what you did and we'll suggest metrics...")

    if st.button("Analyze", type="primary"):
        if bullet:
            with st.spinner("Generating metric suggestions..."):
                metric_result = SendRequest(
                    "Metric_Prompt.txt", bullet,
                    provider=st.session_state.provider,
                    language=st.session_state.language,
                    max_tokens=st.session_state.max_tokens,
                    temperature=st.session_state.temperature,
                )
            if metric_result.startswith("[Error]"):
                st.error(metric_result)
            else:
                st.markdown("### Suggested Metrics")
                st.markdown(metric_result)
        else:
            st.error("Please enter a bullet point to analyze.")


def CoverLetterGenerator():
    st.title("Opti-Resume: Cover Letter Generator")
    st.markdown("Generate a tailored cover letter based on your resume and the job description.")

    uploaded_file = st.file_uploader("Upload Your Resume (PDF only)", type=["pdf"])
    job_description = st.text_area("Enter the Job Description", height=200, placeholder="Paste the full job description here...")

    if uploaded_file is not None and job_description:
        if st.button("Generate Cover Letter", type="primary"):
            with st.spinner("Writing your cover letter..."):
                resume_data = ExtractPDF(uploaded_file)
                req_text = "Resume:\n" + resume_data + "\n\nJob Description:\n" + job_description
                cover_result = SendRequest(
                    "CoverLetter_Prompt.txt", req_text,
                    provider=st.session_state.provider,
                    language=st.session_state.language,
                    max_tokens=st.session_state.max_tokens,
                    temperature=st.session_state.temperature,
                )
            if cover_result.startswith("[Error]"):
                st.error(cover_result)
            else:
                st.markdown("### Your Cover Letter")
                st.markdown(cover_result)
