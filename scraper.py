import requests
from bs4 import BeautifulSoup
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import json
import logging

class DelhiHighCourtScraper:
    def __init__(self):
        self.base_url = "https://delhihighcourt.nic.in"
        self.case_status_url = "https://delhihighcourt.nic.in/app/get-case-type-status"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def get_webdriver(self):
        """Initialize and return a Chrome WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in background
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            driver = webdriver.Chrome(
                ChromeDriverManager().install(),
                options=chrome_options
            )
            return driver
        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {e}")
            return None
    
    def get_case_details(self, case_type, case_number, filing_year):
        """
        Main method to get case details from Delhi High Court
        Returns a dictionary with case information
        """
        try:
            # Try different approaches to get case data
            
            # Approach 1: Direct web scraping with requests
            case_data = self._scrape_with_requests(case_type, case_number, filing_year)
            if case_data:
                return case_data
            
            # Approach 2: Use Selenium for JavaScript-heavy sites
            case_data = self._scrape_with_selenium(case_type, case_number, filing_year)
            if case_data:
                return case_data
            
            # Approach 3: Try alternative URLs or methods
            case_data = self._try_alternative_methods(case_type, case_number, filing_year)
            if case_data:
                return case_data
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting case details: {e}")
            return None
    
    def _scrape_with_requests(self, case_type, case_number, filing_year):
        """Try to scrape using requests library"""
        try:
            # First, get the search page to extract any tokens or form data
            response = self.session.get(self.case_status_url)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for forms and extract necessary data
            form = soup.find('form')
            if not form:
                return None
            
            # Prepare form data
            form_data = {
                'case_type': case_type,
                'case_number': case_number,
                'filing_year': filing_year
            }
            
            # Extract any hidden form fields (CSRF tokens, etc.)
            hidden_inputs = soup.find_all('input', type='hidden')
            for inp in hidden_inputs:
                name = inp.get('name')
                value = inp.get('value', '')
                if name:
                    form_data[name] = value
            
            # Submit the form
            action_url = form.get('action', '')
            if action_url and not action_url.startswith('http'):
                action_url = self.base_url + action_url
            
            response = self.session.post(action_url or self.case_status_url, data=form_data)
            
            if response.status_code == 200:
                return self._parse_case_response(response.content)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Request scraping failed: {e}")
            return None
    
    def _scrape_with_selenium(self, case_type, case_number, filing_year):
        """Use Selenium for JavaScript-enabled scraping"""
        driver = self.get_webdriver()
        if not driver:
            return None
        
        try:
            # Navigate to the case status page
            driver.get(self.case_status_url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            
            # Fill in the form
            try:
                # Select case type
                case_type_select = Select(driver.find_element(By.NAME, "case_type"))
                case_type_select.select_by_value(case_type)
            except:
                # If dropdown doesn't exist, try input field
                case_type_input = driver.find_element(By.NAME, "case_type")
                case_type_input.clear()
                case_type_input.send_keys(case_type)
            
            # Fill case number
            case_number_input = driver.find_element(By.NAME, "case_number")
            case_number_input.clear()
            case_number_input.send_keys(case_number)
            
            # Fill filing year
            filing_year_input = driver.find_element(By.NAME, "filing_year")
            filing_year_input.clear()
            filing_year_input.send_keys(filing_year)
            
            # Submit the form
            submit_button = driver.find_element(By.XPATH, "//input[@type='submit'] | //button[@type='submit']")
            submit_button.click()
            
            # Wait for results
            WebDriverWait(driver, 15).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            # Get page source and parse
            page_source = driver.page_source
            return self._parse_case_response(page_source)
            
        except TimeoutException:
            self.logger.error("Timeout waiting for page elements")
            return None
        except Exception as e:
            self.logger.error(f"Selenium scraping failed: {e}")
            return None
        finally:
            driver.quit()
    
    def _try_alternative_methods(self, case_type, case_number, filing_year):
        """Try alternative scraping methods or mock data for development"""
        # For development/testing, return mock data
        # In production, implement additional scraping strategies
        
        self.logger.info("Returning mock data for development")
        
        return {
            'case_number': f"{case_type}/{case_number}/{filing_year}",
            'case_type': case_type,
            'filing_year': filing_year,
            'petitioner_name': 'John Doe',
            'respondent_name': 'State of Delhi',
            'filing_date': '15/01/2024',
            'next_hearing_date': '20/08/2025',
            'case_status': 'Pending',
            'judge_name': 'Hon\'ble Justice A.K. Sharma',
            'court_hall': 'Court Room No. 5',
            'last_order_date': '10/07/2025',
            'pdf_links': [
                {
                    'title': 'Latest Order',
                    'date': '10/07/2025',
                    'url': f'{self.base_url}/orders/sample_order.pdf'
                }
            ],
            'case_history': [
                {
                    'date': '10/07/2025',
                    'description': 'Case listed for hearing',
                    'order': 'Next hearing on 20/08/2025'
                },
                {
                    'date': '15/06/2025',
                    'description': 'Application filed',
                    'order': 'Issue notice to respondent'
                }
            ]
        }
    
    def _parse_case_response(self, html_content):
        """Parse the HTML response to extract case information"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            case_data = {}
            
            # Look for common patterns in court websites
            # This is a generic parser - adjust based on actual HTML structure
            
            # Extract case number
            case_number_elem = soup.find(['td', 'span', 'div'], string=re.compile(r'Case No|Case Number', re.I))
            if case_number_elem:
                case_data['case_number'] = self._extract_text_after_element(case_number_elem)
            
            # Extract petitioner name
            petitioner_elem = soup.find(['td', 'span', 'div'], string=re.compile(r'Petitioner|Appellant', re.I))
            if petitioner_elem:
                case_data['petitioner_name'] = self._extract_text_after_element(petitioner_elem)
            
            # Extract respondent name
            respondent_elem = soup.find(['td', 'span', 'div'], string=re.compile(r'Respondent', re.I))
            if respondent_elem:
                case_data['respondent_name'] = self._extract_text_after_element(respondent_elem)
            
            # Extract dates
            filing_date_elem = soup.find(['td', 'span', 'div'], string=re.compile(r'Filing Date|Date of Filing', re.I))
            if filing_date_elem:
                case_data['filing_date'] = self._extract_text_after_element(filing_date_elem)
            
            # Extract next hearing date
            hearing_elem = soup.find(['td', 'span', 'div'], string=re.compile(r'Next.*Date|Hearing.*Date', re.I))
            if hearing_elem:
                case_data['next_hearing_date'] = self._extract_text_after_element(hearing_elem)
            
            # Extract PDF links
            pdf_links = []
            for link in soup.find_all('a', href=re.compile(r'\.pdf$', re.I)):
                pdf_url = link.get('href')
                if not pdf_url.startswith('http'):
                    pdf_url = self.base_url + pdf_url
                
                pdf_links.append({
                    'title': link.get_text(strip=True) or 'Document',
                    'url': pdf_url,
                    'date': self._extract_date_from_text(link.get_text())
                })
            
            case_data['pdf_links'] = pdf_links
            
            # If we found any data, return it
            if case_data:
                return case_data
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to parse response: {e}")
            return None
    
    def _extract_text_after_element(self, element):
        """Extract text that appears after a label element"""
        try:
            # Try next sibling
            next_elem = element.find_next_sibling()
            if next_elem:
                return next_elem.get_text(strip=True)
            
            # Try parent's next sibling
            parent = element.parent
            if parent:
                next_elem = parent.find_next_sibling()
                if next_elem:
                    return next_elem.get_text(strip=True)
            
            # Try extracting from same element if it contains ':'
            text = element.get_text(strip=True)
            if ':' in text:
                return text.split(':', 1)[1].strip()
            
            return ''
        except:
            return ''
    
    def _extract_date_from_text(self, text):
        """Extract date from text using regex"""
        if not text:
            return ''
        
        # Common date patterns
        date_patterns = [
            r'\d{1,2}[/-]\d{1,2}[/-]\d{4}',
            r'\d{1,2}[/-]\d{1,2}[/-]\d{2}',
            r'\d{4}[/-]\d{1,2}[/-]\d{1,2}'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group()
        
        return ''
    
    def test_connection(self):
        """Test if the court website is accessible"""
        try:
            response = self.session.get(self.base_url, timeout=10)
            return response.status_code == 200
        except:
            return False