# LegitAI: Smart Resume Screener & Certificate Verifier 🚀

LegitAI is an AI-powered tool designed to automate resume screening, validate certificate hyperlinks (even from Canva-designed resumes), and match candidate resumes with job descriptions using semantic similarity.

---

## 🔍 Features

✅ **Resume Upload & Parsing**  
✅ **Hyperlink Extraction & Broken Link Detection**  
✅ **Job Description Matching with Similarity Score**  
✅ **Streamlit Web App Interface**  
✅ **Supports Resumes from PDFs (including Canva designs)**  
✅ **Modular & Scalable Project Structure**  
✅ **One-click Report Export in .txt**  
✅ **Error Handling for Broken PDFs and Invalid URLs**  
✅ **Works Offline (after first install)**

---

## 📂 Project Structure

```
legitAI/
│
├── app.py               # Streamlit UI
├── resume_parser.py     # Extracts resume text + links
├── verifier.py          # Validates links (HTTP status)
├── job_matcher.py       # JD vs Resume matching logic
├── sample_data/
│   ├── sample_resume.pdf
│   └── sample_jd.txt
├── reports/
│   └── broken_links_report.txt
├── requirements.txt
└── README.md
```

---

## 🧠 How It Works

1. **Upload Resume (.pdf or .docx)**  
   - Text & hyperlinks are extracted using `PyMuPDF` or `python-docx`.
   - Hyperlinks (especially certification links) are collected for validation.

2. **Paste Job Description**  
   - JD is compared to resume content using `SentenceTransformer` (e.g., `all-MiniLM-L6-v2`).
   - Semantic similarity score is calculated.

3. **Result Display**  
   - ✅ Valid & ❌ Broken links are displayed.
   - JD matching score with pass/fail badge.
   - Option to download .txt report.

---

## ⚙️ Setup Instructions

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/legitAI.git
cd legitAI

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

---

## 🧪 Sample Output

```
=== Resume Screening Report ===

Resume File: John_Doe_Resume.pdf

Hyperlink Validation:
- https://linkedin.com/in/johndoe - ✅ Valid
- https://github.com/johndoe - ✅ Valid
- https://myportfolio.com - ❌ Invalid

Similarity Score: 82.50%
✅ This resume is a strong match for the provided job description.

Thank you for using Smart Resume Screener!
```

---

## 👥 Authors

- Balashanmugam – [Your LinkedIn/GitHub URL here]

---

## 🏁 Future Improvements

- Export reports in PDF/HTML format  
- OCR support for scanned PDF resumes  
- UI enhancements with job keyword heatmaps  
- Multi-resume batch analysis  

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.