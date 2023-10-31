import requests
from dotenv import load_dotenv
import os

# ---------- VARIABLES ----------
load_dotenv()
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
SUMMARISER_API_KEY = os.getenv('SUMMARISER_API_KEY')
EXTRACTOR_API_KEY = os.getenv('EXTRACTOR_API_KEY')
SEARCH_QUERY = "geopolitics OR international relations OR conflicts OR economic crises OR government"
NUM_ARTICLES = 10
MAXLENGTH = 200

# ---------- FUNCTIONS ----------
# Get news from newsapi.org
def get_news():
    news = requests.get(f"https://newsapi.org/v2/everything?q={SEARCH_QUERY}&language=en&pageSize={NUM_ARTICLES}&sortBy=relevancy&apiKey={NEWS_API_KEY}").json()
    
    return news


# Extract and summarise news from news article url
def summarize_url(url):
    # EXTRACT
    extracted = requests.get(f"https://extractorapi.com/api/v1/extractor/?apikey={EXTRACTOR_API_KEY}&url={url}").json()

    # SUMMARISE
    headers = {
    "api-key": SUMMARISER_API_KEY, 
    "content-type": "application/json"
    }
    payload = {
    "input": extracted["text"],
    "input_type": "article",
        "content_type": "application/json",
        "output_type": "json",
    "multilingual": {
        "enabled": True
    },
    "steps": [
        {
        "skill": "summarize",
        "params": {
            "auto_length": False,
            "find_origins": True,
            "max_length": MAXLENGTH,
            "min_length": 5,
        }
        }
    ],
    }

    summarised = requests.post("https://api.oneai.com/api/v0/pipeline", json=payload, headers=headers).json()

    return summarised["output"][0]["contents"][0]["utterance"]


# Serve relevant info: article title, url and summary
def serve_info():
    news = get_news()
    output = [{'title': article['title'], 
               'url': article['url'], 
               'text': summarize_url(article['url'])} 
              for article in news['articles']]
    
    return output