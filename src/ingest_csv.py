"""
Download historical odds CSVs from football-data.co.uk.

Files contain match results plus closing odds from multiple bookmakers.
Saved untouched to data/raw/ alongside the API JSONs.
"""

import time
from pathlib import Path

import requests

BASE_URL = "https://www.football-data.co.uk/mmz4281"

# CSV league codes -> our API competition codes (needed later for joining)
LEAGUES = {
    "E0": "PL",    # Premier League
    "SP1": "PD",   # La Liga
    "D1": "BL1",   # Bundesliga
    "I1": "SA",    # Serie A
    "F1": "FL1",   # Ligue 1
}
SEASONS = ["2425", "2526"]

RAW_DIR = Path("data/raw")


def download_csv(season: str, league_code: str) -> Path:
    """Download one season file, save raw bytes untouched."""
    url = f"{BASE_URL}/{season}/{league_code}.csv"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    filepath = RAW_DIR / f"odds_{league_code}_{season}.csv"
    filepath.write_bytes(response.content)  # bytes, not text: no encoding guesses at ingest
    return filepath


def main() -> None:
    for season in SEASONS:
        for league_code, api_code in LEAGUES.items():
            print(f"Downloading {league_code} ({api_code}) season {season}...", end=" ")
            try:
                filepath = download_csv(season, league_code)
                size_kb = filepath.stat().st_size / 1024
                print(f"OK - {size_kb:.0f} KB -> {filepath}")
            except requests.exceptions.RequestException as e:
                print(f"FAILED - {e}")
            time.sleep(1)  # courtesy delay; no documented rate limit


if __name__ == "__main__":
    main()