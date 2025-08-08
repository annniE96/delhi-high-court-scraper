# Delhi High Court Case Data Fetcher

A web application that fetches case information from the Delhi High Court's website and provides a user-friendly interface to search and view case details. The project features a dual-scraper system, defaulting to a stable mock data mode for demonstration while also including a fully implemented live scraper to showcase advanced browser automation and CAPTCHA-solving techniques.

---

## 🏛️ Court Chosen

Delhi High Court (https://delhihighcourt.nic.in/)

---

## ✨ Features

- **Simple Web Interface:** A clean and responsive form for searching cases by type, number, and year.
- **Case Information Display:** Neatly presents key case details, including petitioner/respondent names, filing dates, and current status.
- **PDF Generation:** Allows users to download a formatted PDF summary of any retrieved case.
- **Database Logging:** All user search queries and the scraper's responses are logged to a local SQLite database for record-keeping.
- **Dual Scraper System:** Intelligently switches between a reliable mock data provider and a live web scraper.
- **User-Friendly Error Handling:** Provides clear feedback for invalid searches or when data cannot be fetched.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git
- Tesseract OCR Engine (Required only if you intend to run the live scraper)

### Installation 💻

Clone the repository:

```bash
git clone https://github.com/annniE96/delhi-high-court-scraper.git
cd delhi-high-court-scraper
```

Create and activate a virtual environment:

```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open your browser: Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔧 Sample Environment Variables

While not required to run the application locally, using a .env file is recommended for production:

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

The application includes a dual-scraper system to ensure reliability while also demonstrating a robust approach to the challenges of live web scraping, as required by the project deliverables.

### 1. Mock Scraper (Default Mode)

The application defaults to using a MockScraper. This scraper reads from a curated set of realistic case data in sample_data.py. This approach guarantees a stable, fast, and reliable user experience for demonstrating the application's core features (UI, database, PDF generation) without being affected by the unpredictability of the live website.

### 2. Live Scraper (Advanced Mode)

The project includes a fully implemented DelhiHighCourtScraper designed to interact with the live court website. This scraper can be activated by setting USE_MOCK_SCRAPER=False in app.py.

**Strategy:**
- **Browser Automation:** It uses Selenium WebDriver to launch and control a real (headless) Chrome browser, mimicking a real user's interactions. This is crucial for bypassing basic script-blocking measures.
- **Image Processing:** It locates the CAPTCHA on the page, takes a screenshot, and uses the OpenCV library to pre-process the image (converting to grayscale and applying a binary threshold) to remove noise and improve clarity.
- **OCR with Tesseract:** The cleaned image is passed to the Tesseract OCR engine, which attempts to recognize the characters in the CAPTCHA.
- **Automated Submission & Retries:** The recognized text is entered into the form, which is then submitted. The scraper will retry this process multiple times if it detects that the CAPTCHA failed.

**Limitations Due to Website Restrictions:**
Modern websites like the Delhi High Court's portal employ sophisticated anti-bot measures that are specifically designed to detect and block automated scripts, even those using advanced tools like Selenium. These systems can analyze browsing patterns, JavaScript execution, and other subtle cues.

While the implemented live scraper represents a complete and technically sound strategy for circumventing a standard CAPTCHA, it may still be blocked by these advanced security measures. Therefore, the project defaults to the mock mode to ensure a successful demonstration of the application's functionality. The live scraper is included as a deliverable to showcase the technical approach and understanding of the complexities involved in real-world web scraping.

---

## 🔒 Security Considerations

- **No Hardcoded Secrets:** The Flask SECRET_KEY is designed to be loaded from environment variables.
- **Input Validation:** User input from the search form is validated in app.py before being processed.
- **SQL Injection Prevention:** The database.py uses parameterized queries (?), which is the standard method for preventing SQL injection attacks.

---

## 📄 License

[MIT](LICENSE)

---

## 🙋‍♂️ Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss your ideas.

---

## 📧 Contact

If you have any questions or suggestions, feel free to reach out via [Issues](https://github.com/annniE96/delhi-high-court-scraper/issues)  
or email: **kdb6222@gmail.com**

