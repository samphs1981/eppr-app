import sqlite3
import os
import pandas as pd
# --- Database File Path ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(SCRIPT_DIR, '..', '..', 'db', 'eppr.db')

def populate_grp_data():
    """
    Populates all master data tables with initial values.
    This function is designed to be run after the database schema is created.
    """
    print("--- Starting master data population ---")
    
    if not os.path.exists(DB_FILE):
        print(f"Database file not found at {DB_FILE}. Please run database_setup first.")
        return

    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # --- Populate 'grp' table ---
        groups_data = [
            ('MGT', 'Management'),
            ('ENG', 'Engineering'),
            ('DES', 'Design'),
            ('PROC', 'Procurement'),
            ('CON', 'Construction'),
            ('COMM', 'Commissioning')
        ]
        
        added_count = 0
        for grp_code, grp_name in groups_data:
            # First, check if a group with this code already exists to avoid duplicates
            cursor.execute("SELECT 1 FROM grp WHERE grp_code = ?", (grp_code,))
            if cursor.fetchone() is None:
                # If it doesn't exist, insert it
                cursor.execute('INSERT INTO grp (grp_code, grp_name) VALUES (?, ?)', (grp_code, grp_name))
                added_count += 1
        
        print(f"Populated 'grp' table. Added {added_count} new rows.")

        # --- You can add functions to populate other tables here ---
        # Example: populate_disciplines(cursor)
        # Example: populate_phases(cursor)

        conn.commit()
        print("--- Master data population finished successfully. ---")

    except sqlite3.Error as e:
        print(f"Database error during data population: {e}")
    finally:
        if conn:
            conn.close()


def populate_disciplines_from_dataframe(df):
    """
    Populates the discipline table from a pandas DataFrame.
    It handles the foreign key relationship by looking up the grp_id from the grp_code.

    Args:
        df (pd.DataFrame): A DataFrame that must contain 'grp_code', 'disc_code', and 'disc_name' columns.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # First, fetch the grp_ids and store them in a dictionary for easy lookup.
        cursor.execute("SELECT grp_code, grp_id FROM grp")
        grp_code_to_id = {code: id for code, id in cursor.fetchall()}

        added_count = 0
        skipped_count = 0

        # Iterate through the DataFrame rows
        for index, row in df.iterrows():
            grp_code = row['grp_code']
            disc_code = row['disc_code']
            disc_name = row['disc_name']

            grp_id = grp_code_to_id.get(grp_code)  # Look up the foreign key ID

            if grp_id:
                # CORRECTED CHECK: Verify if the disc_code already exists *for this specific group*.
                cursor.execute("SELECT 1 FROM discipline WHERE grp_id = ? AND disc_code = ?", (grp_id, disc_code,))
                if cursor.fetchone() is None:
                    cursor.execute(
                        'INSERT INTO discipline (grp_id, disc_code, disc_name) VALUES (?, ?, ?)',
                        (grp_id, disc_code, disc_name)
                    )
                    added_count += 1
                else:
                    skipped_count += 1 # Already exists for this group
            else:
                print(f"Warning: grp_code '{grp_code}' not found in 'grp' table. Skipping discipline '{disc_name}'.")
                skipped_count += 1
        
        conn.commit()
        print(f"Processed disciplines from DataFrame. Added: {added_count}, Skipped: {skipped_count}")

    except (sqlite3.Error, KeyError) as e:
        print(f"An error occurred while populating disciplines from DataFrame: {e}")
    finally:
        if conn:
            conn.close()

