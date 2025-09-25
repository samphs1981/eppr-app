import sqlite3
import os

# --- Database File Path ---
# Builds a path to 'eppr.db' in the root of the project directory.
# This assumes the script is run from the project root (e.g., via main.py).
DB_FILE = "eppr.db"

def initialize_database():
    """
    Initializes the database by creating all necessary tables if they don't already exist.
    This function establishes the complete schema for the EPPR application.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        print("Successfully connected to SQLite database.")

        # --- Table Creation Queries ---
        # Each 'CREATE TABLE IF NOT EXISTS' query defines a table's structure,
        # including column names, data types, and constraints like PRIMARY KEYs
        # and FOREIGN KEYs to link tables together.

        # Master Data Tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS PHASE (
            phas_code TEXT PRIMARY KEY,
            phas_name TEXT NOT NULL
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS DISCIPLINE (
            disc_code TEXT PRIMARY KEY,
            disc_name TEXT NOT NULL,
            phas_code TEXT,
            FOREIGN KEY (phas_code) REFERENCES PHASE (phas_code)
        );
        ''')

        # MILESTONES_TYPE table updated: phas_code foreign key removed
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS MILESTONES_TYPE (
            ms_type_code TEXT PRIMARY KEY,
            ms_type_name TEXT NOT NULL
        );
        ''')
        
        # New REVISIONS table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS REVISIONS (
            rev_code TEXT PRIMARY KEY,
            rev_descrpt TEXT NOT NULL
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS USERROLES (
            role_id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT NOT NULL UNIQUE,
            permissions TEXT
        );
        ''')

        # Core Application Tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS USERS (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            role TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            department TEXT
        );
        ''')

        # WORKORDER table updated: phas_code foreign key removed
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS WORKORDER (
            proj_code TEXT PRIMARY KEY,
            proj_name TEXT NOT NULL,
            proj_status TEXT,
            proj_start_dt DATE,
            proj_finish_dt DATE
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS EWBS (
            ewbs_code TEXT PRIMARY KEY,
            ewbs_name TEXT NOT NULL,
            proj_code TEXT,
            phas_code TEXT,
            disc_code TEXT,
            FOREIGN KEY (proj_code) REFERENCES WORKORDER (proj_code),
            FOREIGN KEY (phas_code) REFERENCES PHASE (phas_code),
            FOREIGN KEY (disc_code) REFERENCES DISCIPLINE (disc_code)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS EWP (
            ewp_code TEXT PRIMARY KEY,
            ewp_name TEXT NOT NULL,
            ewp_bl_budg_unit REAL,
            ewp_fct_budg_unit REAL,
            ewbs_code TEXT,
            FOREIGN KEY (ewbs_code) REFERENCES EWBS (ewbs_code)
        );
        ''')

        # DVLB table updated: doc_rev removed
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS DVLB (
            doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_code TEXT NOT NULL UNIQUE,
            doc_title TEXT NOT NULL,
            doc_responsible TEXT,
            doc_bl_budg_unit REAL,
            doc_fct_budg_unit REAL,
            doc_fct_comments TEXT,
            ewp_code TEXT,
            FOREIGN KEY (ewp_code) REFERENCES EWP (ewp_code)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS MS_VALUE (
            ms_value_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ms_type_code TEXT,
            ms_value REAL,
            ms_value_name TEXT,
            ms_value_cum_wtg REAL,
            ms_value_seq_number INTEGER,
            FOREIGN KEY (ms_type_code) REFERENCES MILESTONES_TYPE (ms_type_code)
        );
        ''')
        
        # DVLBPROG table references the new REVISIONS table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS DVLBPROG (
            prog_id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_code TEXT,
            doc_rev TEXT,
            ms_type_code TEXT,
            ms_value_code TEXT,
            doc_progress REAL,
            doc_bl_budg_unit REAL,
            doc_fct_budg_unit REAL,
            doc_ev_units REAL,
            doc_act_date DATE,
            status_date DATE,
            FOREIGN KEY (doc_code) REFERENCES DVLB (doc_code),
            FOREIGN KEY (doc_rev) REFERENCES REVISIONS (rev_code),
            FOREIGN KEY (ms_type_code) REFERENCES MILESTONES_TYPE (ms_type_code)
        );
        ''')

        conn.commit()
        print("Database tables created/verified successfully.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # This allows the script to be run directly for setup/testing
    initialize_database()

