import sqlite3
import os
import pandas as pd

# --- Database File Path ---
# This calculates the correct, absolute path to the database file,
# ensuring the script can find it regardless of where it's run from.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(SCRIPT_DIR, '..', '..', 'db', 'eppr.db')

# This dictionary defines the expected structure of the database.
# It's based on your latest schema with integer primary keys.
EXPECTED_SCHEMA = {
    'grp': ['grp_id', 'grp_code', 'grp_name'],
    'discipline': ['discipline_id', 'grp_id', 'disc_code', 'disc_name'],
    'ms_type': ['ms_type_id', 'ms_type_code', 'ms_type_name'],
    'revision': ['revision_id', 'rev_code', 'rev_descrpt'],
    'userroles': ['role_id', 'role_name', 'permissions'],
    'project': ['proj_id', 'proj_code', 'proj_name', 'proj_status', 'proj_start_dt', 'proj_finish_dt'],
    'phase': ['phase_id', 'project_id', 'phase_code', 'phase_name'],
    'users': ['user_id', 'username', 'email', 'password_hash', 'full_name', 'role_id', 'status', 'created_at', 'last_login', 'department'],
    'ms_value': ['ms_value_id', 'ms_type_id', 'ms_value_code', 'ms_value_name', 'ms_value_cum_wtg', 'ms_value_seq_number'],
    'ewbs': ['ewbs_id', 'phase_id', 'discipline_id', 'ewbs_code', 'ewbs_name'],
    'ewp': ['ewp_id', 'ewbs_id', 'ewp_code', 'ewp_name', 'ewp_bl_budg_unit', 'ewp_fct_budg_unit'],
    'dvlb': ['doc_id', 'ewp_id', 'doc_code', 'doc_name', 'doc_type', 'doc_responsible', 'doc_bl_budg_unit', 'doc_fct_budg_unit', 'doc_fcst_comments'],
    'dvlbprog': ['prog_id', 'doc_id', 'rev_id', 'ms_type_id', 'ms_value_id', 'doc_code', 'doc_progress', 'doc_bl_budg_unit', 'doc_fct_budg_unit', 'doc_earned_val', 'doc_pln_date', 'doc_act_date', 'doc_status_date']
}

def test_database_schema():
    """
    Connects to the database and verifies that the schema matches the EXPECTED_SCHEMA.
    """
    print("--- Running Database Schema Verification Test ---")
    
    if not os.path.exists(DB_FILE):
        print(f"❌ FAILED: Database file not found at '{DB_FILE}'")
        return

    conn = None
    all_tests_passed = True
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Test 1: Verify table existence
        print("\n[TEST 1] Verifying table existence...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        db_tables = {row[0] for row in cursor.fetchall() if row[0] != 'sqlite_sequence'}
        expected_tables = set(EXPECTED_SCHEMA.keys())
        
        if db_tables == expected_tables:
            print("  ✅ SUCCESS: All expected tables are present.")
        else:
            all_tests_passed = False
            missing = expected_tables - db_tables
            extra = db_tables - expected_tables
            if missing:
                print(f"  ❌ FAILED: Missing tables: {', '.join(missing)}")
            if extra:
                print(f"  ❌ FAILED: Found unexpected tables: {', '.join(extra)}")

        # Test 2: Verify columns for each table
        print("\n[TEST 2] Verifying columns for each table...")
        for table_name, expected_columns in EXPECTED_SCHEMA.items():
            if table_name in db_tables:
                cursor.execute(f"PRAGMA table_info({table_name});")
                db_columns = {row[1] for row in cursor.fetchall()}
                expected_columns_set = set(expected_columns)
                
                if db_columns == expected_columns_set:
                    print(f"  ✅ SUCCESS: Table '{table_name}' has correct columns.")
                else:
                    all_tests_passed = False
                    missing = expected_columns_set - db_columns
                    extra = db_columns - expected_columns_set
                    print(f"  ❌ FAILED: Schema mismatch for table '{table_name}':")
                    if missing:
                        print(f"    - Missing columns: {', '.join(missing)}")
                    if extra:
                        print(f"    - Found unexpected columns: {', '.join(extra)}")
    
    except sqlite3.Error as e:
        all_tests_passed = False
        print(f"\nDatabase error during testing: {e}")
    finally:
        if conn:
            conn.close()

    print("\n--- Test Summary ---")
    if all_tests_passed:
        print("🎉 All database schema tests passed successfully!")
    else:
        print("❌ Some tests failed. Please review the errors above.")

def get_table_as_dataframe(table_name):
    """
    Retrieves a specific table and returns it as a pandas DataFrame.
    """
    if not os.path.exists(DB_FILE):
        print(f"Database file not found at {DB_FILE}")
        return None
        
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        df = pd.read_sql_query(f'SELECT * FROM "{table_name}"', conn)
        return df
    except Exception as e:
        print(f"An error occurred while fetching table '{table_name}': {e}")
        return None
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    test_database_schema()

