"""
Ingest match data from the football-data.org API.

Fetches all matches for selected competitions and seasons,
saving each raw JSON response untouched to data/raw/.
"""

import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
BASE_URL = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}

COMPETITIONS = ["PL", "PD", "BL1", "SA", "FL1"]  # top 5 European leagues
SEASONS = [2024, 2025]  # 2024-25 and 2025-26 seasons -> covers calendar year 2025

RAW_DIR = Path("data/raw")
SLEEP_SECONDS = 6.5  # free tier: 10 calls/min; 6.5s keeps us safely under


def fetch_matches(competition: str, season: int) -> dict:
    """Fetch all matches for one competition and season. Returns parsed JSON."""
    url = f"{BASE_URL}/competitions/{competition}/matches"
    response = requests.get(url, headers=HEADERS, params={"season": season}, timeout=30)
    response.raise_for_status()  # raises on 4xx/5xx instead of failing silently
    return response.json()


def save_raw(data: dict, competition: str, season: int) -> Path:
    """Save raw API response as JSON. Never modify raw data."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    filepath = RAW_DIR / f"{competition}_{season}_matches.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filepath


def main() -> None:
    for competition in COMPETITIONS:
        for season in SEASONS:
            print(f"Fetching {competition} season {season}...", end=" ")
            try:
                data = fetch_matches(competition, season)
                n_matches = len(data.get("matches", []))
                filepath = save_raw(data, competition, season)
                print(f"OK - {n_matches} matches -> {filepath}")
            except requests.exceptions.HTTPError as e:
                print(f"FAILED - {e}")
            time.sleep(SLEEP_SECONDS)


if __name__ == "__main__":
    main()