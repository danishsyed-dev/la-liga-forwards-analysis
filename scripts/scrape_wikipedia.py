#!/usr/bin/env python3
"""
Wikipedia Scraper — Extracts La Liga awards and honours data.

Scrapes structured tables from Wikipedia for:
  - Pichichi Trophy (La Liga top scorer each season)
  - Ballon d'Or winners and podium finishers
  - La Liga Best Player / Alfredo Di Stéfano Trophy
  - La Liga title winners (to map team achievements to players)
  - Champions League winners

Uses requests + BeautifulSoup (Wikipedia explicitly allows scraping).

Usage:
    python scripts/scrape_wikipedia.py           # Scrape all award categories
    python scripts/scrape_wikipedia.py --only pichichi ballon_dor

Output:
    data/raw/wikipedia/<category>.json
"""

import argparse
import json
import logging
import re
import sys
import time
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import RAW_WIKI_DIR, WIKI_URLS, USER_AGENT

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml",
}


def _fetch_page(url: str) -> BeautifulSoup:
    """Fetch a Wikipedia page and return parsed HTML."""
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "lxml")


def _clean_text(text: str) -> str:
    """Remove citation markers like [1], (4th), etc."""
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"\[note \d+\]", "", text)
    text = re.sub(r"\[a\]", "", text)
    return text.strip()


# ──────────────────────── Pichichi Trophy ────────────────────────

def scrape_pichichi() -> list[dict]:
    """
    Scrape Pichichi Trophy (La Liga top scorer) winners from Wikipedia.
    Returns list of {season, player, team, goals}.

    Wikipedia table columns: Season | Player(s) | Club(s) | Apps | Goals | Ratio
    When a season has multiple winners, the Season cell uses rowspan and
    subsequent rows are missing the season column (shifting other columns left).
    """
    log.info("Scraping Pichichi Trophy winners...")
    url = WIKI_URLS["pichichi"]
    soup = _fetch_page(url)

    records = []

    # Find the first wikitable that has "Season" in its first header cell
    tables = soup.find_all("table", {"class": "wikitable"})
    for table in tables:
        first_headers = table.find_all("th")
        header_texts = [th.get_text(strip=True).lower() for th in first_headers[:6]]
        if "season" not in header_texts:
            continue

        # This is our target table — parse all data rows
        rows = table.find_all("tr")[1:]  # skip the header row
        current_season = ""
        season_rowspan_remaining = 0

        for row in rows:
            cells = row.find_all(["td", "th"])
            if len(cells) < 3:
                continue

            cell_texts = [_clean_text(c.get_text()) for c in cells]

            # Determine if this row has its own season cell or inherits from rowspan
            if season_rowspan_remaining > 0:
                # This row is a continuation — no season cell, columns shift left
                # cell_texts: [Player, Club, Apps, Goals, Ratio]
                season_rowspan_remaining -= 1
                player_idx = 0
            else:
                # This row has its own season cell
                current_season = cell_texts[0]
                # Check if this season cell has rowspan
                rowspan = cells[0].get("rowspan")
                if rowspan:
                    season_rowspan_remaining = int(rowspan) - 1
                player_idx = 1

            if len(cell_texts) <= player_idx + 2:
                continue

            player = cell_texts[player_idx]
            team = cell_texts[player_idx + 1]

            # Goals are at player_idx + 3 (skipping Apps at player_idx + 2)
            goals_idx = player_idx + 3
            goals_str = cell_texts[goals_idx] if goals_idx < len(cell_texts) else "0"
            goals = int(re.sub(r"[^\d]", "", goals_str or "0") or 0)

            # Remove parenthetical counts like "(2)" from player names
            player = re.sub(r"\s*\(\d+\)\s*$", "", player).strip()

            if player and current_season:
                records.append({
                    "season": current_season,
                    "player": player,
                    "team": team,
                    "goals": goals,
                    "award": "La Liga Golden Boot",
                })

        log.info(f"  Parsed {len(records)} rows from first matching table")
        break  # Use first matching table only

    log.info(f"  Found {len(records)} Pichichi Trophy records")
    return records


# ──────────────────────── Ballon d'Or ────────────────────────

def scrape_ballon_dor() -> list[dict]:
    """
    Scrape Ballon d'Or winners and podium (top 3) from Wikipedia.
    Returns list of {year, player, placement, team}.

    Wikipedia table columns: Year | Rank | Player | Team | Points
    """
    log.info("Scraping Ballon d'Or winners...")
    url = WIKI_URLS["ballon_dor"]
    records = []

    try:
        soup = _fetch_page(url)

        # Find the large table with Year/Rank/Player headers
        tables = soup.find_all("table", {"class": "wikitable"})
        for table in tables:
            header_cells = table.find_all("th")
            header_texts = [th.get_text(strip=True).lower() for th in header_cells[:6]]
            if "year" not in header_texts or "player" not in header_texts:
                continue

            # Found the right table — parse rows
            rows = table.find_all("tr")[1:]
            current_year = ""
            placement_map = {"1": "Ballon d'Or Win", "2": "Ballon d'Or 2nd Place", "3": "Ballon d'Or 3rd Place"}

            for row in rows:
                cells = row.find_all(["td", "th"])
                if len(cells) < 3:
                    continue

                cell_texts = [_clean_text(c.get_text()) for c in cells]

                # Determine which cell is which — handle rowspan for Year
                idx = 0
                # If first cell has a rowspan or is a th, it's the year
                if cells[0].get("rowspan") or (cells[0].name == "th" and cell_texts[0].isdigit()):
                    current_year = cell_texts[0]
                    idx = 1
                elif cell_texts[0].isdigit() and len(cell_texts[0]) == 4:
                    current_year = cell_texts[0]
                    idx = 1

                if len(cell_texts) <= idx + 1:
                    continue

                rank = cell_texts[idx].strip() if idx < len(cell_texts) else ""
                player = cell_texts[idx + 1].strip() if idx + 1 < len(cell_texts) else ""
                team = cell_texts[idx + 2].strip() if idx + 2 < len(cell_texts) else ""

                # Only keep rank 1, 2, 3
                rank_clean = re.sub(r"[^\d]", "", rank)
                award = placement_map.get(rank_clean)

                if award and player and current_year:
                    records.append({
                        "year": current_year,
                        "player": player,
                        "placement": int(rank_clean),
                        "team": team,
                        "award": award,
                    })

            log.info(f"  Parsed {len(records)} rows from Ballon d'Or table")
            break  # Use first matching table

    except Exception as e:
        log.warning(f"  Error scraping Ballon d'Or: {e}")

    log.info(f"  Found {len(records)} Ballon d'Or records")
    return records


# ──────────────────────── La Liga Best Player ────────────────────────

def scrape_la_liga_best_player() -> list[dict]:
    """Scrape La Liga Best Player / Alfredo Di Stéfano Trophy winners."""
    log.info("Scraping La Liga Best Player awards...")
    url = WIKI_URLS["la_liga_best_player"]
    records = []

    try:
        soup = _fetch_page(url)
        html_str = str(soup)
        dfs = pd.read_html(html_str)
        for df in dfs:
            cols_lower = [str(c).lower() for c in df.columns]
            has_season = any("season" in c or "year" in c for c in cols_lower)
            has_player = any("winner" in c or "player" in c for c in cols_lower)

            if has_season and has_player:
                for _, row in df.iterrows():
                    season_val = ""
                    player_val = ""
                    team_val = ""
                    for col in df.columns:
                        cl = str(col).lower()
                        val = _clean_text(str(row[col]))
                        if "season" in cl or "year" in cl:
                            season_val = val
                        elif "winner" in cl or "player" in cl:
                            player_val = val
                        elif "club" in cl or "team" in cl:
                            team_val = val

                    if player_val and player_val != "nan" and season_val:
                        records.append({
                            "season": season_val,
                            "player": player_val,
                            "team": team_val,
                            "award": "La Liga Best Player Award",
                        })
    except Exception as e:
        log.warning(f"  Error scraping La Liga Best Player: {e}")

    log.info(f"  Found {len(records)} La Liga Best Player records")
    return records


# ──────────────────────── La Liga Title Winners ────────────────────────

def scrape_la_liga_titles() -> list[dict]:
    """
    Scrape La Liga championship winners by season from
    https://en.wikipedia.org/wiki/List_of_Spanish_football_champions

    Table columns: Season | Winners[2] | Pts | Runners-up[6][7] | ...
    """
    log.info("Scraping La Liga title winners...")
    url = WIKI_URLS["la_liga_titles"]
    records = []

    try:
        soup = _fetch_page(url)
        tables = soup.find_all("table", {"class": "wikitable"})

        for table in tables:
            header_cells = table.find_all("th")
            header_texts = [th.get_text(strip=True).lower() for th in header_cells[:6]]
            if "season" not in header_texts:
                continue
            # Check this is the main results table (has "winner" in headers)
            has_winner = any("winner" in h for h in header_texts)
            if not has_winner:
                continue

            rows = table.find_all("tr")[1:]
            for row in rows:
                cells = row.find_all(["td", "th"])
                if len(cells) < 2:
                    continue

                cell_texts = [_clean_text(c.get_text()) for c in cells]
                season = cell_texts[0]
                winner = cell_texts[1]

                # Clean parenthetical counts like "(1)" from team name
                winner = re.sub(r"\s*\(\d+\)\s*", "", winner).strip()
                # Remove dagger/special chars
                winner = re.sub(r"[†‡§]", "", winner).strip()

                if season and winner:
                    records.append({
                        "season": season,
                        "champion": winner,
                    })

            log.info(f"  Parsed {len(records)} rows from champions table")
            break

    except Exception as e:
        log.warning(f"  Error scraping La Liga titles: {e}")

    log.info(f"  Found {len(records)} La Liga title records")
    return records


# ──────────────────────── Champions League Winners ────────────────────────

def scrape_champions_league() -> list[dict]:
    """Scrape UEFA Champions League winners by season."""
    log.info("Scraping Champions League winners...")
    url = WIKI_URLS["champions_league"]
    records = []

    try:
        soup = _fetch_page(url)
        html_str = str(soup)
        dfs = pd.read_html(html_str, match="Season|Final")
        for df in dfs:
            cols_lower = [str(c).lower() for c in df.columns]
            has_season = any("season" in c for c in cols_lower)
            has_winner = any("winner" in c or "champion" in c for c in cols_lower)

            if has_season and has_winner:
                for _, row in df.iterrows():
                    season_val = ""
                    winner_val = ""
                    for col in df.columns:
                        cl = str(col).lower()
                        val = _clean_text(str(row[col]))
                        if "season" in cl:
                            season_val = val
                        elif "winner" in cl or "champion" in cl:
                            winner_val = val

                    if winner_val and winner_val != "nan" and season_val:
                        records.append({
                            "season": season_val,
                            "winner": winner_val,
                        })
                break
    except Exception as e:
        log.warning(f"  Error scraping Champions League: {e}")

    log.info(f"  Found {len(records)} Champions League records")
    return records


# ──────────────────────── Main ────────────────────────

SCRAPERS = {
    "pichichi": scrape_pichichi,
    "ballon_dor": scrape_ballon_dor,
    "la_liga_best_player": scrape_la_liga_best_player,
    "la_liga_titles": scrape_la_liga_titles,
    "champions_league": scrape_champions_league,
}


def main():
    parser = argparse.ArgumentParser(description="Scrape La Liga awards data from Wikipedia")
    parser.add_argument(
        "--only", nargs="+", choices=list(SCRAPERS.keys()),
        help="Only scrape specific categories"
    )
    parser.add_argument("--force", action="store_true", help="Re-scrape even if cached")
    args = parser.parse_args()

    categories = args.only or list(SCRAPERS.keys())
    all_data: dict[str, Any] = {}

    for category in categories:
        out_path = RAW_WIKI_DIR / f"{category}.json"

        if out_path.exists() and not args.force:
            log.info(f"{category} — cached, loading from {out_path}")
            with open(out_path) as f:
                all_data[category] = json.load(f)
            continue

        scraper_fn = SCRAPERS[category]
        try:
            data = scraper_fn()
            all_data[category] = data

            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            log.info(f"Saved {len(data)} records to {out_path}")

        except Exception as e:
            log.error(f"Failed to scrape {category}: {e}")
            all_data[category] = []

        time.sleep(1)  # Be polite to Wikipedia

    # Summary
    total = sum(len(v) for v in all_data.values())
    log.info(f"Done — {total} total award records across {len(categories)} categories")
    for cat, records in all_data.items():
        log.info(f"  {cat}: {len(records)} records")


if __name__ == "__main__":
    main()
