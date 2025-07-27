import streamlit as st
from modules.resume_parser import extract_resume_data  # ✅ Unified function
from modules.job_matcher import match_job_description
from modules.verifier import validate_links             # ✅ Just validate now
from modules.report_generator import generate_output_report
import os

# ---------------------------
# App Configuration
# ---------------------------
st.set_page_config(page_title="LegitAI - Resume Screener", layout="centered")
st.title("🧠 LegitAI: Smart Resume Screener & Certificate Verifier 🚀")
st.markdown("Upload your resume, enter a job description, and get smart insights including hyperlink verification and JD match score.")

# ---------------------------
# Session State Initialization
# ---------------------------
if 'similarity_score' not in st.session_state:
    st.session_state.similarity_score = None
if 'resume_filename' not in st.session_state:
    st.session_state.resume_filename = None

# ---------------------------
# File Upload
# ---------------------------
uploaded_file = st.file_uploader("📄 Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    st.session_state.resume_filename = uploaded_file.name

    # ✅ Extract resume text + hyperlinks
    resume_text, raw_links = extract_resume_data(uploaded_file)

    # ✅ Validate the extracted links
    links = validate_links(raw_links)

    # ---------------------------
    # Hyperlink Validation
    # ---------------------------
    st.subheader("🔗 Hyperlink Validation")
    if links:
        st.markdown("Below are the hyperlinks found in your resume and their status:")
        for link, is_valid in links:
            status = "✅ Valid" if is_valid else "❌ Invalid"
            st.markdown(f"- [{link}]({link}) — **{status}**")
    else:
        st.warning("⚠️ No hyperlinks found in the uploaded resume.")

    # ---------------------------
    # Job Description Matching
    # ---------------------------
    st.subheader("📌 Enter Job Description")
    job_description = st.text_area("Paste the job description below:", height=200)

    if st.button("🔍 Match Resume with JD"):
        if job_description.strip() == "":
            st.warning("⚠️ Please enter a valid job description before proceeding.")
        else:
            similarity = match_job_description(resume_text, job_description)
            st.session_state.similarity_score = similarity
            st.success(f"🧠 Resume-JD Similarity Score: **{similarity:.2f}%**")
            if similarity > 70:
                st.info("✅ Strong Match!")
            elif similarity > 40:
                st.warning("⚠️ Partial Match.")
            else:
                st.error("❌ Weak Match.")

    # ---------------------------
    # Report Generation
    # ---------------------------
    if st.button("📥 Generate Analysis Report"):
        if st.session_state.similarity_score is not None:
            output_path = generate_output_report(
                resume_text=resume_text,
                resume_filename=st.session_state.resume_filename,
                links=links,
                similarity_score=st.session_state.similarity_score
            )
            st.success("📄 Report Generated Successfully!")
            st.markdown(f"[📂 Click to Open Report]({output_path})")
            with open(output_path, "rb") as f:
                st.download_button("⬇️ Download Report", f, file_name=os.path.basename(output_path))
        else:
            st.warning("⚠️ Match your resume with a JD before generating the report.")
else:
    st.info("📤 Please upload a resume file to begin.")
