# Delhi High Court Case Data Fetcher

A web application that fetches case information from the Delhi High Court's website and provides a user-friendly interface to search and view case details.

This project features a **dual-scraper system**—defaulting to a stable mock data mode for demonstration, while also including a fully implemented live scraper showcasing advanced browser automation and CAPTCHA-solving techniques.

---

## 🏛️ Court Chosen

**Delhi High Court**  
Website: [https://delhihighcourt.nic.in/](https://delhihighcourt.nic.in/)

---

## ✨ Features

- **Simple Web Interface:** Clean and responsive form for searching cases by type, number, and year.
- **Case Information Display:** Neatly presents key case details, including petitioner/respondent names, filing dates, and current status.
- **PDF Generation:** Download a formatted PDF summary of any retrieved case.
- **Database Logging:** Logs all user search queries and scraper responses to a local SQLite database.
- **Dual Scraper System:** Switches intelligently between a reliable mock data provider and a live web scraper.
- **User-Friendly Error Handling:** Clear feedback for invalid searches or when data cannot be fetched.

---

## 🚀 Quick Start

### **Prerequisites**

- Python 3.8 or higher
- Git
- Tesseract OCR Engine (Required only for live scraper)

### **Installation**

```bash
git clone https://github.com/your-username/delhi-high-court-scraper.git
cd delhi-high-court-scraper

# Create and activate a virtual environment

# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Open your browser and navigate to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔧 Sample Environment Variables

While not required to run locally, using a `.env` file is recommended for production:

```env
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-super-strong-and-random-secret-key

# Scraping Configuration
# Set to "False" to enable the live scraper, "True" for mock data (default)
USE_MOCK_SCRAPER=True
```

---

## 🛡️ CAPTCHA Handling Strategy

The application includes a dual-scraper system to ensure reliability and demonstrate a robust approach to live web scraping.

### 1. **Mock Scraper (Default Mode)**

- Uses a curated set of realistic case data in `sample_data.py`.
- Guarantees a stable, fast, and reliable user experience.
- Demonstrates core features (UI, database, PDF generation) without unpredictability of the live website.

### 2. **Live Scraper (Advanced Mode)**

- Fully implemented `DelhiHighCourtScraper` interacts with the live court website.
- Can be activated by setting `USE_MOCK_SCRAPER=False` in `app.py`.

#### **Strategy:**

- **Browser Automation:** Uses Selenium WebDriver to launch a real (headless) Chrome browser, mimicking user interactions.
- **Image Processing:** Locates the CAPTCHA, takes a screenshot, and uses OpenCV to pre-process the image for clarity.
- **OCR with Tesseract:** Passes the cleaned image to Tesseract OCR to recognize the CAPTCHA.
- **Automated Submission & Retries:** Submits recognized text, retries on failure.

#### **Limitations:**

Modern sites like the Delhi High Court use sophisticated anti-bot measures.  
While the live scraper is technically sound, it may still be blocked.  
The project defaults to mock mode for reliable demonstration, but the live scraper is included to showcase technical capabilities.

---

## 🔒 Security Considerations

- **No Hardcoded Secrets:** Flask `SECRET_KEY` is loaded from environment variables.
- **Input Validation:** All user input is validated in `app.py`.
- **SQL Injection Prevention:** `database.py` uses parameterized queries (`?`) to prevent SQL injection.

---

## 📄 License

[MIT](LICENSE)

---

## 🙋‍♂️ Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss your ideas.

---

## 📧 Contact

If you have any questions or suggestions, feel free to reach out via [Issues](https://github.com/your-username/delhi-high-court-scraper/issues).
