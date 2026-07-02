import duckdb

con = duckdb.connect('fmcsa_search.duckdb', read_only=True)

print("=== BUSINESS_ORG_DESC (candidate for 'Entity Types') ===")
print(con.execute("""
    SELECT BUSINESS_ORG_DESC, COUNT(*) as count
    FROM raw_census
    GROUP BY BUSINESS_ORG_DESC
    ORDER BY count DESC
    LIMIT 20
""").df())

print("\n=== DOCKET1_STATUS_CODE (candidate for 'Operating Authority Status') ===")
print(con.execute("""
    SELECT DOCKET1_STATUS_CODE, COUNT(*) as count
    FROM raw_census
    GROUP BY DOCKET1_STATUS_CODE
    ORDER BY count DESC
    LIMIT 20
""").df())

print("\n=== TOTAL_CARS stats (candidate for 'Non-CMV Units') ===")
print(con.execute("""
    SELECT
        COUNT(*) as non_null_count,
        SUM(TOTAL_CARS) as total_sum,
        MIN(TOTAL_CARS) as min_val,
        MAX(TOTAL_CARS) as max_val,
        AVG(TOTAL_CARS) as avg_val
    FROM raw_census
    WHERE TOTAL_CARS IS NOT NULL
""").df())

print("\n=== POWER_UNITS stats (confirming SUM works) ===")
print(con.execute("""
    SELECT SUM(POWER_UNITS) as total_power_units
    FROM raw_census
""").df())

con.close()