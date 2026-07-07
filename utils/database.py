import sqlite3
import json
import os

DB_FOLDER = "database"
DB_PATH = os.path.join(DB_FOLDER, "jobfit.db")

os.makedirs(DB_FOLDER, exist_ok=True)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            ats_score INTEGER,
            matched_skills TEXT,
            missing_skills TEXT,
            strengths TEXT,
            weaknesses TEXT,
            red_flags TEXT,
            recommendations TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_report(filename, result):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reports (
            filename,
            ats_score,
            matched_skills,
            missing_skills,
            strengths,
            weaknesses,
            red_flags,
            recommendations
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        filename,
        result.get("ats_score", 0),
        json.dumps(result.get("matched_skills", [])),
        json.dumps(result.get("missing_skills", [])),
        json.dumps(result.get("strengths", [])),
        json.dumps(result.get("weaknesses", [])),
        json.dumps(result.get("red_flags", [])),
        json.dumps(result.get("recommendations", []))
    ))

    conn.commit()
    conn.close()


def get_reports():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM reports
        ORDER BY created_at DESC
    """)

    reports = cursor.fetchall()
    conn.close()

    return reports


def delete_report(report_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM reports WHERE id = ?",
        (report_id,)
    )

    conn.commit()
    conn.close()