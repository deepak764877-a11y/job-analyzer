import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_resume(resume_text, jd_text):
   prompt = f"""
Compare this resume with the job description.

FIT_SCORE: (integer 0-100 only, example: 78)
MATCHED_SKILLS: (comma separated)
MISSING_SKILLS: (comma separated)
STRENGTHS: (bullet points)
WEAKNESSES: (bullet points)
RED_FLAGS: (bullet points)
RECOMMENDATION: (bullet points)

No markdown. No extra text. FIT_SCORE number only.

Resume:
{resume_text}

Job Description:
{jd_text}
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"