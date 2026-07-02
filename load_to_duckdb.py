"""
Loads the downloaded census CSV into a local DuckDB file as a raw table,
then prints basic diagnostics: row count, column names/types, and a
sample of rows. This is a standalone sanity check before wiring dbt
around it.
"""

import duckdb
import glob
import os

DB_PATH = "fmcsa_search.duckdb"
RAW_DIR = "data/raw"


def get_latest_csv():
    files = sorted(glob.glob(os.path.join(RAW_DIR, "census_*.csv")))
    if not files:
        raise FileNotFoundError(f"No census_*.csv files found in {RAW_DIR}")
    return files[-1]


def load_and_inspect():
    csv_path = get_latest_csv()
    print(f"Loading: {csv_path}")

    con = duckdb.connect(DB_PATH)

    con.execute(f"""
        CREATE OR REPLACE TABLE raw_census AS
        SELECT * FROM read_csv_auto('{csv_path}', sample_size=-1)
    """)

    row_count = con.execute("SELECT COUNT(*) FROM raw_census").fetchone()[0]
    print(f"\nRows loaded: {row_count:,}")

    print("\nColumns:")
    schema = con.execute("DESCRIBE raw_census").fetchall()
    for col_name, col_type, *_ in schema:
        print(f"  {col_name}: {col_type}")

    print("\nSample rows:")
    sample = con.execute("SELECT * FROM raw_census LIMIT 3").df()
    print(sample)

    con.close()
    print(f"\nDone. Data loaded into {DB_PATH} as table 'raw_census'.")


if __name__ == "__main__":
    load_and_inspect()