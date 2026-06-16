import streamlit as st
import fitz
import re
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from skill_extractor import extract_skills

# -----------------------------
# INIT
# -----------------------------
load_dotenv()
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

st.set_page_config(
    page_title="AI Internship Hunter",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------
# HEADER UI
# -----------------------------
st.title("🚀 AI Internship Hunter")
st.caption("Upload your resume and get AI-matched internships in real time")

# -----------------------------
# PDF TEXT EXTRACTION
# -----------------------------
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()
    text = re.sub(r"\s+", " ", text)
    return text.lower()

# -----------------------------
# WEB SEARCH
# -----------------------------
def get_internships(query):
    try:
        result = tavily.search(
            query=query,
            search_depth="advanced",
            max_results=8
        )

        jobs = []

        for item in result.get("results", []):
            jobs.append({
                "title": item.get("title", ""),
                "link": item.get("url", ""),
                "description": item.get("content", "")
            })

        return jobs

    except Exception as e:
        st.error(f"Search error: {e}")
        return []

# -----------------------------
# FILTER INTERNSHIPS
# -----------------------------
def is_internship(job):
    text = (job["title"] + job["description"]).lower()
    return "intern" in text

# -----------------------------
# MATCHING ENGINE
# -----------------------------
def match_score(user_skills, job_skills):
    user = set(map(str.lower, user_skills))
    job = set(map(str.lower, job_skills))

    if not user:
        return 0, []

    common = user & job
    score = (len(common) / len(user)) * 100

    return round(score, 2), list(common)

# -----------------------------
# SEARCH QUERIES
# -----------------------------
def build_queries():
    return [
        "latest software internship India 2026 remote",
        "AI ML internship fresher 2026",
        "backend developer internship remote",
        "data science internship India 2026",
        "paid internship fresher 2026"
    ]

# -----------------------------
# UI INPUT
# -----------------------------
uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

if uploaded_file:

    # STEP 1: Extract resume text
    with st.spinner("Extracting resume text..."):
        text = extract_text_from_pdf(uploaded_file)
        user_skills = extract_skills(text)

    st.subheader("🧠 Your Skills")
    st.success(", ".join(user_skills))

    # STEP 2: Search button
    if st.button("🚀 Find Internships"):

        jobs = []

        with st.spinner("Searching latest internships on web..."):
            for q in build_queries():
                jobs += get_internships(q)

        # STEP 3: filter
        jobs = [j for j in jobs if is_internship(j)]

        # STEP 4: scoring
        for job in jobs:
            job_skills = extract_skills(job["title"] + " " + job["description"])

            score, common = match_score(user_skills, job_skills)

            job["score"] = score
            job["common"] = common

        jobs = sorted(jobs, key=lambda x: x["score"], reverse=True)

        # STEP 5: UI OUTPUT
        st.subheader("🏆 Top Matching Internships")

        if not jobs:
            st.warning("No internships found. Try again later.")
        else:

            for i, job in enumerate(jobs[:10], 1):

                score = job.get("score", 0)
                common = job.get("common", [])

                if score >= 60:
                    status = "🟢 High Match"
                elif score >= 30:
                    status = "🟡 Medium Match"
                else:
                    status = "🔴 Low Match"

                with st.container():

                    col1, col2 = st.columns([4, 1])

                    with col1:
                        st.markdown(f"### {i}. {job['title']}")
                        st.write("🧠 Skills:", ", ".join(common) if common else "None")
                        st.write(f"🎯 Score: {score}% | {status}")

                    with col2:
                        st.link_button("🚀 Apply", job["link"])

                    st.divider()

else:
    st.info("👆 Upload your resume to start finding internships")