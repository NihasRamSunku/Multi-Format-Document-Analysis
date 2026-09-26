import spacy
import logging

logger = logging.getLogger(__name__)

nlp = None

def ensure_nlp_loaded():
    global nlp
    if nlp is None:
        try:
            # For speed in real-time API, we prefer the smaller model, but try trf first if requested
            nlp = spacy.load("en_core_web_sm")
            logger.info("Loaded small spaCy model for speed.")
        except Exception:
            raise RuntimeError("spaCy NLP model could not be loaded.")
    return nlp
