import duckdb

con = duckdb.connect('fmcsa_search.duckdb', read_only=True)

count = con.execute("SELECT COUNT(*) FROM mart_carrier_search").fetchone()
print(f"Total active, authorized-for-hire carriers: {count[0]:,}")

sample = con.execute("""
    SELECT legal_name, physical_city, physical_state, physical_zip,
           fleetsize_range, date_added
    FROM mart_carrier_search
    WHERE physical_zip = '90001'
    LIMIT 5
""").df()
print(sample)

con.close()