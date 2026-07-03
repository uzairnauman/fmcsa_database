import base64
import os
import duckdb
import pandas as pd
import streamlit as st
import datetime
import time

# --- ADD THIS TO THE VERY TOP OF THE FILE ---
if "page_start_time" not in st.session_state:
    st.session_state.page_start_time = time.perf_counter()
else:
    st.session_state.page_start_time = time.perf_counter()

# Set up page configurations
st.set_page_config(page_title="FMCSA Trucking Companies Lead", page_icon="🛣️", layout="wide")

# Path to your DuckDB output file
DB_URL = "https://huggingface.co/datasets/uzairnauman96/fmcsa_Search/resolve/main/fmcsa_search.duckdb"

# Routes queries through the attached remote database reference
TARGET_TABLE = "remote_db.main.mart_carrier_search"

@st.cache_resource
def get_connection():
    # 1. Start an in-memory client
    con = duckdb.connect()
    
    # 2. Initialize the HTTPS network extensions
    con.execute("INSTALL httpfs;")
    con.execute("LOAD httpfs;")
    
    # 3. Mount the Hugging Face file as a read-only alias
    con.execute(f"ATTACH '{DB_URL}' AS remote_db (READ_ONLY);")
    
    return con

# Initialize connection instance
con = get_connection()


# ---------- Design system (highway signage inspired) ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght=500;600;700&family=Inter:wght=400;500;600&family=IBM+Plex+Mono:wght=400;500&display=swap');

:root {
    --highway-green: #0B4D3A;
    --highway-green-dark: #083828;
    --signal-amber: #F2A03D;
    --asphalt: #1A1D1F;
    --paper: #FAF9F6;
    --line: #E3E0D8;
    --white: #FFFFFF;
    --muted: #6B6862;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: var(--paper);
}

#MainMenu, footer, header {visibility: hidden;}

.block-container {
    padding-top: 3rem;
    max-width: 950px;
}

/* ---- Shield logo ---- */
.shield-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 2rem;
    margin-bottom: 2.5rem;
}

.brand-title {
    font-family: 'Oswald', sans-serif;
    font-weight: 600;
    font-size: 2.1rem;
    color: var(--asphalt);
    letter-spacing: 0.5px;
    text-align: center;
}

.brand-sub {
    font-family: 'Inter', sans-serif;
    font-size: 0.92rem;
    color: var(--muted);
    text-align: center;
    margin-top: 0.15rem;
    letter-spacing: 0.2px;
}

/* ---- Search input ---- */
div[data-testid="stTextInput"] input {
    border-radius: 999px !important;
    border: 1.5px solid var(--line) !important;
    padding: 0.85rem 1.4rem !important;
    font-size: 1.02rem !important;
    font-family: 'Inter', sans-serif;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

div[data-testid="stTextInput"] input:focus {
    border-color: var(--highway-green) !important;
    box-shadow: 0 0 0 3px rgba(11,77,58,0.12) !important;
}

/* ---- Buttons ---- */
.stButton button {
    border-radius: 999px;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.92rem;
    border: none;
    padding: 0.55rem 1.6rem;
}

.stButton button[kind="primary"] {
    background-color: var(--highway-green);
}

.stButton button[kind="primary"]:hover {
    background-color: var(--highway-green-dark);
}

/* ---- Empty state ---- */
.empty-state {
    text-align: center;
    margin-top: 3.5rem;
    color: var(--muted);
}

.empty-state-icon {
    font-size: 2.2rem;
    margin-bottom: 0.6rem;
    opacity: 0.5;
}

.empty-state-title {
    font-family: 'Oswald', sans-serif;
    font-size: 1.15rem;
    color: var(--asphalt);
    font-weight: 500;
    margin-bottom: 0.3rem;
}

.empty-state-sub {
    font-size: 0.9rem;
    color: var(--muted);
    max-width: 420px;
    margin: 0 auto;
    line-height: 1.5;
}

/* ---- Result count strip ---- */
.result-strip {
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
    margin: 1.6rem 0 1rem 0;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid var(--line);
}

.result-count {
    font-family: 'Oswald', sans-serif;
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--asphalt);
}

.result-label {
    font-size: 0.88rem;
    color: var(--muted);
}

div[data-testid="stDataFrame"] {
    font-family: 'IBM Plex Mono', monospace;
}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_connection():
    # 1. Open an empty, in-memory connection
    con = duckdb.connect()
    
    # 2. Install and load the HTTPS file streaming extension
    con.execute("INSTALL httpfs;")
    con.execute("LOAD httpfs;")
    
    # 3. Mount the Hugging Face file as a read-only alias
    con.execute(f"ATTACH '{DB_URL}' AS remote_db (READ_ONLY);")
    
    return con


@st.cache_data
def get_distinct_statuses(_con):
    # Change from FROM mart_carrier_search to using the TARGET_TABLE variable
    result = _con.execute(f"""
        SELECT DISTINCT "Status"
        FROM {TARGET_TABLE}
        WHERE "Status" IS NOT NULL
        ORDER BY "Status"
    """).fetchall()
    return [row[0] for row in result]

@st.cache_data
def get_distinct_states(_con):
    result = _con.execute(f"""
        SELECT DISTINCT "Physical State"
        FROM {TARGET_TABLE}
        WHERE "Physical State" IS NOT NULL
        ORDER BY "Physical State"
    """).fetchall()
    return [row[0] for row in result]


@st.cache_data
def get_distinct_scopes(_con):
    result = _con.execute(f"""
        SELECT DISTINCT "Operating Scope"
        FROM {TARGET_TABLE}
        WHERE "Operating Scope" IS NOT NULL
        ORDER BY "Operating Scope"
    """).fetchall()
    return [row[0] for row in result]

@st.cache_data
def get_distinct_structures(_con):
    result = _con.execute(f"""
        SELECT DISTINCT "Business Structure"
        FROM {TARGET_TABLE}
        WHERE "Business Structure" IS NOT NULL
        ORDER BY "Business Structure"
    """).fetchall()
    return [row[0] for row in result]

@st.cache_data
def get_fleet_size_brackets(_con):
    result = _con.execute(f"""
        SELECT DISTINCT "Fleet Size Bracket"
        FROM {TARGET_TABLE}
        WHERE "Fleet Size Bracket" IS NOT NULL
        ORDER BY "Fleet Size Bracket"
    """).fetchall()
    return [row[0] for row in result]

con = get_connection()

if "has_searched" not in st.session_state:
    st.session_state.has_searched = False

# ---------- Logo rendering fallback mechanics ----------
logo_path = os.path.join(os.path.dirname(__file__), "image.png")
if os.path.exists(logo_path):
    with open(logo_path, "rb") as img:
        logo = base64.b64encode(img.read()).decode()
    logo_html = f'<img class="logo" style="width: 500px; height: auto; display: block; margin: 0 auto;" src="data:image/png;base64,{logo}">'
else:
    logo_html = '<div style="font-size: 40px; text-align:center;">🛣️</div>'


st.markdown(f"""
<div class="shield-wrap">
{logo_html}
<div>
<div class="brand-title">Carrier & Entity Hub</div>
<div class="brand-sub">Comprehensive multi-status tracking powered by FMCSA Company Census data</div>
</div>
</div>
""", unsafe_allow_html=True)

# ---------- Primary search panel ----------
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    company_name = st.text_input(
        "Search",
        placeholder="Search by company name, dba, or USDOT Number",
        label_visibility="collapsed",
    )

# ---------- Horizontal Dropdown Dropdowns ----------
f1, f2, f3, f4 = st.columns([1, 1, 1, 1])

with f1:
    status_filter = st.selectbox(
        "Status",
        options=["All"] + get_distinct_statuses(con)
    )

with f2:
    scope_filter = st.selectbox(
        "Operating Scope",
        options=["All"] + get_distinct_scopes(con)
    )

with f3:
    structure_filter = st.selectbox(
        "Business Structure",
        options=["All"] + get_distinct_structures(con)
    )

with f4:
    fleetsize = st.multiselect(
        "Fleet Size Bracket",
        options=get_fleet_size_brackets(con)
    )

# ---------- Geographical Vectors ----------
g1, g2, g3 = st.columns([1.5, 1, 1.5])

with g1:
    city = st.text_input("Physical City", placeholder="e.g., Sunnyvale")

with g2:
    state = st.selectbox("Physical State", options=["All"] + get_distinct_states(con))

with g3:
    zip_code = st.text_input("Physical ZIP Code", placeholder="e.g., 94086")


# ---------- Multi-Select Commodity Filters ----------
cargo_options = {
    "General Freight": "Flag: General Freight",
    "Household Goods": "Flag: Household Goods",
    "Metal Sheets": "Flag: Metal Sheets",
    "Motor Vehicles": "Flag: Motor Vehicles",
    "Driveaway Towaway": "Flag: Driveaway Towaway",
    "Logs and Poles": "Flag: Logs and Poles",
    "Building Materials": "Flag: Building Materials",
    "Mobile Homes": "Flag: Mobile Homes",
    "Large Machinery": "Flag: Large Machinery",
    "Fresh Produce": "Flag: Fresh Produce",
    "Liquids and Gases": "Flag: Liquids and Gases",
    "Intermodal Containers": "Flag: Intermodal Containers",
    "Passenger Transport": "Flag: Passenger Transport",
    "Oilfield Equipment": "Flag: Oilfield Equipment",
    "Livestock": "Flag: Livestock",
    "Grain and Feed": "Flag: Grain and Feed",
    "Coal and Coke": "Flag: Coal and Coke",
    "Meat Products": "Flag: Meat Products",
    "Waste Management": "Flag: Waste Management",
    "US Mail Contracting": "Flag: US Mail Contracting",
    "Chemicals": "Flag: Chemicals",
    "Dry Bulk Commodities": "Flag: Dry Bulk Commodities",
    "Cold Chain Food": "Flag: Cold Chain Food",
    "Beverage Distribution": "Flag: Beverage Distribution",
    "Paper Products": "Flag: Paper Products",
    "Utility Fleet Support": "Flag: Utility Fleet Support"
}

selected_cargo = st.multiselect(
    "Select Cargo Classifications",
    options=list(cargo_options.keys())
)

# ---------- Metric Range Sliders & Indicators ----------
m1, m2 = st.columns([1, 1])

with m1:
    power_units_min, power_units_max = st.slider("Power Units Range", 0, 500, (0, 500))

with m2:
    hazmat_choice = st.radio("Hazmat Fleet Designation", options=["All", "Hazmat Only", "Non-Hazmat Only"], horizontal=True)


# ---------- Search Button ----------
search_clicked = st.button(
    "Query Registry",
    type="primary",
    use_container_width=True
)

if search_clicked:
    st.session_state.has_searched = True

# ---------- Default Landing State ----------
if not st.session_state.has_searched:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">🚛</div>
        <div class="empty-state-title">Data-warehouse Integrated Carrier Sourcing</div>
        <div class="empty-state-sub">
            Query across active, pending, or inactive commercial entities. 
            Track operational configurations across Power Units and Commodity matrices.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------- Dynamic SQL Query Assembly Execution ----------
else:
    where_clauses = []
    params = []

    if company_name:
        if company_name.isdigit():
            where_clauses.append('"USDOT Number" = ?')
            params.append(int(company_name))
        else:
            where_clauses.append('(LOWER("Company Name") LIKE LOWER(?) OR LOWER("DBA Name") LIKE LOWER(?))')
            like_term = f"%{company_name}%"
            params.extend([like_term, like_term])

    if status_filter != "All":
        where_clauses.append('"Status" = ?')
        params.append(status_filter)

    if scope_filter != "All":
        where_clauses.append('"Operating Scope" = ?')
        params.append(scope_filter)

    if structure_filter != "All":
        where_clauses.append('"Business Structure" = ?')
        params.append(structure_filter)

    if fleetsize:
        placeholders = ",".join(["?"] * len(fleetsize))
        where_clauses.append(f'"Fleet Size Bracket" IN ({placeholders})')
        params.extend(fleetsize)

    if city:
        where_clauses.append('LOWER("State Location City") LIKE LOWER(?)')
        params.append(f"%{city}%")

    if state != "All":
        where_clauses.append('"Physical State" = ?')
        params.append(state)

    if zip_code:
        where_clauses.append('"Physical ZIP Code" LIKE ?')
        params.append(f"%{zip_code}%")

    if hazmat_choice == "Hazmat Only":
        where_clauses.append('"Hazmat Flag" = \'Y\'')
    elif hazmat_choice == "Non-Hazmat Only":
        where_clauses.append('"Hazmat Flag" = \'N\'')

    # Append active Multi-select cargo matrix selections
    for cargo in selected_cargo:
        db_column = cargo_options[cargo]
        where_clauses.append(f'"{db_column}" = TRUE')

    # Apply Power Units bounds
    where_clauses.append('"Power Units Count" BETWEEN ? AND ?')
    params.extend([power_units_min, power_units_max])

    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

    
    # 1. Update your count_query to look like this (add the 'f' prefix and use {TARGET_TABLE}):
    count_query = f'SELECT COUNT(*) FROM {TARGET_TABLE} WHERE {where_sql}'
    total_count = con.execute(count_query, params).fetchone()[0]
    # Securely fetch the count assertion without letting a network timeout crash the app
    try:
        count_result = con.execute(count_query, params).fetchone()
        total_count = count_result[0] if count_result else 0
    except Exception as e:
        # Fallback to 0 if the network stream blips during the count aggregation
        total_count = 0

    # 2. Update your main results query right below it to look like this:
    query = f"""
        SELECT
            "USDOT Number",
            "Company Name",
            "Status",
            "Operating Scope",
            "Entity Operations",
            "Business Structure",
            "Fleet Size Bracket",
            "Power Units Count",
            "Office Phone",    
            "Mobile Phone",       
            "Corporate Email",    
            "Physical State",
            "System Entry Date"
        FROM {TARGET_TABLE}
        WHERE {where_sql}
        ORDER BY "System Entry Date" DESC
        LIMIT 200
    """
    results = con.execute(query, params).df()
    
    # Fetch data safely into dataframes
    try:
    results = con.execute(query, params).df()
except Exception as e:
    st.error(f"Query failed: {e}")
    results = pd.DataFrame()

    # 1. Display the matching count strip (Only ONCE)
    st.markdown(f"""
    <div class="result-strip">
        <span class="result-count">{total_count:,}</span>
        <span class="result-label">matching entities found{' — viewing top 200 records' if total_count > 200 else ''}</span>
    </div>
    """, unsafe_allow_html=True)

    # 2. SAFE CHECK: Render the data grid or the empty state fallback cleanly
    if results is None or results.empty or len(results) == 0:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">🔍</div>
            <div class="empty-state-title">No technical records found matching criteria</div>
            <div class="empty-state-sub">Broaden parameters, clear active state filters, or reset the equipment metric intervals.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Render table results safely
        results["System Entry Date"] = pd.to_datetime(results["System Entry Date"]).dt.strftime('%Y-%m-%d')
        st.dataframe(results, use_container_width=True, hide_index=True)

        # Export Button
        csv = results.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Export Results Metadata to CSV",
            data=csv,
            file_name="fmcsa_clean_leads.csv",
            mime="text/csv",
            use_container_width=True
        )

# --- ADD THIS TO THE ABSOLUTE BOTTOM OF YOUR APP.PY (NO INDENTATION) ---
page_end_time = time.perf_counter()
total_app_latency = page_end_time - st.session_state.page_start_time

# Only show the telemetry box if the user has actually pressed search
if st.session_state.get("has_searched", False):
    st.markdown("---")
    with st.sidebar: # This moves it out of your table UI entirely and sticks it in the sidebar!
        st.subheader("🛠️ FinOps Telemetry")
        
        telemetry_payload = {
    "Latency (seconds)": round(total_app_latency, 4),
    "Results Returned": len(df),
    "Search Query": company_name,
    "State Filter": state,
    "City Filter": city,
}
