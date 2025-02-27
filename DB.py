import sqlite3
import pandas as pd

DATABASE_FILE = "trades.sqlite"
TABLE_NAME = "epex_12_20_12_13"

def load_data_as_dataframe():
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(DATABASE_FILE)
        print("Connected to the database successfully.")

        # Load data into a Pandas DataFrame
        query = f"SELECT * FROM {TABLE_NAME}"
        df = pd.read_sql_query(query, conn)

        return df  # Returning the DataFrame for reuse

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None  # Return None if there's an error

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

    finally:
        if 'conn' in locals() and conn:
            conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    df = load_data_as_dataframe()
    if df is not None:
        print(df.head())  # Display the first few rows
