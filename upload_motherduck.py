import duckdb

# 1. Define your token and paths
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InV6YWlybmF1bWFuMTdAZ21haWwuY29tIiwibWRSZWdpb24iOiJhd3MtdXMtd2VzdC0yIiwic2Vzc2lvbiI6InV6YWlybmF1bWFuMTcuZ21haWwuY29tIiwicGF0IjoiVmhwOTU2WVM5V25odk1zQUY0OWh4b3JXbUd0UFVlUUp0Sy1zdGVqRmVxUSIsInVzZXJJZCI6IjI1N2MwNjJjLWFmYjEtNDFhNS1iZGE1LTNlOWIxMzJmZDdkNiIsImlzcyI6Im1kX3BhdCIsInJlYWRPbmx5IjpmYWxzZSwidG9rZW5UeXBlIjoicmVhZF93cml0ZSIsImlhdCI6MTc4Mjk1NDA1NH0.Q22UZrNCrzctgWH3HD5FvKYmbHg0Aq8FlkZi12QtH90"
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