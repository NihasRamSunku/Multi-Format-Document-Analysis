from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import logging
from concurrent.futures import ThreadPoolExecutor
import asyncio
import os

# Import modules
from extractor import extract_text
from nlp_core import ensure_nlp_loaded
from modules.highlight import highlight_pos
from modules.pos_stats import extract_pos_stats
from modules.statistics import calculate_statistics
from modules.wordcloud_gen import generate_wordcloud
from modules.summarizer import generate_summary
from modules.readability import analyze_readability
from modules.sentiment import analyze_sentiment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for local dev
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/app", StaticFiles(directory=frontend_path, html=True), name="frontend")


# A thread pool for heavy processing
executor = ThreadPoolExecutor(max_workers=4)

class AnalyzeResponse(BaseModel):
    highlighted_text_html: str
    nouns: list
    verbs: list
    adjectives: list
    adverbs: list
    keywords: list
    statistics: dict
    wordcloud_img: str
    summary: str
    readability: float | None
    sentiment: dict | None
    error: str | None = None

@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_document(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = extract_text((file.filename, content))
        
        if text.startswith("Error:"):
            return AnalyzeResponse(
                error=text, highlighted_text_html="", nouns=[], verbs=[], 
                adjectives=[], adverbs=[], keywords=[], statistics={}, 
                wordcloud_img="", summary="", readability=None, sentiment=None
            )

        if not text.strip():
            return AnalyzeResponse(
                error="Extracted text is empty.", highlighted_text_html="", nouns=[], verbs=[], 
                adjectives=[], adverbs=[], keywords=[], statistics={}, 
                wordcloud_img="", summary="", readability=None, sentiment=None
            )

        # Process in thread pool to avoid blocking the event loop
        loop = asyncio.get_running_loop()
        
        _nlp = ensure_nlp_loaded()
        doc = await loop.run_in_executor(executor, _nlp, text)
        
        # We can run independent tasks concurrently
        # However, POS tagging and highlighting depend on doc. We can run them in thread pool.
        highlight_task = loop.run_in_executor(executor, highlight_pos, doc)
        pos_stats_task = loop.run_in_executor(executor, extract_pos_stats, doc)
        basic_stats_task = loop.run_in_executor(executor, calculate_statistics, doc)
        summary_task = loop.run_in_executor(executor, generate_summary, text)
        readability_task = loop.run_in_executor(executor, analyze_readability, text)
        sentiment_task = loop.run_in_executor(executor, analyze_sentiment, text)

        # Wait for those that don't depend on pos_stats
        highlighted_text_html, pos_results, stats, summary, readability, sentiment = await asyncio.gather(
            highlight_task, pos_stats_task, basic_stats_task, summary_task, readability_task, sentiment_task
        )
        
        # Wordcloud depends on pos_results
        unique_keywords = pos_results["unique_keywords"]
        wordcloud_img = await loop.run_in_executor(executor, generate_wordcloud, unique_keywords)
        
        return AnalyzeResponse(
            highlighted_text_html=highlighted_text_html,
            nouns=pos_results["nouns"],
            verbs=pos_results["verbs"],
            adjectives=pos_results["adjectives"],
            adverbs=pos_results["adverbs"],
            keywords=pos_results["keywords"],
            statistics=stats,
            wordcloud_img=wordcloud_img or "",
            summary=summary,
            readability=readability,
            sentiment=sentiment
        )
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return AnalyzeResponse(
            error=str(e), highlighted_text_html="", nouns=[], verbs=[], 
            adjectives=[], adverbs=[], keywords=[], statistics={}, 
            wordcloud_img="", summary="", readability=None, sentiment=None
        )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
