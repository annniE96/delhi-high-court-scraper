import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin
import logging
import json
import io
# New imports for the CAPTCHA solver
try:
    from PIL import Image, ImageEnhance, ImageFilter
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False


# Import the centralized mock data for the MockScraper
from sample_data import MOCK_CASES

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DelhiHighCourtScraper:
    """
    Scraper for fetching live case data from the Delhi High Court website.
    This class contains the logic to handle real web requests, including CAPTCHA solving.
    """
    def __init__(self):
        self.base_url = "https://delhihighcourt.nic.in"
        self.case_status_url = f"{self.base_url}/dhc_case_status_list_new.php"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        })
        if not TESSERACT_AVAILABLE:
            logger.warning("Pillow or Pytesseract is not installed. The live scraper's CAPTCHA solver will not work.")
            logger.warning("Install them with: pip install Pillow pytesseract")


    def _solve_captcha(self, captcha_image_url):
        """
        Downloads a CAPTCHA image, processes it, and uses Tesseract OCR to solve it.
        """
        if not TESSERACT_AVAILABLE:
            logger.error("Cannot solve CAPTCHA because required libraries are missing.")
            return None

        try:
            # Step 1: Download the CAPTCHA image
            logger.info(f"Downloading CAPTCHA from: {captcha_image_url}")
            response = self.session.get(captcha_image_url, stream=True, timeout=10)
            response.raise_for_status()
            
            # Step 2: Open the image using Pillow
            image = Image.open(io.BytesIO(response.content))

            # Step 3: Pre-process the image to make it easier for OCR to read
            # Convert to grayscale, increase contrast, and apply a threshold
            image = image.convert('L')  # Grayscale
            image = ImageEnhance.Contrast(image).enhance(2.0) # Increase contrast
            # Thresholding: pixels darker than 150 become black, others become white
            image = image.point(lambda x: 0 if x < 150 else 255, '1')

            # Optional: Save the processed image for debugging
            # image.save("captcha_processed.png")

            # Step 4: Use Pytesseract to perform OCR on the processed image
            # We configure it to recognize alphanumeric characters of a specific length
            custom_config = r'-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz --psm 7'
            captcha_text = pytesseract.image_to_string(image, config=custom_config)
            
            # Clean up the result
            captcha_text = re.sub(r'[^a-zA-Z0-9]', '', captcha_text).strip()
            
            logger.info(f"OCR Result: '{captcha_text}'")
            return captcha_text if len(captcha_text) > 3 else None # Return only if we get a reasonable result

        except Exception as e:
            logger.error(f"An error occurred during CAPTCHA solving: {e}")
            return None

    def search_case(self, case_type, case_number, filing_year, **kwargs):
        """
        Attempts to fetch real case details from the court website.
        """
        logger.info(f"Attempting LIVE scrape for: {case_type}/{case_number}/{filing_year}")
        
        # This is a placeholder. You would need to find all the correct codes.
        case_type_codes = {"W.P.(C)": "28", "CRL.A.": "8"}
        if case_type not in case_type_codes:
            return False, {}, f"Live scraper does not have the code for case type: {case_type}"

        # --- CAPTCHA Handling Logic ---
        # First, we need to visit the page to get the CAPTCHA image URL
        try:
            initial_response = self.session.get(self.case_status_url, timeout=20)
            initial_soup = BeautifulSoup(initial_response.text, 'html.parser')
            
            # Find the CAPTCHA image tag
            captcha_img = initial_soup.find('img', {'id': 'captcha_image'}) # Assuming it has an ID
            if not captcha_img:
                return False, {}, "Could not find the CAPTCHA image on the page."

            captcha_url = urljoin(self.base_url, captcha_img['src'])
            
            # Solve the CAPTCHA
            captcha_solution = self._solve_captcha(captcha_url)
            if not captcha_solution:
                return False, {}, "Failed to solve the CAPTCHA."

        except requests.RequestException as e:
            logger.error(f"Failed to load the initial page: {e}")
            return False, {}, "Could not connect to the court website to get CAPTCHA."

        # Now, submit the form with the CAPTCHA solution
        form_data = {
            'case_type': case_type_codes[case_type],
            'case_no': case_number,
            'case_year': filing_year,
            'captcha': captcha_solution, # Add the solved CAPTCHA
            'submit': 'Search'
        }

        try:
            response = self.session.post(self.case_status_url, data=form_data, timeout=20)
            response.raise_for_status()

            if "No Record Found" in response.text or "Invalid Captcha" in response.text:
                logger.warning("Live scraper: 'No Record Found' or 'Invalid Captcha' message on page.")
                return False, {}, "Case not found or CAPTCHA was incorrect."

            case_data = self._parse_response(response.text)
            return True, case_data, ""

        except requests.exceptions.RequestException as e:
            logger.error(f"Live scrape failed: {e}")
            return False, {}, "A network error occurred while contacting the court website."

    def _parse_response(self, html_content):
        # This remains a placeholder as before
        soup = BeautifulSoup(html_content, 'html.parser')
        parsed_data = {
            'case_title': 'Live Scrape Successful (Example)',
            'petitioner_name': 'Parsed Petitioner Name',
            'respondent_name': 'Parsed Respondent Name',
        }
        return parsed_data


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
        case_key = f"{case_type}.{case_number}.{filing_year}"
        
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
        logger.info("Using LIVE DelhiHighCourtScraper.")
        return DelhiHighCourtScraper()
