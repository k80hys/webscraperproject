# WebScraperProject

This project is a web scraper built in Python to extract iPhone model details from a sample web page. It was developed as part of my **ISQS-6339 (Business Intelligence)** course in my **MS Data Science** program.

## Overview

The scraper uses Python libraries `requests` and `BeautifulSoup` to:

- Fetch and parse HTML content from a specified URL.
- Extract detailed information about the iPhone 11 Pro, including OS, color, storage, and front camera features.
- Navigate child pages linked within the main page to retrieve additional phone specifications.
- Export collected phone data for all listed iPhone models into a CSV file (`assign2.csv`).

## How it works

1. The program sends an HTTP request to the target URL.
2. Parses the HTML content using BeautifulSoup.
3. Locates the phone list section and extracts attributes of each iPhone model.
4. For the iPhone 11 Pro specifically, it prints key details to the console.
5. For all phones, it follows links to child pages to gather more specs.
6. Outputs a CSV file with structured phone data, saved locally.

## Dependencies

- Python 3.x
- `requests` library
- `beautifulsoup4` library

Install dependencies via pip if you don't have them:

```bash
pip install requests beautifulsoup4