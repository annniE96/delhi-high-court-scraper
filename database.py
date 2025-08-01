import sqlite3
import json
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_path='data/court_data.db'):
        self.db_path = db_path
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dictionary-like access
        return conn
    
    def initialize_database(self):
        """Create database tables if they don't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create queries table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    case_type TEXT NOT NULL,
                    case_number TEXT NOT NULL,
                    filing_year TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    ip_address TEXT,
                    user_agent TEXT
                )
            ''')
            
            # Create responses table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_id INTEGER,
                    raw_response TEXT,
                    parsed_data TEXT,
                    status TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    error_message TEXT,
                    FOREIGN KEY (query_id) REFERENCES queries (id)
                )
            ''')
            
            # Create case_data table for structured storage
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS case_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_id INTEGER,
                    case_number TEXT,
                    case_type TEXT,
                    filing_year TEXT,
                    petitioner_name TEXT,
                    respondent_name TEXT,
                    filing_date TEXT,
                    next_hearing_date TEXT,
                    case_status TEXT,
                    judge_name TEXT,
                    court_hall TEXT,
                    pdf_links TEXT,  -- JSON array of PDF links
                    last_order_date TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (query_id) REFERENCES queries (id)
                )
            ''')
            
            conn.commit()
    
    def log_query(self, case_type, case_number, filing_year, ip_address=None, user_agent=None):
        """Log a search query and return the query ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO queries (case_type, case_number, filing_year, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?)
            ''', (case_type, case_number, filing_year, ip_address, user_agent))
            conn.commit()
            return cursor.lastrowid
    
    def log_response(self, query_id, response_data, status, error_message=None, raw_response=None):
        """Log the response for a query"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Store response in responses table
            cursor.execute('''
                INSERT INTO responses (query_id, raw_response, parsed_data, status, error_message)
                VALUES (?, ?, ?, ?, ?)
            ''', (query_id, raw_response, json.dumps(response_data), status, error_message))
            
            # If successful and we have structured data, store in case_data table
            if status == 'success' and response_data:
                cursor.execute('''
                    INSERT INTO case_data (
                        query_id, case_number, case_type, filing_year,
                        petitioner_name, respondent_name, filing_date,
                        next_hearing_date, case_status, judge_name,
                        court_hall, pdf_links, last_order_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    query_id,
                    response_data.get('case_number', ''),
                    response_data.get('case_type', ''),
                    response_data.get('filing_year', ''),
                    response_data.get('petitioner_name', ''),
                    response_data.get('respondent_name', ''),
                    response_data.get('filing_date', ''),
                    response_data.get('next_hearing_date', ''),
                    response_data.get('case_status', ''),
                    response_data.get('judge_name', ''),
                    response_data.get('court_hall', ''),
                    json.dumps(response_data.get('pdf_links', [])),
                    response_data.get('last_order_date', '')
                ))
            
            conn.commit()
    
    def get_query_history(self, limit=50):
        """Get recent query history"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT q.*, r.status, r.timestamp as response_time
                FROM queries q
                LEFT JOIN responses r ON q.id = r.query_id
                ORDER BY q.timestamp DESC
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()
    
    def get_case_data_by_query_id(self, query_id):
        """Get structured case data by query ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM case_data WHERE query_id = ?
            ''', (query_id,))
            return cursor.fetchone()
    
    def search_cases(self, case_number=None, case_type=None, petitioner_name=None):
        """Search for cases in the database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM case_data WHERE 1=1"
            params = []
            
            if case_number:
                query += " AND case_number LIKE ?"
                params.append(f"%{case_number}%")
            
            if case_type:
                query += " AND case_type = ?"
                params.append(case_type)
            
            if petitioner_name:
                query += " AND petitioner_name LIKE ?"
                params.append(f"%{petitioner_name}%")
            
            query += " ORDER BY timestamp DESC LIMIT 100"
            
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def get_stats(self):
        """Get database statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            stats = {}
            
            # Total queries
            cursor.execute("SELECT COUNT(*) FROM queries")
            stats['total_queries'] = cursor.fetchone()[0]
            
            # Successful queries
            cursor.execute("SELECT COUNT(*) FROM responses WHERE status = 'success'")
            stats['successful_queries'] = cursor.fetchone()[0]
            
            # Failed queries
            cursor.execute("SELECT COUNT(*) FROM responses WHERE status = 'failed'")
            stats['failed_queries'] = cursor.fetchone()[0]
            
            # Most searched case types
            cursor.execute('''
                SELECT case_type, COUNT(*) as count 
                FROM queries 
                GROUP BY case_type 
                ORDER BY count DESC 
                LIMIT 5
            ''')
            stats['top_case_types'] = cursor.fetchall()
            
            return stats