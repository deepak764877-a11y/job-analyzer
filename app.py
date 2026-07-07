import os
from flask import Flask, render_template, request, redirect, flash, url_for
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

from utils.pdf_parser import extract_text_from_pdf
from utils.gemini_analyzer import analyze_resume
from utils.text_cleaner import parse_gemini_response
from utils.database import init_db, save_report

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "jobfit-secret")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files.get("resume")
    jd_text = request.form.get("jd", "")

    if not file or file.filename == "":
        flash("Please upload a Resume PDF.", "danger")
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

        save_report(filename, parsed_result)

        return render_template(
            "result.html",
            result=parsed_result
        )

    except Exception as e:
        print(e)
        flash("Something went wrong while analyzing the resume.", "danger")
        return redirect(url_for("home"))

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@app.errorhandler(413)
def file_too_large(e):
    flash("File too large. Maximum size is 5 MB.", "danger")
    return redirect(url_for("home"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)