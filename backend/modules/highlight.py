import re

def highlight_pos(doc):
    text = doc.text
    highlighted_text_html = ""
    
    POS_COLORS = {
        "NOUN": "background-color: #ffcccc; color: #cc0000;",
        "PRON": "background-color: #ccffcc; color: #006600;",
        "ADJ":  "background-color: #ffebcc; color: #cc7a00;",
        "ADV":  "background-color: #cce0ff; color: #0044cc;",
        "VERB": "background-color: #ffccf2; color: #990066;",
        "OTHER": "background-color: #e6e6e6; color: #333333;",
        "LINK": "background-color: #fff0b3; color: #b38600;",
    }
    OTHER_POS_TAGS = {"AUX", "ADP", "CCONJ", "SCONJ", "DET", "PART", "INTJ", "NUM", "PUNCT", "SYM", "X", "SPACE"}
    
    current_char_index = 0
    for token in doc:
        match_start = text.find(token.text, current_char_index)
        if match_start == -1:
             highlighted_text_html += token.text_with_ws
             current_char_index += len(token.text_with_ws)
             continue
             
        highlighted_text_html += text[current_char_index:match_start]
        current_char_index = match_start
        style = ""
        
        if token.like_url or token.text.startswith("http"):
            style = POS_COLORS["LINK"]
        elif token.pos_ in POS_COLORS:
            style = POS_COLORS[token.pos_]
        elif token.pos_ in OTHER_POS_TAGS or token.pos_ == "":
            style = POS_COLORS["OTHER"]
        else:
            style = POS_COLORS["OTHER"]

        if style:
             highlighted_text_html += f'<span style="{style} padding: 2px 4px; border-radius: 4px; display: inline-block; margin: 2px;">{token.text}</span>'
        else:
             highlighted_text_html += token.text
             
        current_char_index += len(token.text)
        
        # Replace newlines with <br> for HTML rendering
        whitespace = token.whitespace_.replace('\n', '<br>')
        highlighted_text_html += whitespace
        current_char_index += len(token.whitespace_)
            
    if current_char_index < len(text):
        highlighted_text_html += text[current_char_index:].replace('\n', '<br>')

    legend_html_str = """
    <div style="margin-top: 20px; font-size: 13px; padding: 15px; background: rgba(255,255,255,0.8); backdrop-filter: blur(10px); border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
        <strong>POS Legend:</strong>
        <span style="background-color:#ffcccc;color:#cc0000;padding:2px 5px;border-radius:3px;margin:2px;">NOUN</span>
        <span style="background-color:#ccffcc;color:#006600;padding:2px 5px;border-radius:3px;margin:2px;">PRONOUN</span>
        <span style="background-color:#ffebcc;color:#cc7a00;padding:2px 5px;border-radius:3px;margin:2px;">ADJECTIVE</span>
        <span style="background-color:#cce0ff;color:#0044cc;padding:2px 5px;border-radius:3px;margin:2px;">ADVERB</span>
        <span style="background-color:#ffccf2;color:#990066;padding:2px 5px;border-radius:3px;margin:2px;">VERB</span>
        <span style="background-color:#e6e6e6;color:#333333;padding:2px 5px;border-radius:3px;margin:2px;">OTHER</span>
    </div>"""

    return f"<div style='font-family: \"Inter\", sans-serif; line-height: 2.0;'>{highlighted_text_html.strip()}</div>{legend_html_str}"
