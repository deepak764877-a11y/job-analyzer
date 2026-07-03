import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def analyze_resume(resume_text, jd_text):

    prompt = f"""
You are an ATS Resume Analyzer.

Compare the resume with the job description and return ONLY the response in the exact format below.

FIT_SCORE: 85
MATCHED_SKILLS: Python, Flask, SQL
MISSING_SKILLS: React, Docker

STRENGTHS:
- Point 1
- Point 2
- Point 3

WEAKNESSES:
- Point 1
- Point 2

RED_FLAGS:
- Point 1
- Point 2

RECOMMENDATION:
- Point 1
- Point 2
- Point 3

Rules:
1. FIT_SCORE must be an integer between 0 and 100.
2. MATCHED_SKILLS must be comma separated.
3. MISSING_SKILLS must be comma separated.
4. Use "-" for every bullet point.
5. Do not use Markdown.
6. Do not include code blocks.
7. Do not add explanations.
8. Start the response with FIT_SCORE.
9. End the response after RECOMMENDATION.
10. If any section has no items, write "None".

Resume:
{resume_text}

Job Description:
{jd_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()