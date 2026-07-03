import re


def parse_gemini_response(raw_text):
    sections = {
        "fit_score": 0,
        "matched_skills": [],
        "missing_skills": [],
        "strengths": [],
        "weaknesses": [],
        "red_flags": [],
        "recommendation": []
    }

    current_key = None

    for line in raw_text.splitlines():

        line = line.strip()

        if not line:
            continue

        upper = line.upper()

        if upper.startswith("FIT_SCORE") or upper.startswith("FIT SCORE"):
            current_key = "fit_score"

            match = re.search(r"\d+", line)
            if match:
                sections["fit_score"] = int(match.group())

        elif upper.startswith("MATCHED_SKILLS") or upper.startswith("MATCHED SKILLS"):
            current_key = "matched_skills"

            if ":" in line:
                skills = line.split(":", 1)[1]
                sections["matched_skills"].extend(
                    s.strip() for s in skills.split(",") if s.strip()
                )

        elif upper.startswith("MISSING_SKILLS") or upper.startswith("MISSING SKILLS"):
            current_key = "missing_skills"

            if ":" in line:
                skills = line.split(":", 1)[1]
                sections["missing_skills"].extend(
                    s.strip() for s in skills.split(",") if s.strip()
                )

        elif upper.startswith("STRENGTHS"):
            current_key = "strengths"

        elif upper.startswith("WEAKNESSES"):
            current_key = "weaknesses"

        elif upper.startswith("RED_FLAGS") or upper.startswith("RED FLAGS"):
            current_key = "red_flags"

        elif upper.startswith("RECOMMENDATION"):
            current_key = "recommendation"

        else:

            item = line.lstrip("-•* ").strip()

            if item and current_key in sections and isinstance(sections[current_key], list):
                sections[current_key].append(item)

    return sections