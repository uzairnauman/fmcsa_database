import duckdb

con = duckdb.connect('fmcsa_search.duckdb', read_only=True)

print("=== Breakdown by STATUS_CODE ===")
print(con.execute("""
    SELECT status_code, COUNT(*) as count
    FROM stg_carriers
    GROUP BY status_code
    ORDER BY count DESC
""").df())

print("\n=== Breakdown by CARRIER_OPERATION ===")
print(con.execute("""
    SELECT carrier_operation, COUNT(*) as count
    FROM stg_carriers
    GROUP BY carrier_operation
    ORDER BY count DESC
""").df())

print("\n=== Breakdown: Active carriers only, by CARRIER_OPERATION ===")
print(con.execute("""
    SELECT carrier_operation, COUNT(*) as count
    FROM stg_carriers
    WHERE status_code = 'A'
    GROUP BY carrier_operation
    ORDER BY count DESC
""").df())

con.close()