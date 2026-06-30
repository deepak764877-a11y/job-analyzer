def parse_gemini_response(raw_text):
    sections = {
        "fit_score": "",
        "matched_skills": [],
        "missing_skills": [],
        "strengths": [],
        "weaknesses": [],
        "red_flags": [],
        "recommendation": []
    }

    current_key = None
    lines = raw_text.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.upper().startswith("FIT_SCORE"):
            current_key = "fit_score"
            if ":" in line:
                sections["fit_score"] = line.split(":", 1)[1].strip()
        elif line.upper().startswith("MATCHED_SKILLS"):
            current_key = "matched_skills"
            if ":" in line:
                sections["matched_skills"] = line.split(":", 1)[1].strip()
        elif line.upper().startswith("MISSING_SKILLS"):
            current_key = "missing_skills"
            if ":" in line:
                sections["missing_skills"] = line.split(":", 1)[1].strip()
        elif line.upper().startswith("STRENGTHS"):
            current_key = "strengths"
        elif line.upper().startswith("WEAKNESSES"):
            current_key = "weaknesses"
        elif line.upper().startswith("RED_FLAGS"):
            current_key = "red_flags"
        elif line.upper().startswith("RECOMMENDATION"):
            current_key = "recommendation"
        else:
            if current_key in ["strengths", "weaknesses", "red_flags", "recommendation"]:
                sections[current_key].append(line.lstrip("-• "))

    if isinstance(sections["matched_skills"], str):
        sections["matched_skills"] = [s.strip() for s in sections["matched_skills"].split(",") if s.strip()]
    if isinstance(sections["missing_skills"], str):
        sections["missing_skills"] = [s.strip() for s in sections["missing_skills"].split(",") if s.strip()]

    try:
        sections["fit_score"] = int(sections["fit_score"])
    except (ValueError, TypeError):
        sections["fit_score"] = 0

    return sections