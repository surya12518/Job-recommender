# src/resume_parser.py
import pdfplumber, re
def extract_text_from_pdf(path):
    with pdfplumber.open(path) as pdf:
        pages = [p.extract_text() or "" for p in pdf.pages]
    return "\n".join(pages)

def parse_basic_resume(text):
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    phone = re.search(r'(\+?\d[\d\-\s]{7,}\d)', text)
    # simple skills extraction: check for keywords list
    skill_keywords = ['python','sql','pandas','machine learning','tableau','excel']
    found = [k for k in skill_keywords if k.lower() in text.lower()]
    # years experience (simple)
    yexp = re.search(r'(\d+)\s+years?', text.lower())
    return {
        'email': email.group(0) if email else None,
        'phone': phone.group(0) if phone else None,
        'skills': found,
        'years_experience': int(yexp.group(1)) if yexp else None
    }
