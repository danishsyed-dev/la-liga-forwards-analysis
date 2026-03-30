#!/usr/bin/env python3
"""
Manual FBref Data Importer — Processes FBref "Get table as CSV" exports.

Since FBref uses Cloudflare protection that blocks automated scraping,
this script processes manually downloaded data instead.

HOW TO USE:
    1. Open your browser and navigate to the FBref La Liga stats page:
       https://fbref.com/en/comps/12/stats/La-Liga-Stats
       (or a specific season like /2023-2024/stats/2023-2024-La-Liga-Stats)

    2. Find the "Standard Stats" table on the page.

    3. Click "Share & Export" → "Get table as CSV (for Excel)"

    4. Copy the CSV text and save it as a .csv file in data/raw/fbref/
       Name it by season: e.g., 2023-2024.csv

    5. Run this script to process all CSVs:
       python scripts/import_fbref_csv.py

    Alternatively, you can simply select all the data in the table,
    copy it, paste it into a spreadsheet, and export as CSV.

Output:
    data/raw/fbref/<season>.csv — cleaned and standardised CSVs
"""

import argparse
import logging
import sys
from io import StringIO
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import RAW_FBREF_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def process_fbref_csv(filepath: Path) -> pd.DataFrame:
    """
    Process a raw FBref "Get table as CSV" export.

    FBref CSV exports have:
      - A header comment line starting with "Player Standard Stats"
      - Multi-level column headers (two header rows)
      - Rows that repeat the header mid-table (for section breaks)
    """
    # Read the file
    with open(filepath, encoding="utf-8") as f:
        raw = f.read()

    # Remove the first line if it's a comment
    lines = raw.strip().split("\n")
    if lines and not lines[0].startswith("Rk") and not lines[0].startswith("Player"):
        lines = lines[1:]  # Skip the comment line

    # Parse CSV
    try:
        df = pd.read_csv(StringIO("\n".join(lines)))
    except Exception:
        # Try with multi-level header
        try:
            df = pd.read_csv(StringIO("\n".join(lines)), header=[0, 1])
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [
                    col[-1] if "Unnamed" in str(col[0]) else f"{col[0]}_{col[-1]}"
                    for col in df.columns
                ]
        except Exception as e:
            log.error(f"Could not parse {filepath.name}: {e}")
            return pd.DataFrame()

    # Remove repeated header rows and blank rows
    if "Player" in df.columns:
        df = df[df["Player"].notna() & (df["Player"] != "Player")]
    elif "player" in df.columns:
        df = df[df["player"].notna() & (df["player"] != "player")]

    # Standardise column names
    rename_map = {}
    for col in df.columns:
        cl = str(col).lower().strip()
        if cl == "player":
            rename_map[col] = "player"
        elif cl in ("squad", "team"):
            rename_map[col] = "team"
        elif cl in ("pos", "position"):
            rename_map[col] = "position"
        elif cl in ("nation", "nationality"):
            rename_map[col] = "nationality"
        elif cl in ("age",):
            rename_map[col] = "age"
        elif cl in ("mp",):
            rename_map[col] = "matches_played"
        elif cl in ("starts",):
            rename_map[col] = "starts"
        elif cl in ("min",):
            rename_map[col] = "minutes"
        elif cl in ("gls",) or cl == "performance_gls":
            rename_map[col] = "goals"
        elif cl in ("ast",) or cl == "performance_ast":
            rename_map[col] = "assists"

    df = df.rename(columns=rename_map)

    # Make sure we have goals and assists
    if "goals" not in df.columns:
        for c in df.columns:
            if "gls" in c.lower():
                df = df.rename(columns={c: "goals"})
                break
    if "assists" not in df.columns:
        for c in df.columns:
            if "ast" in c.lower():
                df = df.rename(columns={c: "assists"})
                break

    # Convert numeric columns
    for col in ["goals", "assists", "matches_played", "starts", "minutes", "age"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    # Extract season from filename (e.g., 2023-2024.csv → 2023-2024)
    season = filepath.stem
    df["season"] = season

    # Drop rows without player name
    if "player" in df.columns:
        df = df[df["player"].notna() & (df["player"].str.strip() != "")]

    return df.reset_index(drop=True)


def main():
    parser = argparse.ArgumentParser(
        description="Process manually downloaded FBref CSV exports"
    )
    parser.add_argument(
        "--dir", type=str, default=str(RAW_FBREF_DIR),
        help=f"Directory containing FBref CSV files (default: {RAW_FBREF_DIR})"
    )
    args = parser.parse_args()

    csv_dir = Path(args.dir)
    csv_files = sorted(csv_dir.glob("*.csv"))
    csv_files = [f for f in csv_files if not f.name.startswith("_")]

    if not csv_files:
        log.error(f"No CSV files found in {csv_dir}/")
        log.info("")
        log.info("=== HOW TO GET DATA FROM FBREF ===")
        log.info("1. Open: https://fbref.com/en/comps/12/stats/La-Liga-Stats")
        log.info("2. Find 'Standard Stats' table")
        log.info("3. Click 'Share & Export' → 'Get table as CSV'")
        log.info("4. Save the CSV as data/raw/fbref/<season>.csv")
        log.info("   e.g., data/raw/fbref/2023-2024.csv")
        log.info("5. Re-run this script")
        sys.exit(1)

    total_players = 0
    for f in csv_files:
        df = process_fbref_csv(f)
        if df.empty:
            log.warning(f"  {f.name}: no valid data")
            continue

        # Overwrite the file with the cleaned version
        df.to_csv(f, index=False)
        total_players += len(df)
        log.info(f"  {f.name}: {len(df)} players processed")

    log.info(f"Done — {total_players} total player records across {len(csv_files)} seasons")


if __name__ == "__main__":
    main()
