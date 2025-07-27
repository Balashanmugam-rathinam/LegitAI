from PyPDF2 import PdfReader
import docx
import fitz  # PyMuPDF
import re

def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"[ERROR] PDF text extraction failed: {e}")
        return ""

def extract_text_from_docx(uploaded_file):
    try:
        doc = docx.Document(uploaded_file)
        full_text = "\n".join([para.text for para in doc.paragraphs])
        return full_text.strip()
    except Exception as e:
        print(f"[ERROR] DOCX text extraction failed: {e}")
        return ""

def extract_links_from_text(text):
    pattern = r'(https?://[^\s\)\]\}\"\']+)'
    return re.findall(pattern, text)

def extract_embedded_links_from_pdf(uploaded_file):
    links = set()
    try:
        uploaded_file.seek(0)
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            for link in page.get_links():
                uri = link.get("uri")
                if uri:
                    links.add(uri)
        doc.close()
    except Exception as e:
        print(f"[ERROR] Embedded link extraction failed: {e}")
    return list(links)

def extract_resume_data(uploaded_file):
    resume_text = ""
    links = []

    if uploaded_file.type == "application/pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
        embedded_links = extract_embedded_links_from_pdf(uploaded_file)
        text_links = extract_links_from_text(resume_text)
        links = list(set(embedded_links + text_links))

    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resume_text = extract_text_from_docx(uploaded_file)
        links = extract_links_from_text(resume_text)

    return resume_text, links
