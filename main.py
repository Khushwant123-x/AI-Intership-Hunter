import fitz
import re
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from skill_extractor import extract_skills

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily = TavilyClient(api_key=TAVILY_API_KEY)


# 1. PDF TEXT EXTRACTION
def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    text = re.sub(r"\s+", " ", text)
    return text.lower()



# 2. WEB SEARCH INTERNSHIPS (REAL TIME)
def get_internships(query):
    try:
        result = tavily.search(
            query=query,
            search_depth="advanced",
            max_results=10
        )

        jobs = []

        for item in result.get("results", []):
            jobs.append({
                "title": item.get("title", ""),
                "link": item.get("url", ""),
                "description": item.get("content", ""),
                "skills": []
            })

        return jobs

    except Exception as e:
        print("Search error:", e)
        return demo_data()



#FALLBACK DATA
def demo_data():
    return [
        {"title": "Python Developer Intern", "link": "https://example.com", "description": "", "skills": []},
        {"title": "Machine Learning Intern", "link": "https://example.com", "description": "", "skills": []},
        {"title": "Frontend Developer Intern", "link": "https://example.com", "description": "", "skills": []},
    ]


# 3. FILTER ONLY INTERNSHIPS
def is_internship(job):
    text = (job["title"] + job.get("description", "")).lower()
    return "intern" in text or "internship" in text


# 4. MATCHING ENGINE
def match_score(user_skills, job_skills):
    user = set(map(str.lower, user_skills))
    job = set(map(str.lower, job_skills))

    if not user:
        return 0, []

    common = user & job

    score = (len(common) / len(user)) * 100

    return round(score, 2), list(common)

# 5. SEARCH QUERIES
def build_queries():
    return [
        "latest software internship 2026 India remote",
        "fresher AI ML internship 2026 apply",
        "backend developer internship remote 2026",
        "data science internship fresher India 2026",
        "paid internship software engineering 2026"
    ]


# 6. MAIN
def main():

    path = input("Enter PDF path: ")

    # STEP 1: Extract resume text
    text = extract_text_from_pdf(path)

    # STEP 2: Extract skills from resume
    user_skills = extract_skills(text)

    print("\n===== YOUR SKILLS =====")
    print(user_skills)

    # STEP 3: Get internships from web
    jobs = []

    for query in build_queries():
        jobs += get_internships(query)

    # STEP 4: Filter internships only
    jobs = [job for job in jobs if is_internship(job)]

    # STEP 5: Skill matching
    for job in jobs:
        job_skills = extract_skills(job["title"] + " " + job.get("description", ""))
        job["skills"] = job_skills

        score, common = match_score(user_skills, job_skills)

        job["score"] = score
        job["matched_skills"] = common

    # STEP 6: Sort by score
    jobs = sorted(jobs, key=lambda x: x["score"], reverse=True)

    # STEP 7: Show top results
    print("\n===== TOP INTERNSHIPS =====\n")

    for i, job in enumerate(jobs[:5], 1):
        print(f"\n#{i}")
        print("Title:", job["title"])
        print("Score:", job["score"], "%")
        print("Matched Skills:", job["matched_skills"])
        print("Apply Link:", job["link"])
        print("-" * 50)


if __name__ == "__main__":
    main()