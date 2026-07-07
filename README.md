# JobFit Analyzer
I built this project because applying for jobs often feels like guessing.
You never know whether your resume actually matches the job requirements until you apply.
This tool compares your resume with any job description using Gemini AI and shows where you stand before applying.
## What it does
- Gives an ATS Match Score (0-100)
- Shows matched and missing skills
- Highlights resume strengths and weaknesses
- Flags suspicious job requirements
- Gives personalized learning recommendations
- Interactive speedometer gauge
- Download analysis as PDF
## Tech used
Python, Flask, Gemini API, pdfplumber, SQLite, Bootstrap 5, Chart.js
## Run locally
```bash
git clone https://github.com/deepak764877-a11y/job-analyzer.git
cd job-analyzer
pip install -r requirements.txt
```
Create `.env` file:
```
GEMINI_API_KEY=your_key_here
SECRET_KEY=any_secret
```
Run the application:
```bash
python app.py
```
Open:
```
http://127.0.0.1:5000
```
## Note
Works best with text-based PDFs.
Scanned resumes may give inconsistent results.
## Live Demo
Coming Soon