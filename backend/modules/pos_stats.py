from collections import Counter

def extract_pos_stats(doc):
    nouns, verbs, adjectives, adverbs, pronouns = [], [], [], [], []
    important_keywords_collector = []
    
    for token in doc:
        lemma = token.lemma_.lower()
        if token.pos_ == "NOUN" and token.is_alpha:
            nouns.append(lemma)
        elif token.pos_ == "VERB" and token.is_alpha:
            verbs.append(lemma)
        elif token.pos_ == "ADJ" and token.is_alpha:
            adjectives.append(lemma)
        elif token.pos_ == "ADV" and token.is_alpha:
            adverbs.append(lemma)
        elif token.pos_ == "PRON" and token.is_alpha:
            pronouns.append(lemma)
            
        if token.pos_ in ["NOUN", "PROPN", "ADJ", "VERB"] and len(lemma) > 3 and not token.is_stop and token.is_alpha:
            important_keywords_collector.append(lemma)
            
    def clean_and_count(word_list):
        filtered = [word for word in word_list if len(word) > 1]
        return Counter(filtered).most_common(20) # Return top 20
        
    unique_important_keywords = list(set(important_keywords_collector))
    
    return {
        "nouns": clean_and_count(nouns),
        "verbs": clean_and_count(verbs),
        "adjectives": clean_and_count(adjectives),
        "adverbs": clean_and_count(adverbs),
        "keywords": clean_and_count(unique_important_keywords),
        "unique_keywords": unique_important_keywords
    }
