import os
import pdfplumber
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text
resume_text = extract_text_from_pdf("uploads/resume.pdf")

jd_text = """
We are looking for a Python Developer with experience in:
- Flask or Django
- REST APIs
- SQL databases
- Git version control
"""

prompt = f"""
Compare this resume with the job description.

FIT SCORE:
MATCHED SKILLS:
MISSING SKILLS:
STRENGTHS:
WEAKNESSES:
RED FLAGS IN JD:
RECOMMENDATION:

Resume:
{resume_text}

Job Description:
{jd_text}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print(response.text)