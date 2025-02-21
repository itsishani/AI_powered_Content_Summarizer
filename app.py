from flask import Flask, render_template, request, redirect, url_for, jsonify
import feedparser
import requests
from bs4 import BeautifulSoup
import sqlite3
import cohere

# Flask setup
app = Flask(__name__)
DATABASE = 'articles.db'

# Cohere API setup
COHERE_API_KEY = 'your_cohere_api_key'
co = cohere.Client(COHERE_API_KEY)

# Initialize database
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            publication_date TEXT,
            link TEXT NOT NULL UNIQUE,
            content TEXT,
            summary TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Fetch RSS feed articles
def fetch_rss_feed(feed_url):
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries:
        articles.append({
            'title': entry.title,
            'author': getattr(entry, 'author', 'Unknown'),
            'publication_date': getattr(entry, 'published', 'Unknown'),
            'link': entry.link
        })
    return articles

# Extract full content from article link
def extract_full_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        return ' '.join(p.get_text() for p in paragraphs)
    except Exception as e:
        print(f"Error extracting content from {url}: {e}")
        return None

# Summarize text using Cohere
def summarize_text(content):
    try:
        response = co.summarize(text=content, length="short")
        return response.summary
    except Exception as e:
        print(f"Error summarizing content: {e}")
        return "Summary unavailable."

# Save article to the database
def save_article(article):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        INSERT OR IGNORE INTO articles (title, author, publication_date, link, content, summary)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (article['title'], article['author'], article['publication_date'], article['link'], article['content'], article['summary']))
    conn.commit()
    conn.close()

# Flask routes
@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM articles ORDER BY id DESC')
    articles = c.fetchall()
    conn.close()
    return render_template('index.html', articles=articles)

@app.route('/fetch', methods=['POST'])
def fetch():
    feed_url = request.form['feed_url']
    articles = fetch_rss_feed(feed_url)
    for article in articles:
        content = extract_full_content(article['link'])
        if content:
            article['content'] = content
            article['summary'] = summarize_text(content)
            save_article(article)
    return redirect(url_for('index'))

@app.route('/delete/<int:article_id>')
def delete_article(article_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('DELETE FROM articles WHERE id = ?', (article_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Initialize the database
init_db()

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
