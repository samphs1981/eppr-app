import sqlite3
import os
import sys
import pandas as pd

# --- Path Setup ---
# This adjusts the Python path to allow this script to find the database file
# located in the project's root directory. It goes up three levels from
# db_tests -> tests -> eppr_app.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)
DB_PATH = os.path.join(PROJECT_ROOT, "eppr.db")

# --- Expected Schema Definition ---
# This dictionary defines what the database structure *should* look like.
# We will test the actual database against this definition.
EXPECTED_SCHEMA = {
    "PHASE": ["phas_code", "phas_name"],
    "DISCIPLINE": ["disc_code", "disc_name", "phas_code"],
    "MILESTONES_TYPE": ["ms_type_code", "ms_type_name", "phas_code"],
    "MS_VALUE": ["ms_value_id", "ms_type_code", "ms_value", "ms_value_name", "ms_value_cum_wtg", "ms_value_seq_number"],
    "WORKORDER": ["proj_code", "proj_name", "proj_status", "proj_start_dt", "proj_finish_dt", "phas_code"],
    "EWBS": ["ewbs_code", "ewbs_name", "proj_code", "phas_code", "disc_code"],
    "EWP": ["ewp_code", "ewp_name", "ewp_bl_budg_unit", "ewp_fct_budg_unit", "ewbs_code"],
    "DVLB": ["doc_id", "doc_code", "doc_title", "doc_rev", "doc_responsible", "doc_bl_budg_unit", "doc_fct_budg_unit", "doc_fct_budg_comments", "ewp_code"],
    "DVLBPROG": ["prog_id", "doc_code", "doc_rev", "ms_type_code", "ms_value_code", "doc_progress", "doc_bl_budg_unit", "doc_fct_budg_unit", "doc_ev_units", "doc_act_date", "status_date"],
    "USERS": ["user_id", "username", "email", "password_hash", "full_name", "role", "status", "created_at", "last_login", "department"],
    "USERROLES": ["role_id", "role_name", "permissions"],
}

def get_table_as_dataframe(table_name):
    """
    Connects to the database, reads a full table, and returns it as a pandas DataFrame.

    Args:
        table_name (str): The name of the table to retrieve.

    Returns:
        pandas.DataFrame: A DataFrame containing the table's data, or None if an
                          error occurs or the table doesn't exist.
    """
    print(f"\n--- Fetching table '{table_name}' as DataFrame ---")
    if not os.path.exists(DB_PATH):
        print(f"ERROR: Database file not found at '{DB_PATH}'")
        return None

    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        # Use pandas to directly read the SQL query into a DataFrame
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if conn:
            conn.close()

def run_db_tests():
    """
    Connects to the database and verifies that the schema matches the
    expected structure defined in EXPECTED_SCHEMA.
    """
    print("--- Running Database Schema Verification Test ---")
    
    if not os.path.exists(DB_PATH):
        print(f"ERROR: Database file not found at '{DB_PATH}'")
        return

    conn = None
    all_tests_passed = True
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 1. Test if all expected tables exist
        print("\n[TEST 1] Verifying table existence...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        # Filter out the internal 'sqlite_sequence' table from the results
        actual_tables = {row[0] for row in cursor.fetchall() if row[0] != 'sqlite_sequence'}
        expected_tables = set(EXPECTED_SCHEMA.keys())

        if actual_tables == expected_tables:
            print("  \u2705 SUCCESS: All expected tables exist.")
        else:
            all_tests_passed = False
            missing = expected_tables - actual_tables
            extra = actual_tables - expected_tables
            if missing:
                print(f"  \u274C FAILED: Missing tables: {', '.join(missing)}")
            if extra:
                print(f"  \u274C FAILED: Found unexpected tables: {', '.join(extra)}")

        # 2. Test if each table has the correct columns
        print("\n[TEST 2] Verifying columns for each table...")
        for table_name, expected_columns in EXPECTED_SCHEMA.items():
            if table_name not in actual_tables:
                continue # Skip column check if table is missing
                
            cursor.execute(f"PRAGMA table_info({table_name});")
            # The column name is the second item (index 1) in each row
            actual_columns = {row[1] for row in cursor.fetchall()}
            expected_columns_set = set(expected_columns)

            if actual_columns == expected_columns_set:
                print(f"  \u2705 SUCCESS: Table '{table_name}' has correct columns.")
            else:
                all_tests_passed = False
                missing = expected_columns_set - actual_columns
                extra = actual_columns - expected_columns_set
                print(f"  \u274C FAILED: Schema mismatch for table '{table_name}':")
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
        print(" కొన్ని పరీక్షలు విఫలమయ్యాయి. దయచేసి ఎర్రర్‌లను సమీక్షించండి. (Some tests failed. Please review the errors.)")


if __name__ == "__main__":
    # First, run the schema verification tests
    run_db_tests()

    # --- Example usage of the new function ---
    # Now, fetch the 'PHASE' table and display it
    phase_df = get_table_as_dataframe("PHASE")
    if phase_df is not None:
        print("Successfully retrieved 'PHASE' table:")
        print(phase_df)

