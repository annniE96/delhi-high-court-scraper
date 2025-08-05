# Delhi High Court Case Data Fetcher
A web application that fetches case information from the Delhi High Court's website and provides a user-friendly interface to search and view case details.

# 🏛️ Court Chosen
Delhi High Court (https://delhihighcourt.nic.in/)

# ✨ Features
Simple Web Interface: Clean, responsive form for case search.

Case Information Display: Shows petitioner, respondent, dates, and case status.

Document Downloads: Generates and allows downloading of a PDF summary for any searched case.

Database Logging: All search queries and their outcomes are logged in an SQLite database.

Error Handling: User-friendly error messages for invalid cases or server issues.

Dual Scraper System: A robust backend that can run in a reliable mock mode or a live scraping mode.

# 🚀 Quick Start
## Prerequisites
Python 3.8 or higher
Git
Tesseract OCR Engine (Required only if you want to run the live scraper)

# Installation 💻
1. Clone the repository:
 git clone [https://github.com/your-username/delhi-high-court-scraper.git](https://github.com/your-username/delhi-high-court-scraper.git)
 cd delhi-high-court-scraper

Create and activate a virtual environment:

# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Create required directories:

# This command works on macOS/Linux. On Windows, create the 'data' folder manually.
mkdir -p data

Run the application:

python app.py

Open your browser: Navigate to http://127.0.0.1:5000

🔧 Environment Variables
For best practice, you can create a .env file in the root directory to manage configuration. This project does not require one to run, but here is a sample for production use:

# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-super-strong-and-random-secret-key

# Scraping Configuration
# Set to "False" to enable the live scraper, "True" for mock data (default)
USE_MOCK_SCRAPER=True

🛡️ CAPTCHA Handling Strategy
The application includes a dual-scraper system to ensure reliability and to demonstrate a robust approach to handling website challenges, as required.

1. Mock Scraper (Default Mode)
Purpose: Provides a stable and fast experience for development and demonstration.

How it works: Reads from a predefined set of realistic case data in sample_data.py. This guarantees the UI and all application features can be tested without hitting the live website.

2. Live Scraper with OCR (Advanced Mode)
Purpose: To interact with the live court website and handle dynamic challenges like CAPTCHAs.

Activation: Set USE_MOCK_SCRAPER=False in app.py.

Strategy:

Image Processing: The scraper downloads the CAPTCHA image and uses the Pillow library to convert it to grayscale and enhance its contrast, making it easier for a machine to read.

OCR with Tesseract: The processed image is passed to the Tesseract OCR engine via the pytesseract library. Tesseract attempts to recognize the characters in the image.

Form Submission: The recognized text is then submitted along with the case details in the search form.

Error Handling: If the CAPTCHA fails or the case is not found, the system provides a clear error message to the user.

🔒 Security Considerations
No Hardcoded Secrets: The Flask SECRET_KEY is loaded from environment variables, not written in the code.

Input Validation:

