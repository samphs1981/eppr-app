import sqlite3
import os

# --- Database File Path ---
# Builds a path to 'eppr.db' in the root of the project directory.
DB_FILE = "eppr.db"

def populate_phase_table():
    """
    Inserts initial master data into the PHASE table.
    Uses 'INSERT OR IGNORE' to prevent errors if the data already exists.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        print("\nPopulating PHASE table with initial data...")

        # --- Data for PHASE table ---
        # List of tuples, where each tuple represents a row to be inserted.
        phases = [
            ('PM', 'Project Management'),
            ('ENG', 'Engineering'),
            ('DES', 'Design'),
            ('PROC', 'Procurement'),
            ('CON', 'Construction'),
            ('COMM', 'Commissioning')
        ]

        # Use 'INSERT OR IGNORE' to avoid errors on subsequent runs.
        # This will only insert rows where the primary key (phas_code) does not already exist.
        cursor.executemany('INSERT OR IGNORE INTO PHASE (phas_code, phas_name) VALUES (?, ?)', phases)

        conn.commit()
        
        # Verify the insertion
        inserted_rows = cursor.rowcount
        if inserted_rows > 0:
            print(f"  Successfully inserted {inserted_rows} new rows into PHASE.")
        else:
            print("  PHASE table already contains data. No new rows were added.")

    except sqlite3.Error as e:
        print(f"Database error during data population: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # This allows the script to be run directly for populating the data
    populate_phase_table()
