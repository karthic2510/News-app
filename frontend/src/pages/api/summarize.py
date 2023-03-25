import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
import requests
from bs4 import BeautifulSoup
import openai
import os
import time
import re
from datetime import datetime
from datetime import timedelta
from newsapi import NewsApiClient

GNEWS_API_BASE_URL = 'https://gnews.io/api/v4/search'
GNEWS_API_KEY = 'your_gnews_api_key'
NEWS_API_KEY = 'your_news_api_key'
MS_API_KEY = 'your_mediastack_api_key'
openai.api_key = os.getenv("your_openai_api_key")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        request_body = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(request_body)
        topic = data.get('topic', '')

        # Fetch and process headlines, articles, and summaries
        headlines = fetch_headlines(topic)
        summaries = []
        for headline in headlines:
            if len(summaries) < 5:    
                try:
                    article = scrape_article(headline)
                    summary = summarize_article(article)
                    summaries.append(summary)
                    time.sleep(1)
                except Exception as e:
                    print(f"Error summarizing article: {e}")
                    continue
            else:
                break
            
        concatenated_text = concatenate_summaries(summaries)
        final_summary = summarize_summary(concatenated_text)

        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = json.dumps({'header': final_summary['header'], 'summary': final_summary['summary']}).encode()
        self.wfile.write(response)
        return

def fetch_headlines(topic):
    #fetching 15 from gnews
    params = {
        'q': topic,
        'token': GNEWS_API_KEY,
        'lang': 'en',
        'max': 15 #,
        #'sortby' : 'relevance',
        #'from' : date
    }
    response = requests.get(GNEWS_API_BASE_URL, params=params)

    if response.status_code != 200:
        print(f"Failed to fetch headlines with status code {response.status_code}")
        print(f"Response text: {response.text}")
        raise Exception('Failed to fetch headlines')

    data = response.json()
    headlines = []
    for article in data['articles']:
        headlines.append({"title": article['title'], "url": article['url']})
    
    #fetching 15 from newsapi
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    sources = newsapi.get_sources()
    top_headlines = newsapi.get_top_headlines(q=topic, page_size = 15)
    if top_headlines['status'] == 'ok':
        articles = top_headlines['articles']
        for article in articles:
            title = article['title']
            #print(f"news_api_Title: {title}")
            url = article['url']
            if not any(d['title'] == title for d in headlines):
                headlines.append({'title': title, 'url': url})
    else:
        print(f"Error fetching top headlines for {topic}")
    
    #fetching 15 from mediastack
    ms_url = f"http://api.mediastack.com/v1/news?access_key={MS_API_KEY}&keywords={topic}&limit=15"
    ms_response = requests.get(ms_url)
    
    if response.status_code == 200:
        ms_data = ms_response.json()
        ms_articles = ms_data["data"]
        
        for article in ms_articles:
            if not any(d['title'] == article['title'] for d in headlines):
                headlines.append({
                    "title": article["title"],
                    "url": article["url"]
                })
    else:
        print("Error fetching data from mediastack API:", response.status_code)

    return headlines


def scrape_article(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception('Failed to fetch article')

    soup = BeautifulSoup(response.content, 'html.parser')
    #article = soup.find('article')
    #print(f"Scraping URL: {url}")  
    paragraphs = soup.find_all('p')
    article_text = ' '.join([p.get_text() for p in paragraphs])
    
    return article_text

def summarize_article(article):
    openai.api_key = "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"
    prompt = f"Please summarize the following article in 75 words:\n\n{article}\n"
    ## print(f"Prompt: {prompt}")  
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=750,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0.6,
            presence_penalty=0.6
        #    stop=["\n", "Article"]
        )
        
        summary = response.choices[0].message["content"].strip()
        return summary

    except openai.error.APIError as e:
        print(f"APIError: {e}")
        return None

def concatenate_summaries(summaries):
    concatenated_text = ""
    for summary in summaries:
        # Remove unwanted characters
        cleaned_summary = re.sub(r"[^\w\s.,?!-]+", "", summary)
        # Remove extra whitespace
        cleaned_summary = re.sub(r"\s+", " ", cleaned_summary)
        concatenated_text += cleaned_summary + "\n\n"
    return concatenated_text

def summarize_summary(article):
    openai.api_key = "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"
    prompt = f"Please summarize the following text into a single paragraph of 500 words, with a header stating a unifying theme. Always start with the header and start the summary in a new line. Do not have any additional formating or mention that it is a summary:\n\n{article}\n"
    #print(f"Prompt: {prompt}")  # Add this line
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=1,
            #top_p=1,
            frequency_penalty=0.4,
            presence_penalty=0.4 #,
            #stop=["\n", "Article"]
        )
        
        summary_text = response.choices[0].message["content"]
        #print(summary_text)

        # Split the header from the summary
        split_text = summary_text.split('\n', 1)
        header = split_text[0].strip()
        summary = split_text[1].strip()

        return {'header': header, 'summary': summary}


    except openai.error.APIError as e:
        print(f"APIError: {e}")
        return None