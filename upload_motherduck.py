import duckdb

# 1. Define your token and paths
token = "motherduck token"
local_db_path = r"E:\Trucking_Dashboard\fmcsa_search.duckdb"

# Note: The 'r' before the string is a "raw string" in Python. 
# It prevents Windows backslashes (\) from causing errors.

print("Connecting to MotherDuck...")
# 2. Open a connection directly to MotherDuck
con = duckdb.connect(f"md:?motherduck_token={token}")

print(f"Uploading local database {local_db_path} to MotherDuck cloud...")
# 3. Create the cloud database by cloning your local database file
con.execute(f"CREATE DATABASE fmcsa_search FROM '{local_db_path}';")

print("Successfully uploaded! Your entire local database is now in the MotherDuck cloud.")
