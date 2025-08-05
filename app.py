import os
import logging
import json
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from werkzeug.middleware.proxy_fix import ProxyFix
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

# Import from your actual project files
from database import DatabaseManager
from scraper import get_scraper
from sample_data import CASE_TYPES, MOCK_CASES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "a-strong-dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

db_manager = DatabaseManager()
db_manager.initialize_database()

# --- This is the main switch for your application ---
# Set to True to use your reliable mock data (for development and demonstration)
# Set to False to attempt a live scrape against the real court website
USE_MOCK_SCRAPER = True 

@app.route('/')
def index():
    """Renders the main page with the case search form."""
    return render_template('index.html', case_types=CASE_TYPES, mock_cases=MOCK_CASES)

@app.route('/search', methods=['POST'])
def search_case():
    """Handles the form submission and displays case details."""
    try:
        case_type = request.form.get('case_type', '').strip()
        case_number = request.form.get('case_number', '').strip()
        filing_year = request.form.get('filing_year', '').strip()

        if not all([case_type, case_number, filing_year]):
            flash('All fields (case type, case number, filing year) are required.', 'warning')
            return redirect(url_for('index'))

        query_id = db_manager.log_query(
            case_type=case_type,
            case_number=case_number,
            filing_year=filing_year,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')
        )
        
        # The get_scraper function will now return either the MockScraper or the DelhiHighCourtScraper
        # based on the USE_MOCK_SCRAPER flag above.
        scraper = get_scraper(use_mock=USE_MOCK_SCRAPER)
        
        success, case_data, error_message = scraper.search_case(
            case_type=case_type, 
            case_number=case_number, 
            filing_year=filing_year
        )
        
        db_manager.log_response(
            query_id=query_id,
            response_data=case_data,
            status='success' if success else 'failed',
            error_message=error_message if not success else None,
            raw_response=json.dumps(case_data) if case_data else None
        )
        
        if success:
            return render_template('results.html', case_data=case_data)
        else:
            flash(error_message, 'danger')
            return redirect(url_for('index'))
            
    except Exception as e:
        logger.error(f"An unexpected error occurred in /search: {e}", exc_info=True)
        flash('An internal server error occurred. Please try again later.', 'danger')
        return redirect(url_for('index'))

@app.route('/download_pdf/<case_key>')
def download_pdf(case_key):
    """Generate and download a mock PDF for the case"""
    try:
        case_data = MOCK_CASES.get(case_key)
        if not case_data:
            flash('Case not found for PDF generation.', 'error')
            return redirect(url_for('index'))

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        p.setFont("Helvetica-Bold", 16)
        p.drawString(inch, height - inch, "DELHI HIGH COURT - CASE DETAILS")

        p.setFont("Helvetica", 12)
        y = height - inch * 1.5
        
        details = [
            ("Case Title:", case_data.get('case_title', 'N/A')),
            ("Case Number:", case_data.get('case_number', 'N/A')),
            ("Case Type:", case_data.get('case_type', 'N/A')),
            ("Filing Date:", case_data.get('filing_date', 'N/A')),
            ("Petitioner:", case_data.get('petitioner_name', 'N/A')),
            ("Respondent:", case_data.get('respondent_name', 'N/A')),
            ("Next Hearing:", case_data.get('next_hearing_date', 'N/A')),
            ("Status:", case_data.get('case_status', 'N/A')),
        ]
        
        for label, value in details:
            p.drawString(inch, y, f"{label} {value}")
            y -= 20
        
        p.save()
        buffer.seek(0)
        
        response = make_response(buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=case_{case_key.replace(".", "_")}.pdf'
        
        logger.info(f"PDF generated for case: {case_key}")
        return response
        
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        flash('An error occurred while generating the PDF. Please try again.', 'error')
        return redirect(url_for('index'))


@app.errorhandler(404)
def not_found_error(error):
    return "Page Not Found", 404

@app.errorhandler(500)
def internal_error(error):
    return "Internal Server Error", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
