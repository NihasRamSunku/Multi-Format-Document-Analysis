from textblob import TextBlob
import logging

logger = logging.getLogger(__name__)

def analyze_sentiment(text):
    if not text.strip():
        return None
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        if polarity > 0.05:
            sentiment_type = "Positive"
        elif polarity < -0.05:
            sentiment_type = "Negative"
        else:
            sentiment_type = "Neutral"
            
        return {
            "type": sentiment_type,
            "polarity": round(polarity, 2),
            "subjectivity": round(subjectivity, 2)
        }
    except Exception as e:
        logger.error(f"Sentiment analysis error: {e}")
        return None
