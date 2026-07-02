Carrier & Entity Hub: Serverless FMCSA Search Engine
A high-performance, cost-effective, serverless logistics dashboard designed to search, filter, and analyze massive United States Federal Motor Carrier Safety Administration (FMCSA) Company Census data in real time.

By leveraging an embedded OLAP architecture, this application streams and queries gigabytes of compressed data directly over the internet without requiring an expensive, always-on cloud database cluster—reducing infrastructure maintenance and operational costs to $0/month.

👉 Live Application Link: https://fmcsadatabase-uzairnauman.streamlit.app/

🏗️ Architecture & Data Pipeline Blueprint
The project transitions a massive raw dataset into a lightweight, zero-infra production environment:

Extraction & Seeding: Raw FMCSA company census files are stored, structured, and managed via version control.

Transformation (dbt): Data is cleaned, typed, and structured using analytics engineering best practices. Features like fleet sizes are segmented into actionable brackets.

Storage (Hugging Face): The final dbt mart (mart_carrier_search) is exported into a highly compressed, columnar .duckdb format and hosted on the cloud.

Serverless Execution Layer (DuckDB + Streamlit): When a user triggers a query, the application uses the DuckDB httpfs extension to stream only the requested data slices over HTTPS, resulting in sub-second query execution without downloading the database file.

🛠️ Tech Stack & Core Engineering Components
Query Engine: DuckDB (Embedded OLAP engine utilizing zero-copy network file streaming)

Transformation & Modeling: dbt (Data Build Tool) for clean, staging-to-mart modular SQL transformations

Application Framework: Streamlit (Python)

Data Storage Backend: Hugging Face Storage (Columnar object hosting)

Environment & Package Management: Python 3.11+, Pandas

🌟 Key Engineering Features
1. Serverless Object Storage Mounting
Instead of running a heavy relational database instance, the application mounts remote storage directly at the application layer, optimizing lookups through an initialized memory footprint:

Dynamically installs and loads the httpfs network file streaming extension.

Attaches the remote Hugging Face file as a read-only database alias (remote_db).

2. Defensive Network Programming & Fault Tolerance
To guarantee a robust enterprise UI, the application implements hardened database access layers:

Anti-Crash Schema Wrappers: Encapsulates row aggregations and data fetches in decoupled try/except syntax blocks. If an unmapped filter or network jitter returns an empty cursor, the app falls back elegantly to a structured empty state instead of raising a NoneType exception.

Smart Input Sanitation: Automatically handles user inputs (such as trailing spaces or numerical formatting differences in ZIP codes) through flexible LIKE %query% SQL parameterization.

3. Decoupled UI State Caching
Uses @st.cache_resource to maintain a persistent network connection across user sessions.

Uses @st.cache_data to pre-aggregate dropdown filters (Status, Operating Scope, States), ensuring that immediate UI interactions load instantaneously from cache memory rather than re-querying the network stream.

📂 Repository Structure
Plaintext
├── fmcsa_search/
│   ├── models/
│   │   ├── staging/        # Source declarations and initial casting
│   │   ├── intermediate/   # Field transformations and logic cleaning
│   │   └── marts/          # Optimized analytical tables built for the frontend
│   ├── app.py              # Main Streamlit application and query execution engine
│   ├── dbt_project.yml     # dbt compilation configurations
│   └── image.png           # Custom branding and UI assets
├── .gitignore              # Multi-tier ignore configuration to exclude massive files
├── requirements.txt        # Production python dependencies
└── README.md               # Documentation
🚀 Local Deployment Setup
To run this dashboard locally, clone the repository and configure your local environment:

1. Clone the Repository
Bash
git clone https://github.com/uzairnauman/fmcsa_database.git
cd fmcsa_database
2. Set Up a Virtual Environment & Install Dependencies
Bash
# Create environment
python -m venv env

# Activate environment (Windows)
source env/Scripts/activate

# Install required packages
pip install -r requirements.txt
3. Run the App
Bash
streamlit run fmcsa_search/app.py
The application will automatically initialize, load the network streaming extensions, pull metadata filters from the cloud, and spin up on your local host environment!
