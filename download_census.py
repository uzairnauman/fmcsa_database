"""
Downloads the FMCSA Company Census File (full CSV export) from the
DOT Open Data Portal and saves it locally, streaming to disk to
avoid loading the whole ~4.46M row file into memory at once.
"""

import os
import time
import requests

CENSUS_URL = "https://data.transportation.gov/api/v3/views/az4n-8mr2/export.csv?accessType=DOWNLOAD"
RAW_DIR = "data/raw"


def download_census_file():
    os.makedirs(RAW_DIR, exist_ok=True)
    today = time.strftime("%Y-%m-%d")
    filepath = os.path.join(RAW_DIR, f"census_{today}.csv")

    print(f"Starting download to {filepath} ...")

    with requests.get(CENSUS_URL, stream=True, timeout=600) as response:
        response.raise_for_status()
        total_bytes = 0
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
                if chunk:
                    f.write(chunk)
                    total_bytes += len(chunk)

    print(f"Done. Downloaded {total_bytes / (1024 * 1024):.1f} MB to {filepath}")
    return filepath


if __name__ == "__main__":
    download_census_file()