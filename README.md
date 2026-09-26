# Multi-Format Document Analysis Tool

A Python-based web application built with Gradio that performs comprehensive linguistic and statistical analysis on text extracted from various document formats (`.txt`, `.docx`, `.pdf`, `.pptx`).

## Features
- **Multi-Format Extraction:** Extracts text from plain text, Word documents, PDFs, and PowerPoint presentations.
- **NLP Analysis:** Uses `spaCy` to perform Part-of-Speech tagging and extract keywords.
- **Interactive Highlighting:** Visually highlights different parts of speech directly in the text.
- **Text Statistics:** Calculates word counts, sentence counts, and readability scores.
- **Visualizations:** Generates word clouds based on important extracted keywords.
- **Summarization:** Provides an extractive summary of the document.
- **Sentiment Analysis:** Evaluates the polarity and subjectivity of the text using `TextBlob`.

## Project Structure
- `app.py`: Main entry point containing the Gradio web interface.
- `extractor.py`: Functions for parsing and extracting text from different file formats.
- `nlp_processor.py`: Core NLP logic using `spaCy` for tokenization and POS tagging.
- `summarizer.py`: Logic for ranking sentences and generating extractive summaries.
- `analyzer.py`: Functions for sentiment analysis, readability scoring, and word cloud generation.
- `requirements.txt`: Python dependencies.

## Installation & Setup

1. **Clone the repository** (or download the files).
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Download Language Models & Corpora:**
   ```bash
   python -m textblob.download_corpora
   python -m spacy download en_core_web_sm
   python -m spacy download en_core_web_trf
   ```
   *(Note: If `en_core_web_trf` is too large or fails, the app will gracefully fall back to `en_core_web_sm`)*

## Running the Application
Run the main script to launch the Gradio web interface:
```bash
python app.py
```
Open the provided local URL (usually `http://127.0.0.1:7860`) in your web browser.
