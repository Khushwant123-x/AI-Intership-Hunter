# 🚀 AI Internship Hunter

An AI-powered web app that analyzes your resume and finds the most relevant internships in real time using web search and skill matching.

---

## ✨ Features

- 📄 **Resume Parsing** — Upload your PDF resume and extract text automatically
- 🧠 **Skill Extraction** — Identifies your key skills using a custom NLP extractor
- 🌐 **Live Web Search** — Searches the web for the latest internship listings via Tavily API
- 🎯 **Smart Matching** — Scores each internship based on skill overlap with your resume
- 🏆 **Ranked Results** — Displays top 10 matches with match percentage and direct apply links

---

## 🖥️ Demo

<img width="1920" height="1080" alt="Screenshot (499)" src="https://github.com/user-attachments/assets/bfad6e58-95d5-4761-b99c-a906cd419eaa" />


> _Upload your resume → Extract skills → Find matching internships in seconds_

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend / UI | [Streamlit](https://streamlit.io/) |
| PDF Parsing | [PyMuPDF](https://pymupdf.readthedocs.io/) (`fitz`) |
| Web Search | [Tavily API](https://tavily.com/) |
| Skill Extraction | Custom `skill_extractor.py` module |
| Config | `python-dotenv` |

---
## Architecture
<img width="1536" height="1024" alt="ai-intership-hunter" src="https://github.com/user-attachments/assets/92d07a5b-2a0f-474e-8871-81464a2f3e84" />


## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Ai-Internship-Hunter.git
cd Ai-Internship-Hunter
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory:

```env
TAVILY_API_KEY=your_tavily_api_key_here
```

Get your free Tavily API key at [https://tavily.com](https://tavily.com).

### 4. Add your skill extractor

Make sure `skill_extractor.py` is present in the root directory. It must expose:

```python
def extract_skills(text: str) -> list[str]:
    ...
```

---

## 🚀 Usage

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

1. Upload your resume as a PDF
2. View your extracted skills
3. Click **Find Internships**
4. Browse ranked matches and apply directly

---

## 📁 Project Structure

```
ai-internship-hunter/
├── app.py                 # Main Streamlit app
├── skill_extractor.py     # Skill extraction module
├── requirements.txt       # Python dependencies
├── .env                   # API keys (not committed)
└── README.md
```

---

## ⚙️ How It Works

1. **Resume Upload** — PyMuPDF extracts raw text from the uploaded PDF
2. **Skill Extraction** — `skill_extractor.py` parses the text to identify technical and soft skills
3. **Web Search** — Tavily searches across multiple queries (e.g., "AI ML internship India 2026")
4. **Filtering** — Results are filtered to only include actual internship listings
5. **Scoring** — Each listing is scored by the percentage of your skills it mentions
6. **Display** — Top 10 results are shown with match tier (🟢 High / 🟡 Medium / 🔴 Low)

---

## 🔒 Environment Variables

| Variable | Description |
|---|---|
| `TAVILY_API_KEY` | Your Tavily search API key |

Never commit your `.env` file. Add it to `.gitignore`:

```
.env
```

---

## 📋 Requirements

See [`requirements.txt`](requirements.txt):

```
streamlit
pymupdf
python-dotenv
tavily-python
```

---

## 🤝 Contributing

Pull requests are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙋 FAQ

**Q: Why are no internships showing up?**
A: Try again — Tavily search results vary. Make sure your API key is valid and has remaining quota.

**Q: Can I add more search queries?**
A: Yes! Edit the `build_queries()` function in `app.py` to add more targeted searches.

**Q: What file formats are supported?**
A: Only PDF resumes are supported at this time.
