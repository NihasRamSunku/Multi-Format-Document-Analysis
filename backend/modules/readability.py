import textstat
import logging

logger = logging.getLogger(__name__)

def analyze_readability(text):
    try:
        if len(text.split()) > 20: 
            return textstat.flesch_reading_ease(text)
        else:
            return None
    except Exception as e:
        logger.error(f"Readability score error: {e}")
        return None
