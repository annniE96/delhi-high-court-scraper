# Delhi High Court Case Data Fetcher

A web application to fetch case information from the Delhi High Court's website, providing a user-friendly interface to search and view case details.

---

## 🏛️ Court Chosen

**Delhi High Court**  
[https://delhihighcourt.nic.in/](https://delhihighcourt.nic.in/)

---

## ✨ Features

- **Simple Web Interface**: Clean, responsive form for case search.
- **Case Information Display**: Shows petitioner, respondent, dates, and case status.
- **Document Downloads**: Generates and allows downloading of a PDF summary for any searched case.
- **Database Logging**: All search queries and their outcomes are logged in an SQLite database.
- **Error Handling**: User-friendly error messages for invalid cases or server issues.
- **Dual Scraper System**: Robust backend can run in a reliable mock mode or a live scraping mode.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git
- Tesseract OCR Engine *(required only for live scraper mode)*

### Installation 💻

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/delhi-high-court-scraper.git
   cd delhi-high-court-scraper
   ```

2. **Create and activate a virtual environment:**
   - *On Windows:*
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - *On macOS/Linux:*
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create required directories:**
   - *On macOS/Linux:*
     ```bash
     mkdir -p data
     ```
   - *On Windows:*  
     Create a folder named `data` manually.

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Open your browser:**  
   Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔧 Environment Variables

For best practice, create a `.env` file in the root directory to manage configuration.  
*(Not required to run, but recommended for production use)*

```
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-super-strong-and-random-secret-key

# Scraping Configuration
# Set to "False" to enable the live scraper, "True" for mock data (default)
USE_MOCK_SCRAPER=True
```

---

## 🛡️ CAPTCHA Handling Strategy

The application includes a dual-scraper system designed for reliability and robust handling of website challenges.

### 1. Mock Scraper (Default Mode)
- **Purpose:** Provides stability and speed for development and demos.
- **How it works:** Reads from a predefined set of realistic case data in `sample_data.py`, ensuring the UI and all features are testable without hitting the live website.

### 2. Live Scraper with OCR (Advanced Mode)
- **Purpose:** Interacts with the live court website, handling dynamic challenges like CAPTCHAs.
- **Activation:** Set `USE_MOCK_SCRAPER=False` in `app.py`.
- **Strategy:**
  - *Image Processing:* Downloads the CAPTCHA image, converts it to grayscale and enhances contrast using Pillow.
  - *OCR with Tesseract:* Uses pytesseract to recognize the CAPTCHA text.
  - *Form Submission:* Submits the recognized text and case details.
  - *Error Handling:* Provides clear error messages if CAPTCHA fails or case is not found.

---

## 🔒 Security Considerations

- **No Hardcoded Secrets:** The Flask `SECRET_KEY` should be managed securely, preferably via environment variables or a `.env` file.
- **Sensitive Data:** Do not commit sensitive keys or credentials to your repository.

---

## 📄 License

[MIT License](LICENSE)

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📫 Contact

For questions, open an issue or contact [kdb6222@gmail.com](mailto:kdb6222@gmail.com).
