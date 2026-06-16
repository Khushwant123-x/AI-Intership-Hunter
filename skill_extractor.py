SKILLS = [
    "Python", "Java", "C", "C++", "JavaScript", "SQL",
    "HTML5", "CSS3", "React.js", "Streamlit", "Tailwind CSS", "Bootstrap",
    "FastAPI", "Flask", "Django", "REST APIs", "Node.js", "Express.js",
    "MySQL", "PostgreSQL", "SQLite", "MongoDB",
    "Machine Learning", "Deep Learning", "Natural Language Processing (NLP)",
    "Computer Vision", "Generative AI", "Retrieval Augmented Generation (RAG)",
    "Prompt Engineering", "Model Evaluation",
    "LangChain", "Hugging Face", "Transformers", "Scikit-learn",
    "TensorFlow", "PyTorch", "OpenCV", "NumPy", "Pandas", "Matplotlib",
    "OpenAI API", "Ollama", "FAISS", "ChromaDB", "Sentence Transformers",
    "Data Cleaning", "Data Analysis", "ETL Pipelines", "Web Scraping",
    "PaddleOCR", "EasyOCR", "Tesseract OCR", "PDF Processing",
    "Git", "GitHub", "Docker", "Linux", "CI/CD", "Vercel", "Render",
    "Hugging Face Spaces",
    "AWS Basics", "Google Cloud Basics",
    "OOP", "Data Structures & Algorithms", "System Design",
    "API Development", "Debugging", "Testing",
    "VS Code", "Postman", "Jupyter Notebook", "Figma",
    "Problem Solving", "Communication", "Teamwork",
    "Time Management", "Analytical Thinking", "Project Management"
]

def extract_skills(text):
    extracted_skills = []
    for skill in SKILLS:
        if skill.lower() in text.lower():
            extracted_skills.append(skill)
    return extracted_skills