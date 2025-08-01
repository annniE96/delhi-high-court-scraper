# Delhi High Court Case Scraper 🏛️

A Flask web application that scrapes and displays case information from the Delhi High Court website.

## Features ✨
- **Case Search**: Find cases by type, number, and filing year
- **Database Storage**: SQLite backend for query history
- **Dual Scraping**: Uses both Requests and Selenium (fallback)
- **REST API**: `/api/case-types` endpoint for available case types
- **Health Monitoring**: `/health` endpoint for status checks

## Tech Stack 🛠️
- **Backend**: Flask (Python)
- **Scraping**: BeautifulSoup4, Selenium
- **Database**: SQLite
- **Frontend**: HTML/CSS (Jinja2 templates)

## Installation 💻

### Prerequisites
- Python 3.8+
- Chrome/Firefox (for Selenium)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/[YOUR_USERNAME]/delhi-high-court-scraper.git
   cd delhi-high-court-scraper

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Set up environment variables (create .env file):
   ```env
    FLASK_SECRET_KEY=your_secret_key_here
    FLASK_ENV=development

4. Run the application:
   ```bash
   python app.py

5. Access at: http://localhost:5000

CAPTCHA Handling Strategy
Primary Method
✅ Randomized user agents

✅ Request throttling (2s delay between requests)

✅ Session persistence

Fallback Method
✅ Headless Chrome browser

✅ Human-like interaction delays

✅ Automatic retries (3 attempts maximum)
