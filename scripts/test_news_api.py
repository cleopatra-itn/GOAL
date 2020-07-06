import os
import sys
from pathlib import Path

# root path
ROOT_PATH = Path(os.path.dirname(__file__)).parent

# import MLMInference
sys.path.append(str(ROOT_PATH))
from models.news_articles_api import NewsArticlesApi

# news api
news_api = NewsArticlesApi(api_key=open(f'{ROOT_PATH}/ER_API_KEY').readline())

# tests
hannover = news_api.get_news_articles('Hannover', 'de')
sofia = news_api.get_news_articles('Hannover', 'en')
dubrovnik = news_api.get_news_articles('Dubrovnik', 'hu')

print(hannover)
print(sofia)
print(dubrovnik)
