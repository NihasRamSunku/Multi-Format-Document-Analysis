import re
from collections import Counter
import logging
from nlp_core import ensure_nlp_loaded

logger = logging.getLogger(__name__)

def generate_summary(text, target_ratio=0.25, min_words=100, max_words_cap=800):
    _nlp = ensure_nlp_loaded()
    
    # We parse the doc here again, but for a real-time API we could pass the sentences
    doc = _nlp(text)
    
    if not text or len(text.split()) < 50:
        return "Not enough content to summarize meaningfully (requires at least 50 words)."
        
    try:
        sentences = [sent.text for sent in doc.sents]
        if len(sentences) < 3:
            return "Text is too short (less than 3 sentences) to summarize."
    except Exception as e:
        logger.error(f"Sentence segmentation error: {e}")
        return f"Error during sentence segmentation: {str(e)}"
        
    total_words_original = len(text.split())
    target_word_count = max(min_words, int(total_words_original * target_ratio))
    target_word_count = min(target_word_count, max_words_cap)
    
    sentence_scores = {}
    important_pos = {"NOUN", "PROPN", "VERB", "ADJ"}
    important_ents = {"PERSON", "ORG", "GPE", "PRODUCT", "EVENT"}
    
    for i, sentence in enumerate(sentences):
        score = 0
        if i < len(sentences) * 0.15 or i > len(sentences) * 0.85:
            score += 1.0
        words = len(sentence.split())
        if 15 <= words <= 30:
            score += 0.5
            
        sent_doc = _nlp(sentence)
        pos_counts = Counter([token.pos_ for token in sent_doc])
        for pos in important_pos:
            score += pos_counts.get(pos, 0) * 0.1
            
        ent_counts = Counter([ent.label_ for ent in sent_doc.ents])
        for ent in important_ents:
            score += ent_counts.get(ent, 0) * 0.2
            
        cue_phrases = [
            "in conclusion", "this paper", "we propose", "results show",
            "findings suggest", "important to", "key finding", "main result" 
        ]
        lower_sent = sentence.lower()
        for phrase in cue_phrases:
            if phrase in lower_sent:
                score += 0.5
        sentence_scores[i] = score
        
    ranked_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    selected_indices = []
    current_length = 0
    
    for idx, score in ranked_sentences:
        if current_length >= target_word_count:
            break
        sent_words = len(sentences[idx].split())
        if current_length + sent_words <= target_word_count * 1.2 or not selected_indices:
            selected_indices.append(idx)
            current_length += sent_words
            
    selected_indices.sort()
    summary_sentences = [sentences[i] for i in selected_indices]
    summary_text = " ".join(summary_sentences)
    summary_text = re.sub(r'\s+([.,;:])', r'\1', summary_text)
    summary_text = re.sub(r'\s+', ' ', summary_text)
    
    if summary_text:
        summary_text = summary_text[0].upper() + summary_text[1:]
        if not summary_text.endswith(('.', '!', '?')):
            summary_text += '.'
            
    return summary_text
