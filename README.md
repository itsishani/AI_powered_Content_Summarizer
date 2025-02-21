This project is an AI-driven news aggregator and summarizer that streamlines the process of consuming news content.
It automatically fetches articles from various RSS feeds, extracts the full content, and generates concise summaries using advanced natural language processing techniques.

Key Features
RSS Feed Parsing: Fetches news articles from multiple RSS feeds using the feedparser library.

Article Content Extraction: Extracts full article content from web pages using the requests library.

AI-Powered Summarization: Utilizes the Cohere API to generate concise summaries of article content.

Database Storage: Stores article details including title, author, publication date, link, full content, and summary in a SQLite database.

Web Interface: Offers a user-friendly interface built with Flask, featuring both light and dark themes, as well as custom theme options.
