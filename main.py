import sys
import os

# --- System Path Setup ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

# --- Imports ---
# Import the functions directly from their respective modules
from services.db_ops.database_setup import initialize_database
from services.db_ops.populate_master_data import populate_phase_table
from tests.db_tests.db_test import get_table_as_dataframe

def main():
    """
    Main function to run the application setup and data retrieval.
    """
    print("--- Starting EPPR Application ---")

    # Step 1: Initialize the database (creates tables if they don't exist)
    #initialize_database()
    
    # Step 2: Populate master data tables (adds initial rows)
    #populate_phase_table()
    
    # Step 3: Fetch and display data from a table as a DataFrame
    print("\n--- Retrieving Data ---")
    phase_df = get_table_as_dataframe("PHASE")
    
    if phase_df is not None:
        print("\nContents of 'PHASE' table:")
        print(phase_df)
    
    print("\n--- EPPR App finished. ---")

if __name__ == "__main__":
    main()

