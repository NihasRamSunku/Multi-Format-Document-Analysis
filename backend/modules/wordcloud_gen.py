import io
import base64
import logging
import matplotlib
matplotlib.use('Agg') # Needed for headless server
import matplotlib.pyplot as plt
from wordcloud import WordCloud

logger = logging.getLogger(__name__)

def generate_wordcloud(unique_important_keywords):
    if not unique_important_keywords or len(unique_important_keywords) < 3:
        return None
        
    text_for_cloud = ' '.join(unique_important_keywords)
    try:
        wordcloud_obj = WordCloud(width=800, height=400, background_color='white',
                                  colormap='viridis', max_words=100).generate(text_for_cloud)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud_obj, interpolation='bilinear')
        plt.axis('off')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        plt.close()
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode()
        return f"data:image/png;base64,{img_base64}"
    except Exception as e:
        logger.error(f"Error generating word cloud: {e}")
        return None
