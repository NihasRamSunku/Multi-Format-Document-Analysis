# Multi-Format Document Analysis Tool (FastAPI + Glassmorphism)

A high-performance web application that performs comprehensive linguistic and statistical analysis on text extracted from various document formats (`.txt`, `.docx`, `.pdf`, `.pptx`).

## 🚀 Architecture
This project has been modularized and upgraded from a monolithic script into a modern Web App architecture:
- **Backend (Python / FastAPI):** Utilizes `asyncio` and `ThreadPoolExecutor` to run heavy ML parsing, summarization, and statistic generations concurrently, avoiding event-loop blocking for rapid real-time analysis.
- **Frontend (HTML / CSS / Vanilla JS):** A zero-dependency, ultra-lightweight UI featuring beautiful glassmorphism, dynamic skeleton loaders, staggered reveal animations, and a seamless dark mode.

## ✨ Features
- **Multi-Format Extraction:** Extracts text from plain text, Word documents, PDFs, and PowerPoint presentations.
- **Concurrency Optimized:** Asynchronously processes Document Summarization, Sentiment Analysis, and NLP Tagging.
- **NLP Analysis:** Uses `spaCy` to perform Part-of-Speech tagging and extract keywords.
- **Interactive Highlighting:** Visually highlights different parts of speech directly in the text.
- **Data Export:** Export your results seamlessly into `.csv` format or save a beautiful print-optimized `.pdf` report.
- **Visualizations:** Generates word clouds based on important extracted keywords.

## 📂 Project Structure
```
backend/
├── main.py                 # FastAPI application and routing
├── extractor.py            # File parsing for PDF, DOCX, PPTX
├── nlp_core.py             # Singleton SpaCy model loader
└── modules/
    ├── highlight.py        # POS color-tagging HTML generator
    ├── pos_stats.py        # Keyword and POS parsing
    ├── readability.py      # Flesch reading ease scoring
    ├── sentiment.py        # TextBlob polarity and subjectivity
    ├── statistics.py       # General text metrics
    ├── summarizer.py       # Extractive NLP summarization
    └── wordcloud_gen.py    # Matplotlib WordCloud generator
frontend/
├── index.html              # Main HTML markup
├── script.js               # Logic for API calls, Theme toggling, and Exports
└── style.css               # Advanced animations, skeleton loaders, and print layouts
```

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NihasRamSunku/Multi-Format-Document-Analysis.git
   cd Multi-Format-Document-Analysis
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download Language Models & Corpora:**
   ```bash
   python -m textblob.download_corpora
   python -m spacy download en_core_web_sm
   ```

## ⚡ Running the Application
Launch the FastAPI server which automatically serves the frontend directory:
```bash
python backend/main.py
```
Open the application in your web browser:
**👉 http://127.0.0.1:8000/app**
