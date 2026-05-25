#!/usr/bin/env python3
"""
Data Pipeline Orchestrator — Runs the full data collection and merge pipeline.

Usage:
    python scripts/main.py              # Run full pipeline
    python scripts/main.py --skip-fbref  # Skip FBref (requires manual CSV export)
"""

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent


def run_script(name: str, args: list = None) -> None:
    """Run a pipeline script and raise on failure."""
    cmd = [sys.executable, str(SCRIPTS_DIR / name)] + (args or [])
    print(f"\n{'='*60}")
    print(f"Running: {' '.join(cmd)}")
    print(f"{'='*60}")
    subprocess.run(cmd, check=True)
    print(f"✅ {name} completed successfully")


def main():
    parser = argparse.ArgumentParser(description="Run the full La Liga data pipeline")
    parser.add_argument(
        "--skip-fbref", action="store_true",
        help="Skip FBref scraping (use if you've manually exported CSVs)",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Force re-scrape even if cached data exists",
    )
    args = parser.parse_args()

    print("⚽ La Liga Forwards Analysis — Data Pipeline")
    print("=" * 60)

    # Step 1: Scrape Wikipedia awards
    wiki_args = ["--force"] if args.force else []
    run_script("scrape_wikipedia.py", wiki_args)

    # Step 2: Process FBref data
    if args.skip_fbref:
        print("\n⏭️  Skipping FBref scraping (--skip-fbref)")
        print("   Make sure CSVs exist in data/raw/fbref/")
    else:
        run_script("import_fbref_csv.py")

    # Step 3: Merge all data sources
    run_script("merge_data.py")

    print("\n" + "=" * 60)
    print("🏆 Pipeline complete!")
    print("   Dataset: data/processed/la_liga_all_players.json")
    print("   Summary: data/processed/players_summary.csv")
    print("\n   Next: Run 'streamlit run app.py' to explore the data.")


if __name__ == "__main__":
    main()
