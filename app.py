from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime
from scraper import DelhiHighCourtScraper
from database import DatabaseManager

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this in production

# Initialize database
db_manager = DatabaseManager()
scraper = DelhiHighCourtScraper()

@app.route('/')
def index():
    """Main page with the search form"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_case():
    """Handle case search requests"""
    try:
        # Get form data
        case_type = request.form.get('case_type')
        case_number = request.form.get('case_number')
        filing_year = request.form.get('filing_year')
        
        # Validate input
        if not all([case_type, case_number, filing_year]):
            flash('All fields are required', 'error')
            return redirect(url_for('index'))
        
        # Log the query
        query_id = db_manager.log_query(case_type, case_number, filing_year)
        
        # Scrape case data
        case_data = scraper.get_case_details(case_type, case_number, filing_year)
        
        if case_data:
            # Log successful response
            db_manager.log_response(query_id, case_data, 'success')
            return render_template('results.html', case_data=case_data)
        else:
            # Log failed response
            db_manager.log_response(query_id, {}, 'failed')
            flash('Case not found or unable to fetch data. Please check case details.', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/case-types')
def get_case_types():
    """API endpoint to get available case types"""
    case_types = [
        {'value': 'CRL', 'text': 'Criminal Appeal'},
        {'value': 'CRA', 'text': 'Criminal Revision'},
        {'value': 'BAIL', 'text': 'Bail Application'},
        {'value': 'W.P.(C)', 'text': 'Writ Petition (Civil)'},
        {'value': 'W.P.(CRL)', 'text': 'Writ Petition (Criminal)'},
        {'value': 'FAO', 'text': 'First Appeal from Order'},
        {'value': 'CS(OS)', 'text': 'Civil Suit (Original Side)'},
        {'value': 'MAC APP', 'text': 'Motor Accident Claims Appeal'},
        {'value': 'CRP', 'text': 'Civil Revision Petition'},
        {'value': 'MAT.APP', 'text': 'Matrimonial Appeal'}
    ]
    return jsonify(case_types)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    flash('Internal server error. Please try again later.', 'error')
    return render_template('index.html'), 500

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Initialize database tables
    db_manager.initialize_database()
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)