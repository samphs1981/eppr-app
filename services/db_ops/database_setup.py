import sqlite3
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(SCRIPT_DIR, '..', '..', 'db', 'eppr.db')

def initialize_database():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.execute('PRAGMA foreign_keys = ON;')  # enforce FKs
        cursor = conn.cursor()
        print(f"Successfully connected to SQLite database at: {DB_FILE}")

        # --- Parents first ---
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS grp (
            grp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            grp_code TEXT,
            grp_name TEXT NOT NULL
        );''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ms_type (
            ms_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ms_type_code TEXT,
            ms_type_name TEXT NOT NULL
        );''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS revision (
            revision_id INTEGER PRIMARY KEY AUTOINCREMENT,
            rev_code TEXT,
            rev_descrpt TEXT
        );''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS userroles (
            role_id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT NOT NULL UNIQUE,
            permissions TEXT
        );''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS project (
            proj_id INTEGER PRIMARY KEY AUTOINCREMENT,
            proj_code TEXT,
            proj_name TEXT NOT NULL,
            proj_status TEXT,
            proj_start_dt DATE,
            proj_finish_dt DATE
        );''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS discipline (
            discipline_id INTEGER PRIMARY KEY AUTOINCREMENT,
            grp_id INTEGER,
            disc_code TEXT,
            disc_name TEXT NOT NULL,
            FOREIGN KEY (grp_id) REFERENCES grp(grp_id)
        );''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS phase (
            phase_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            phase_code TEXT,
            phase_name TEXT NOT NULL,
            FOREIGN KEY (project_id) REFERENCES project(proj_id)
        );''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT UNIQUE,
            password_hash TEXT,
            full_name TEXT,
            role_id INTEGER,
            status TEXT,
            created_at TIMESTAMP,
            last_login TIMESTAMP,
            department TEXT,
            FOREIGN KEY (role_id) REFERENCES userroles(role_id)
        );''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ms_value (
            ms_value_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ms_type_id INTEGER NOT NULL,
            ms_value_code TEXT,
            ms_value_name TEXT NOT NULL,
            ms_value_cum_wtg REAL,
            ms_value_seq_number INTEGER,
            FOREIGN KEY (ms_type_id) REFERENCES ms_type(ms_type_id)
        );''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ewbs (
            ewbs_id INTEGER PRIMARY KEY AUTOINCREMENT,
            phase_id INTEGER,
            discipline_id INTEGER,
            ewbs_code TEXT,
            ewbs_name TEXT NOT NULL,
            FOREIGN KEY (discipline_id) REFERENCES discipline(discipline_id),
            FOREIGN KEY (phase_id) REFERENCES phase(phase_id)
        );''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ewp (
            ewp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ewbs_id INTEGER NOT NULL,
            ewp_code TEXT,
            ewp_name TEXT NOT NULL,
            ewp_bl_budg_unit REAL,
            ewp_fct_budg_unit REAL,
            FOREIGN KEY (ewbs_id) REFERENCES ewbs(ewbs_id)
        );''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS dvlb (
            doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ewp_id INTEGER NOT NULL,
            doc_code TEXT NOT NULL UNIQUE,
            doc_name TEXT NOT NULL,
            doc_type TEXT,
            doc_responsible INTEGER,
            doc_bl_budg_unit REAL,
            doc_fct_budg_unit REAL,
            doc_fcst_comments TEXT,
            FOREIGN KEY (ewp_id) REFERENCES ewp(ewp_id),
            FOREIGN KEY (doc_responsible) REFERENCES users(user_id)
        );''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS dvlbprog (
            prog_id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id INTEGER NOT NULL,
            rev_id INTEGER,
            ms_type_id INTEGER,
            ms_value_id INTEGER,
            doc_code TEXT,
            doc_progress REAL,
            doc_bl_budg_unit REAL,
            doc_fct_budg_unit REAL,
            doc_earned_val REAL,
            doc_pln_date DATE,
            doc_act_date DATE,
            doc_status_date DATE,
            FOREIGN KEY (doc_id) REFERENCES dvlb(doc_id),
            FOREIGN KEY (rev_id) REFERENCES revision(revision_id),
            FOREIGN KEY (ms_type_id) REFERENCES ms_type(ms_type_id),
            FOREIGN KEY (ms_value_id) REFERENCES ms_value(ms_value_id)
        );''')

        # Indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_project_code ON project(proj_code);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ewp_code ON ewp(ewp_code);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_dvlb_code ON dvlb(doc_code);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_dvlbprog_doc_date ON dvlbprog(doc_id, doc_status_date);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ms_value_type ON ms_value(ms_type_id, ms_value_seq_number);')

        conn.commit()
        print("Database tables and indexes created/verified successfully.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    initialize_database()
