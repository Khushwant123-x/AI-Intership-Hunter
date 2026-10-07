import fitz
import re
import requests
from skill_extractor import extract_skills


# -----------------------------
# 1. PDF TEXT EXTRACTION
# -----------------------------
def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    text = re.sub(r"\s+", " ", text)
    return text.lower()


# -----------------------------
# 2. GET INTERNSHIPS (API BASED - FIXED)
# -----------------------------
def get_internships():
    url = "https://remotive.com/api/remote-jobs"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        jobs = []

        for job in data["jobs"][:20]:
            jobs.append({
                "title": job["title"],
                "link": job["url"],
                "skills": []
            })

        return jobs

    except:
        return demo_data()


# -----------------------------
# FALLBACK DATA (SAFE)
# -----------------------------
def demo_data():
    return [
        {"title": "Python Developer Intern", "link": "https://remotive.com", "skills": []},
        {"title": "Machine Learning Intern", "link": "https://remotive.com", "skills": []},
        {"title": "Frontend Developer Intern", "link": "https://remotive.com", "skills": []},
        {"title": "Data Science Intern", "link": "https://remotive.com", "skills": []},
    ]


# -----------------------------
# 3. SKILL GUESSING
# -----------------------------
def guess_skills(text):
    text = text.lower()
    skills = []

    skill_map = {
        "python": ["python"],
        "frontend": ["html5", "css3", "javascript"],
        "react": ["react.js"],
        "backend": ["django", "flask"],
        "data": ["machine learning", "pandas", "numpy"],
        "ai": ["machine learning"],
        "sql": ["mysql", "postgresql"]
    }

    for key, values in skill_map.items():
        if key in text:
            skills += values

    return list(set(skills))


# -----------------------------
# 4. MATCHING ENGINE
# -----------------------------
def match_score(user_skills, job_skills):
    user = set([s.lower() for s in user_skills])
    job = set([s.lower() for s in job_skills])

    if not job:
        return 0, []

    common = user.intersection(job)

    # realistic scoring
    score = (len(common) / len(user)) * 100

    return round(score, 2), list(common)


# -----------------------------
# 5. MAIN
# -----------------------------
def main():

    path = input("Enter PDF path: ")
    text = extract_text_from_pdf(path)

    user_skills = extract_skills(text)

    print("\n===== YOUR SKILLS =====")
    print(user_skills)

    jobs = get_internships()

    for job in jobs:
        job_text = job["title"] + " " + job.get("description", "")
        job["skills"] = guess_skills(job_text)

        score, common = match_score(user_skills, job["skills"])

        job["score"] = score
        job["matched_skills"] = common

    jobs = sorted(jobs, key=lambda x: x["score"], reverse=True)

    print("\n===== TOP 5 INTERNSHIPS =====\n")

    for i, job in enumerate(jobs[:5], 1):
        print(f"\n#{i}")
        print("Title:", job["title"])
        print("Score:", job["score"], "%")
        print("Matched Skills:", job["matched_skills"])
        print("Apply Link:", job["link"])
        print("-" * 50)


if __name__ == "__main__":
    main()

