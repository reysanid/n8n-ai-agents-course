import feedparser
import requests
import schedule
import time

TELEGRAM_TOKEN = "8540300047:AAHR31mObBZ5lXz-KFMZRuH8Xks9CTBtdvc"
CHAT_ID = "Id: 126233537"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"

RSS_FEEDS = [
    "https://www.designboom.com/feed/",
    "https://www.designboom.com/art/feed/",
    "https://www.designboom.com/technology/feed/"
]

def fetch_news():
    all_articles = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            article = {
                "title": entry.title,
                "link": entry.link,
                "summary": entry.summary
            }
            all_articles.append(article)
    return all_articles

def summarize_with_ollama(text):
    prompt = f"Please summarize this news in two short Persian sentences:\n{text}"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=180)
        response_data = response.json()
        return response_data.get("response", "No summary found.")
    except Exception as e:
        return f"Ollama Error: {e}"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Telegram Error: {response.text}")
    except Exception as e:
        print(f"Telegram Send Failed (VPN is on?): {e}")

def daily_job():
    print("Fetching News...")
    articles = fetch_news()
    
    if not articles:
        send_telegram_message("No news found today!")
        return

    digest = "Daily Digest News\n\n"
    
    for i, article in enumerate(articles[:10], 1):
        print(f"Summarizing news {i}...")
        summary = summarize_with_ollama(article["summary"])
        
        digest += f"{i}. {article['title']}\n"
        digest += f"Summary: {summary}\n"
        digest += f"Link: {article['link']}\n\n"
        time.sleep(1)

    print("Sending to Telegram...")
    send_telegram_message(digest)

schedule.every().day.at("10:00").do(daily_job)

print("Bot is running! Waiting for 10 AM...")

daily_job() 
while True:
    schedule.run_pending()
    time.sleep(60)