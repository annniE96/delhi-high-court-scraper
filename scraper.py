import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin
import logging
import json
import io

# --- New/Updated Imports for Selenium & OpenCV Approach ---
try:
    from PIL import Image
    import pytesseract
    import cv2 # OpenCV for advanced image processing
    import numpy as np # Required by OpenCV
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import Select
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# Import from your renamed sample_data.py file
from sample_data import MOCK_CASES

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DelhiHighCourtScraper:
    """
    Scraper for fetching live case data using Selenium and OpenCV for CAPTCHA solving.
    """
    def __init__(self):
        self.base_url = "https://delhihighcourt.nic.in"
        self.case_status_url = f"{self.base_url}/case-status"
        
        if not SELENIUM_AVAILABLE:
            logger.warning("Required libraries (Selenium, OpenCV, etc.) are not installed. The live scraper will not work.")
            logger.warning("Install them via requirements.txt")

    def _get_driver(self):
        """Initializes and returns a Selenium WebDriver instance."""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def _solve_captcha_with_opencv(self, image_bytes):
        """
        Processes a CAPTCHA image using OpenCV and solves it with Tesseract.
        """
        try:
            # Step 1: Read the in-memory image bytes with OpenCV
            image_array = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            # Step 2: Pre-process the image (Grayscale and Thresholding)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV) # Inverting can sometimes help

            # Step 3: Perform OCR with a specific configuration for digits
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz'
            captcha_text = pytesseract.image_to_string(thresh, config=custom_config).strip()
            
            captcha_text = re.sub(r'[^a-zA-Z0-9]', '', captcha_text)
            logger.info(f"OpenCV+Tesseract OCR Result: '{captcha_text}'")
            
            return captcha_text if len(captcha_text) > 3 else None
        except Exception as e:
            logger.error(f"An error occurred during OpenCV CAPTCHA solving: {e}")
            return None


    def search_case(self, case_type, case_number, filing_year, **kwargs):
        """
        Attempts to fetch real case details from the court website using Selenium.
        """
        if not SELENIUM_AVAILABLE:
            return False, {}, "Selenium libraries are not installed. Cannot perform live scrape."

        driver = self._get_driver()
        try:
            logger.info(f"Attempting LIVE scrape for: {case_type}/{case_number}/{filing_year}")
            driver.get(self.case_status_url)
            time.sleep(2)

            logger.info("Filling out the search form...")
            select_element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, 'c_type'))
            )
            Select(select_element).select_by_visible_text(case_type.rstrip('.'))
            
            driver.find_element(By.ID, 'c_no').send_keys(case_number)
            driver.find_element(By.ID, 'c_year').send_keys(filing_year)

            for attempt in range(3):
                logger.info(f"Attempt {attempt + 1} to solve CAPTCHA...")
                captcha_element = driver.find_element(By.ID, "captcha-image")
                
                image_bytes = captcha_element.screenshot_as_png
                captcha_solution = self._solve_captcha_with_opencv(image_bytes)

                if not captcha_solution:
                    logger.warning("OCR failed to produce a result, retrying...")
                    driver.find_element(By.ID, 'reload-captcha').click()
                    time.sleep(2)
                    continue

                driver.find_element(By.ID, "captcha").send_keys(captcha_solution)
                driver.find_element(By.ID, 'search').click()

                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "table-bordered"))
                    )
                    logger.info("CAPTCHA solved successfully!")
                    case_data = self._parse_response(driver.page_source, case_type, case_number, filing_year)
                    return True, case_data, ""
                except:
                    logger.warning("CAPTCHA likely failed, retrying...")
                    driver.find_element(By.ID, 'reload-captcha').click()
                    time.sleep(2)
            
            return False, {}, "Failed to solve CAPTCHA after multiple attempts."

        except Exception as e:
            logger.error(f"An error occurred during the Selenium scrape: {e}")
            return False, {}, "An unexpected error occurred during the live scrape."
        finally:
            driver.quit()

    def _parse_response(self, html_content, case_type, case_number, filing_year):
        # This function remains the same as it correctly parses the results table
        soup = BeautifulSoup(html_content, 'html.parser')
        parsed_data = { 'case_number': f"{case_number}/{filing_year}", 'case_type': case_type }
        try:
            details_table = soup.find('table', {'class': 'table-bordered'})
            if not details_table: return None
            rows = details_table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) < 2: continue
                label = cells[0].text.strip().lower()
                value = cells[1].text.strip()
                if 'case title' in label:
                    parsed_data['case_title'] = value
                    if 'vs' in value.lower():
                        parts = re.split(r'\s+vs\s+', value, flags=re.IGNORECASE)
                        parsed_data['petitioner_name'] = parts[0].strip()
                        parsed_data['respondent_name'] = parts[1].strip()
                elif 'filing date' in label: parsed_data['filing_date'] = value
                elif 'next date' in label: parsed_data['next_hearing_date'] = value
                elif 'status' in label: parsed_data['case_status'] = value
            return parsed_data
        except Exception as e:
            logger.error(f"Error parsing live response: {e}")
            return None


class MockScraper:
    """
    Mock scraper that uses a centralized, corrected data source for development.
    """
    def __init__(self):
        self.mock_data = MOCK_CASES
        logger.info(f"MockScraper initialized with {len(self.mock_data)} cases.")

    def search_case(self, case_type, case_number, filing_year, **kwargs):
        """
        Mock search that returns predefined data from the MOCK_CASES dictionary.
        """
        time.sleep(0.5)
        
        # --- THIS IS THE FIX ---
        # Remove any trailing dots from the case_type before creating the key.
        cleaned_case_type = case_type.rstrip('.')
        
        case_key = f"{cleaned_case_type}.{case_number}.{filing_year}"
        
        if case_key in self.mock_data:
            logger.info(f"Mock scraper: Found case '{case_key}'")
            return True, self.mock_data[case_key], ""
        else:
            logger.warning(f"Mock scraper: Case '{case_key}' not found in mock data.")
            return False, {}, "Case not found in the mock records. Please try another sample case."


def get_scraper(use_mock: bool = False):
    """
    Factory function to get the appropriate scraper instance.
    """
    if use_mock:
        logger.info("Using MockScraper for development and testing.")
        return MockScraper()
    else:
        logger.info("Using LIVE DelhiHighCourtScraper with Selenium.")
        return DelhiHighCourtScraper()
