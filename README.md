Delhi High Court Case Data Fetcher
A web application that fetches case information from Delhi High Court's website and provides a user-friendly interface to search and view case details.
🏛️ Court Chosen
Delhi High Court (https://delhihighcourt.nic.in/)
✨ Features

Simple Web Interface: Clean, responsive form for case search
Case Information Display: Shows petitioner, respondent, dates, and case status
Document Downloads: Links to PDF orders and judgments
Database Logging: All queries and responses are logged in SQLite
Error Handling: User-friendly error messages for invalid cases
Responsive Design: Works on desktop and mobile devices

🚀 Quick Start
Prerequisites

Python 3.8 or higher
Git
Chrome browser (for Selenium automation)

## Installation 💻

### Prerequisites
- Python 3.8+
- Chrome/Firefox (for Selenium)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/annniE96/delhi-high-court-scraper.git
   cd delhi-high-court-scraper

2. Create virtual environment:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
3. Install dependencies:    
   ```bash
   pip install -r requirements.txt
4. Create project structure:
   ```bash
   mkdir -p templates static data

5. Run the application:
   ```bash
   python app.py

6. Open your browser: Navigate to http://localhost:5000

## 🔧 Environment Variables
Create a .env file in the root directory (optional):
### Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

### Database Configuration
DATABASE_PATH=data/court_data.db

### Scraping Configuration
SCRAPING_DELAY=2
MAX_RETRIES=3
TIMEOUT=30
    
## 🛡️ CAPTCHA Handling Strategy
Our multi-layered approach to handle website challenges:
1. Request-based Scraping

Uses Python requests library for fast HTTP requests
Handles form submissions and session management
Extracts CSRF tokens and hidden form fields automatically

2. Selenium Browser Automation

Falls back to Selenium WebDriver for JavaScript-heavy pages
Handles dynamic content loading
Can solve simple CAPTCHAs through automated interaction

3. Intelligent Parsing

Uses BeautifulSoup for robust HTML parsing
Handles various HTML structures and layouts
Extracts case information using multiple parsing strategies

4. Error Handling & Retries

Implements exponential backoff for failed requests
Graceful degradation when scraping fails
Provides meaningful error messages to users

5. Development Mode

Returns mock data for testing when real scraping fails
Allows development without constant website dependencies

## 🐳 Docker Support
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p data

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "app.py"]

## Build and Run
# Build image
docker build -t court-data-fetcher .

# Run container
docker run -p 5000:5000 court-data-fetcher

### 🔒 Security Considerations

No Hardcoded Secrets: All sensitive data via environment variables
Input Validation: Form inputs are validated and sanitized
SQL Injection Prevention: Uses parameterized queries
Rate Limiting: Respectful scraping with delays between requests
Error Handling: No sensitive information in error messages
      


