import streamlit as st
import os
from PyPDF2 import PdfReader
import docx

# Custom module imports
from modules.resume_parser import extract_text_from_pdf, extract_text_from_docx
from modules.job_matcher import match_job_description
from modules.verifier import extract_and_validate_links
from modules.report_generator import generate_output_report

# ---------------------------
# Session State Initialization
# ---------------------------
# This ensures we keep track of similarity score and resume filename across interactions
if 'similarity_score' not in st.session_state:
    st.session_state.similarity_score = None

if 'resume_filename' not in st.session_state:
    st.session_state.resume_filename = None

# ---------------------------
# App Title
# ---------------------------
st.title("🧠 LegitAI: Smart Resume Screener & Certificate Verifier 🚀")
st.markdown("Upload your resume, enter a job description, and get smart insights including hyperlink verification and JD match score.")

# ---------------------------
# Resume File Upload Section
# ---------------------------
uploaded_file = st.file_uploader("📄 Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    # Save resume filename to session state
    st.session_state.resume_filename = uploaded_file.name

    # -------------
    # Extract Text
    # -------------
    # Use the appropriate function based on file type
    if uploaded_file.type == "application/pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resume_text = extract_text_from_docx(uploaded_file)
    else:
        st.error("❌ Unsupported file format.")
        resume_text = ""

    # ---------------------------
    # Hyperlink Validation Section
    # ---------------------------
    st.subheader("🔗 Hyperlink Validation")
    links = extract_and_validate_links(resume_text)

    if links:
        st.markdown("Below are the hyperlinks found in your resume and their status:")
        for link, is_valid in links:
            if is_valid:
                st.write(f"✅ **{link}** - Valid")
            else:
                st.write(f"❌ **{link}** - Invalid")
    else:
        st.warning("⚠️ No hyperlinks found in the uploaded resume.")

    # ---------------------------
    # Job Description Input Area
    # ---------------------------
    st.subheader("📌 Enter Job Description")
    job_description = st.text_area(
        label="Paste the job description below. The system will compare it with your resume.",
        height=200
    )

    # ---------------------------
    # Resume to JD Matching Button
    # ---------------------------
    if st.button("🔍 Match Resume with JD"):
        if job_description.strip() == "":
            st.warning("⚠️ Please enter a valid job description before proceeding.")
        else:
            similarity = match_job_description(resume_text, job_description)
            st.session_state.similarity_score = similarity

            # Display result
            st.success(f"🧠 Resume-JD Similarity Score: **{similarity:.2f}%**")
            if similarity > 70:
                st.info("✅ Strong Match! Your resume aligns well with the job description.")
            elif 40 <= similarity <= 70:
                st.warning("⚠️ Partial Match! Consider tailoring your resume further.")
            else:
                st.error("❌ Weak Match. The resume content doesn't align well with the job description.")

    # ---------------------------
    # Generate Output Report
    # ---------------------------
    if st.button("📥 Generate Analysis Report"):
        if st.session_state.similarity_score is not None:
            output_path = generate_output_report(
                resume_text=resume_text,
                resume_filename=st.session_state.resume_filename,
                links=links,
                similarity_score=st.session_state.similarity_score
            )

            # Output success message with generated file path
            st.success(f"📄 Analysis Report Generated Successfully!")
            st.markdown(f"👉 [Click here to open report]({output_path})")

        else:
            st.warning("⚠️ Please match your resume with a job description before generating the report.")

else:
    st.info("📤 Please upload a resume file in PDF or DOCX format to proceed.")
