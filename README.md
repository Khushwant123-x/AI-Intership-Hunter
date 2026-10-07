# 🚀 AI Internship Hunter

An AI-powered web app and real-time matching engine that extracts technical skills from candidate resumes (PDF format) and finds relevant internship opportunities using real-time web search and algorithmic matching.

---

## ✨ Features

- 📄 **Resume Parsing** — Upload your PDF resume and extract text automatically using PyMuPDF (`fitz`).
- 🧠 **Skill Extraction Engine** — Identifies 50+ key technical skills, frameworks, and tools.
- 🌐 **Live Web Search** — Queries live web listings via the Tavily Search API with dynamic queries.
- 🎯 **Smart Matching Engine** — Calculates realistic percentage match scores based on job requirements.
- 🎨 **Glassmorphism UI** — Dark neon dashboard with drag-and-drop resume upload, interactive skill chips, and direct application links.

---

## 🖥️ Demo

https://github.com/user-attachments/assets/2854003b-4709-4171-bc08-2599d40ea0bb

> _Upload your resume → Extract skills → Find matching internships in seconds_

---

## 🏗️ Architecture

<img width="1536" height="1024" alt="ai-internship-hunter" src="https://github.com/user-attachments/assets/92d07a5b-2a0f-474e-8871-81464a2f3e84" />

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend & API** | Python 3.10+, Flask, Flask-CORS |
| **PDF Parsing** | [PyMuPDF](https://pymupdf.readthedocs.io/) (`fitz`) |
| **Web Search** | [Tavily API](https://tavily.com/) |
| **Skill Extraction** | Curated technical taxonomy matcher (`skill_extractor.py`) |
| **Frontend** | HTML5, Vanilla CSS3 (Glassmorphism & Neon accents), Vanilla JavaScript |
| **Config** | `python-dotenv` |

---

## 📦 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Khushwant123-x/AI-Intership-Hunter.git
cd AI-Intership-Hunter
```

### 2. Set Up Virtual Environment

```bash
python -m venv .venv

# Windows
.\.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and set your Tavily API key:

```bash
cp .env.example .env
```

In `.env`:
```env
TAVILY_API_KEY=your_tavily_api_key_here
```

Get your free Tavily search API key at [tavily.com](https://tavily.com).

---

## 🚀 Running the App

```bash
python app.py
```

Then open your browser at:
```
http://127.0.0.1:5000
```

1. Upload your resume as a PDF via the drag-and-drop zone.
2. View and edit your extracted skills in real time.
3. Click **🚀 Find Internships**.
4. Browse ranked matches with match percentage scores and apply directly!

---

## 📁 Project Structure

```text
AI_Intership_Hunter/
├── app.py                 # Flask server & REST API endpoints (/api/extract, /api/search)
├── main.py                # Standalone CLI / matching script
├── skill_extractor.py     # Skill taxonomy definition & parsing logic
├── static/
│   ├── index.html         # Main single-page application dashboard
│   ├── style.css          # Glassmorphism styling and responsive layout
│   └── app.js             # Drag & drop upload, dynamic skill tags & cards rendering
├── .env.example           # Environment variable template
├── .gitignore             # Git ignore patterns
└── requirements.txt       # Python dependencies
```

---

## ⚠️ Notes & Limitations

- Internship results depend on Tavily search availability and remaining API credits.
- Only PDF resumes are supported.
- Never commit your `.env` file containing your secret API keys (it is protected by `.gitignore`).

---

## 📄 License

This project is licensed under the MIT License.
