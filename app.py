import os
import re
import fitz
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from tavily import TavilyClient
from skill_extractor import extract_skills

# Load env variables
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
app = Flask(__name__, static_folder=STATIC_DIR, static_url_path='/static')
CORS(app)  # Enable Cross-Origin Resource Sharing

# Initialize Tavily
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily = None
if TAVILY_API_KEY:
    try:
        tavily = TavilyClient(api_key=TAVILY_API_KEY)
    except Exception as e:
        print(f"Error initializing Tavily Client: {e}")


# --------------------------------------------------------------------------
# HELPERS
# --------------------------------------------------------------------------
def extract_text_from_pdf(file_obj):
    """Extracts clean text from a PDF file."""
    try:
        file_obj.seek(0)
        pdf_bytes = file_obj.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        text = re.sub(r"\s+", " ", text)
        return text.strip().lower()
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return ""


def get_tavily_internships(query):
    """Executes a web search for internship listings using Tavily API."""
    if not tavily:
        return demo_data()
    
    try:
        result = tavily.search(
            query=query,
            search_depth="advanced",
            max_results=6
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
        print(f"Tavily search error for query '{query}': {e}")
        return []


def demo_data():
    """Fallback mock internships if search fails or is unauthorized."""
    return [
        {
            "title": "Python Backend Developer Intern",
            "link": "https://remotive.com",
            "description": "Looking for a Python Developer Intern experienced with Django, Flask, or FastAPI, SQL databases (MySQL/PostgreSQL), and REST API design."
        },
        {
            "title": "React Frontend Developer Intern",
            "link": "https://remotive.com",
            "description": "Seeking an advanced Frontend Intern with strong skills in React.js, JavaScript, HTML5, CSS3, Tailwind CSS, and Git/GitHub."
        },
        {
            "title": "Machine Learning & AI Intern",
            "link": "https://remotive.com",
            "description": "Join our AI research team as an ML intern. Ideal skills: Python, Scikit-learn, TensorFlow, PyTorch, Pandas, and Model Evaluation."
        },
        {
            "title": "Full Stack Developer Intern (Node & React)",
            "link": "https://remotive.com",
            "description": "Looking for a developer to build web apps using Node.js, Express.js, React.js, and MongoDB. Experience with REST APIs required."
        },
        {
            "title": "Data Analyst Intern",
            "link": "https://remotive.com",
            "description": "Analyze datasets and build dashboards using NumPy, Pandas, Matplotlib, and SQL. Python programming required."
        }
    ]


def build_dynamic_queries(user_skills):
    """Dynamically builds targeted search queries based on extracted user skills."""
    # Base general queries
    queries = [
        "latest software developer internship India 2026 remote",
        "paid frontend backend engineering internship remote 2026"
    ]
    
    # Add skill-specific queries for the top 3 skills
    meaningful_skills = [s for s in user_skills if s.lower() not in ["problem solving", "communication", "teamwork", "time management"]]
    
    for skill in meaningful_skills[:3]:
        queries.append(f"latest {skill} internship remote 2026")
        
    return queries[:4]  # Cap at 4 queries to optimize API usage rate limit


def is_internship(job):
    """Filters search results to ensure they represent internship listings."""
    text = (job["title"] + " " + job.get("description", "")).lower()
    return "intern" in text or "internship" in text


def match_score(user_skills, job_skills):
    """Computes a realistic percentage match score based on job requirements."""
    user = set(map(str.lower, user_skills))
    job = set(map(str.lower, job_skills))

    if not job:
        return 0, []

    common = user & job
    # Score is the percentage of job's required skills that the candidate has
    score = (len(common) / len(job)) * 100

    return round(score, 2), list(common)


# --------------------------------------------------------------------------
# ROUTES
# --------------------------------------------------------------------------
@app.route('/')
def serve_index():
    """Serves the main single-page dashboard application."""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/extract', methods=['POST'])
def api_extract_skills():
    """Accepts a PDF resume, parses text, and returns extracted skill tags."""
    if 'resume' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
        
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Only PDF files are supported"}), 400

    # Extract text from file stream
    text = extract_text_from_pdf(file.stream)
    if not text:
        return jsonify({"error": "Unable to extract text from PDF"}), 422

    # Parse skills
    extracted = extract_skills(text)
    return jsonify({"skills": extracted})


@app.route('/api/search', methods=['POST'])
def api_search_internships():
    """Crawl web for internships, filter, score and rank them against skills."""
    data = request.get_json() or {}
    skills = data.get("skills", [])
    
    if not skills:
        return jsonify({"error": "No skills provided for matching"}), 400

    # Clean and construct a single query with the top skills to save Tavily credits
    meaningful_skills = [s for s in skills if s.lower() not in ["problem solving", "communication", "teamwork", "time management", "analytical thinking", "project management"]]
    skills_query_part = " ".join(meaningful_skills[:4])
    query = f"latest remote tech internships 2026 India paid fresher {skills_query_part}"
    
    # Run a single Tavily search request with max_results=5 to save credits and limit output
    raw_jobs = []
    if tavily:
        try:
            result = tavily.search(
                query=query,
                search_depth="advanced",
                max_results=5
            )
            for item in result.get("results", []):
                raw_jobs.append({
                    "title": item.get("title", ""),
                    "link": item.get("url", ""),
                    "description": item.get("content", "")
                })
        except Exception as e:
            print(f"Tavily search error: {e}")
            raw_jobs = demo_data()
    else:
        raw_jobs = demo_data()

    # Filter out duplicate URLs/titles and non-internships
    seen_links = set()
    jobs = []
    for job in raw_jobs:
        link = job.get("link")
        if link in seen_links:
            continue
        if is_internship(job):
            seen_links.add(link)
            jobs.append(job)

    # If Tavily returned nothing, or key wasn't active, fallback to demo data
    if not jobs:
        print("No real-time jobs found or API inactive. Loading fallback demo data...")
        jobs = [j for j in demo_data() if is_internship(j)]

    # Score and annotate job matches
    scored_jobs = []
    for job in jobs:
        # Extract skills required by this specific internship
        job_content = job["title"] + " " + job.get("description", "")
        job_skills = extract_skills(job_content)
        job["skills"] = job_skills

        score, common = match_score(skills, job_skills)
        job["score"] = score
        job["matched_skills"] = common

        scored_jobs.append(job)

    # Sort from highest to lowest score
    scored_jobs = sorted(scored_jobs, key=lambda x: x["score"], reverse=True)

    return jsonify({
        "jobs": scored_jobs,
        "queries": [query]
    })


# Start Server
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting server on http://127.0.0.1:{port} ...")
    app.run(host='0.0.0.0', port=port, debug=True)