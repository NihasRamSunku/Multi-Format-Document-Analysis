def calculate_statistics(doc):
    stats_data = {
        "Total Content Words": len([t for t in doc if not t.is_space]),
        "Unique Lemmatized Words": len(set([token.lemma_.lower() for token in doc if token.is_alpha])),
        "Sentences": len(list(doc.sents))
    }
    return stats_data
