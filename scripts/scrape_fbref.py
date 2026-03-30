#!/usr/bin/env python3
"""
FBref Scraper — Fetches season-by-season La Liga player stats.

Uses Selenium (real browser) to bypass FBref's aggressive bot blocking.
Falls back to direct HTTP requests with proper headers if Selenium is unavailable.

Usage:
    python scripts/scrape_fbref.py                   # Scrape all configured seasons
    python scripts/scrape_fbref.py --seasons 2023-2024 2022-2023
    python scripts/scrape_fbref.py --start 2015 --end 2024
    python scripts/scrape_fbref.py --current          # Current season only

Output:
    data/raw/fbref/<season>.csv   — one CSV per season with player stats
"""

import argparse
import json
import logging
import sys
import time
from pathlib import Path

import pandas as pd

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import (
    ALL_SEASONS,
    FBREF_START_SEASON,
    FBREF_END_SEASON,
    RAW_FBREF_DIR,
    REQUEST_DELAY_SECONDS,
    SELENIUM_PAGE_TIMEOUT,
    MAX_RETRIES,
    USER_AGENT,
    fbref_season_stats_url,
    fbref_current_season_url,
    season_str,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


# ──────────────────────── Selenium backend ────────────────────────

def _get_selenium_driver(visible: bool = False):
    """Create a Chrome driver via Selenium. Uses stealth settings to bypass FBref bot detection."""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        import random

        opts = Options()

        if not visible:
            opts.add_argument("--headless=new")

        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_argument(f"--user-agent={USER_AGENT}")
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--disable-extensions")
        opts.add_argument("--disable-popup-blocking")
        opts.add_argument("--lang=en-US,en")

        # remove "Enable automation" infobar
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.Chrome(options=opts)
        driver.set_page_load_timeout(SELENIUM_PAGE_TIMEOUT)

        # Remove webdriver flag via CDP
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                window.chrome = {runtime: {}};
            """
        })

        mode = "visible" if visible else "headless"
        log.info(f"Selenium Chrome driver initialized ({mode})")
        return driver
    except Exception as e:
        log.warning(f"Could not create Selenium driver: {e}")
        return None


def _scrape_with_selenium(driver, url: str) -> pd.DataFrame:
    """Load a FBref page in Selenium and extract the main stats table."""
    import random
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    driver.get(url)
    # Random delay to look more human
    time.sleep(random.uniform(3, 6))

    # Wait for the main stats table to appear
    try:
        WebDriverWait(driver, SELENIUM_PAGE_TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.stats_table"))
        )
    except Exception:
        # Try broader selectors
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
            )
        except Exception:
            log.warning(f"No tables found on {url}")
            # Save page source for debugging
            source = driver.page_source[:500]
            log.warning(f"  Page snippet: {source[:200]}...")
            return pd.DataFrame()

    # Get all stats tables
    tables = driver.find_elements(By.CSS_SELECTOR, "table.stats_table")
    if not tables:
        # Fallback: try any table with id containing "stats"
        tables = driver.find_elements(By.CSS_SELECTOR, "table[id*='stats']")
    if not tables:
        tables = driver.find_elements(By.CSS_SELECTOR, "table")

    if not tables:
        return pd.DataFrame()

    # Extract the first stats table's HTML
    table_html = tables[0].get_attribute("outerHTML")

    # Parse with pandas
    try:
        from io import StringIO
        dfs = pd.read_html(StringIO(table_html), header=[0, 1])
    except Exception:
        dfs = pd.read_html(StringIO(table_html))

    if not dfs:
        return pd.DataFrame()

    df = dfs[0]
    # Flatten multi-level column headers
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            col[-1] if col[0].startswith("Unnamed") else f"{col[0]}_{col[-1]}"
            for col in df.columns
        ]

    return df


# ──────────────────────── HTTP fallback ────────────────────────

def _scrape_with_requests(url: str) -> pd.DataFrame:
    """Attempt direct HTTP scrape (may get 403 from FBref)."""
    import requests
    from bs4 import BeautifulSoup

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/",
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    table = soup.find("table", {"class": "stats_table"})
    if table is None:
        return pd.DataFrame()

    dfs = pd.read_html(str(table), header=[0, 1])
    if not dfs:
        return pd.DataFrame()

    df = dfs[0]
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            col[-1] if col[0].startswith("Unnamed") else f"{col[0]}_{col[-1]}"
            for col in df.columns
        ]
    return df


# ──────────────────────── Post-processing ────────────────────────

def _clean_player_stats(df: pd.DataFrame, season: str) -> pd.DataFrame:
    """Clean and standardise a raw FBref stats DataFrame."""
    if df.empty:
        return df

    # Remove section header / totals rows
    df = df[df.iloc[:, 0] != df.columns[0]]  # header rows repeated
    if "Player" in df.columns:
        df = df[df["Player"].notna() & (df["Player"] != "Player")]

    # Standardise key column names
    rename_map = {}
    for col in df.columns:
        cl = col.lower()
        if cl == "player":
            rename_map[col] = "player"
        elif cl == "squad":
            rename_map[col] = "team"
        elif cl == "pos":
            rename_map[col] = "position"
        elif cl == "nation":
            rename_map[col] = "nationality"
        elif cl in ("age",):
            rename_map[col] = "age"
        elif "mp" in cl and "match" not in cl:
            rename_map[col] = "matches_played"
        elif cl in ("starts",):
            rename_map[col] = "starts"
        elif cl in ("min",):
            rename_map[col] = "minutes"
        elif cl.endswith("gls") or cl == "goals" or cl == "performance_gls":
            if "gls" in cl and "performance" in cl.lower():
                rename_map[col] = "goals"
            elif cl in ("gls", "goals"):
                rename_map[col] = "goals"
        elif cl.endswith("ast") or cl == "assists" or cl == "performance_ast":
            if "ast" in cl:
                rename_map[col] = "assists"

    df = df.rename(columns=rename_map)

    # Ensure we have key columns; if column exists with different name, try standard FBref names
    if "goals" not in df.columns:
        for c in df.columns:
            if "Gls" in c or "gls" in c:
                df = df.rename(columns={c: "goals"})
                break

    if "assists" not in df.columns:
        for c in df.columns:
            if "Ast" in c or "ast" in c:
                df = df.rename(columns={c: "assists"})
                break

    # Add season column
    df["season"] = season

    # Convert numeric columns
    for col in ["goals", "assists", "matches_played", "starts", "minutes", "age"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    # Drop rows without a valid player name
    if "player" in df.columns:
        df = df[df["player"].notna() & (df["player"].str.strip() != "")]

    return df.reset_index(drop=True)


# ──────────────────────── Main scraping loop ────────────────────────

def scrape_seasons(seasons: list[str], force: bool = False, visible: bool = False) -> dict:
    """
    Scrape player stats for the given seasons.

    Returns dict mapping season -> output CSV path.
    """
    results = {}

    # Try Selenium first
    driver = _get_selenium_driver(visible=visible)
    use_selenium = driver is not None

    try:
        for i, season in enumerate(seasons):
            out_path = RAW_FBREF_DIR / f"{season}.csv"

            # Skip if already scraped (unless --force)
            if out_path.exists() and not force:
                log.info(f"[{i+1}/{len(seasons)}] {season} — cached, skipping")
                results[season] = str(out_path)
                continue

            url = fbref_season_stats_url(season)
            log.info(f"[{i+1}/{len(seasons)}] Scraping {season} from {url}")

            df = pd.DataFrame()
            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    if use_selenium:
                        df = _scrape_with_selenium(driver, url)
                    else:
                        df = _scrape_with_requests(url)

                    if not df.empty:
                        break
                except Exception as e:
                    log.warning(f"  Attempt {attempt}/{MAX_RETRIES} failed: {e}")
                    time.sleep(REQUEST_DELAY_SECONDS * attempt)

            if df.empty:
                log.error(f"  FAILED to scrape {season} after {MAX_RETRIES} attempts")
                continue

            # Clean and save
            df = _clean_player_stats(df, season)
            df.to_csv(out_path, index=False)
            log.info(f"  Saved {len(df)} players to {out_path}")
            results[season] = str(out_path)

            # Rate limiting
            if i < len(seasons) - 1:
                log.info(f"  Waiting {REQUEST_DELAY_SECONDS}s (rate limit)...")
                time.sleep(REQUEST_DELAY_SECONDS)

    finally:
        if driver:
            driver.quit()
            log.info("Selenium driver closed")

    return results


# ──────────────────────── CLI ────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Scrape La Liga player stats from FBref")
    parser.add_argument(
        "--seasons", nargs="+",
        help="Specific seasons to scrape, e.g. 2023-2024 2022-2023"
    )
    parser.add_argument("--start", type=int, help="Start year (e.g. 2015)")
    parser.add_argument("--end", type=int, help="End year (e.g. 2024)")
    parser.add_argument("--current", action="store_true", help="Scrape current season only")
    parser.add_argument("--force", action="store_true", help="Re-scrape even if cached")
    parser.add_argument("--visible", action="store_true",
                        help="Run browser in visible mode (use when headless is blocked by FBref)")
    args = parser.parse_args()

    if args.current:
        seasons = [season_str(FBREF_END_SEASON)]
    elif args.seasons:
        seasons = args.seasons
    elif args.start or args.end:
        start = args.start or FBREF_START_SEASON
        end = args.end or FBREF_END_SEASON
        seasons = [season_str(y) for y in range(start, end + 1)]
    else:
        seasons = ALL_SEASONS

    log.info(f"Will scrape {len(seasons)} season(s): {seasons[0]} → {seasons[-1]}")
    results = scrape_seasons(seasons, force=args.force, visible=args.visible)
    log.info(f"Done — scraped {len(results)}/{len(seasons)} seasons successfully")

    # Summary
    summary_path = RAW_FBREF_DIR / "_scrape_summary.json"
    with open(summary_path, "w") as f:
        json.dump({"seasons_scraped": results, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}, f, indent=2)
    log.info(f"Summary saved to {summary_path}")


if __name__ == "__main__":
    main()
