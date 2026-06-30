import os
from flask import Flask, render_template, request, redirect, flash, url_for
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from utils.pdf_parser import extract_text_from_pdf
from utils.gemini_analyzer import analyze_resume
from utils.text_cleaner import parse_gemini_response

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "jobfit-secret")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("resume")
    jd_text = request.form.get("jd", "")

    if not file or file.filename == "":
        flash("Please upload a resume PDF", "danger")
        return redirect(url_for("home"))

    if not file.filename.lower().endswith(".pdf"):
        flash("Only PDF files are allowed.", "danger")
        return redirect(url_for("home"))

    if not jd_text.strip():
        flash("Please paste a Job Description.", "danger")
        return redirect(url_for("home"))

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    try:
        resume_text = extract_text_from_pdf(file_path)
        raw_result = analyze_resume(resume_text, jd_text)
        parsed_result = parse_gemini_response(raw_result)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    return render_template("result.html", result=parsed_result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)