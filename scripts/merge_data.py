#!/usr/bin/env python3
"""
Data Merger — Combines FBref stats + Wikipedia awards into a unified JSON dataset.

Reads:
  - data/raw/fbref/*.csv          (season-by-season player stats)
  - data/raw/wikipedia/*.json     (awards and honours data)

Produces:
  - data/processed/la_liga_all_players.json   (comprehensive merged dataset)

Usage:
    python scripts/merge_data.py
    python scripts/merge_data.py --forwards-only     # Filter to forward positions
"""

import argparse
import json
import logging
import re
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import (
    RAW_FBREF_DIR,
    RAW_WIKI_DIR,
    PROCESSED_DIR,
    FINAL_JSON,
    AWARD_MAP,
    FORWARD_POSITIONS,
    season_display,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


# ──────────────────────── Load raw data ────────────────────────

def load_fbref_data() -> pd.DataFrame:
    """Load and concatenate all FBref season CSVs."""
    csv_files = sorted(RAW_FBREF_DIR.glob("*.csv"))
    if not csv_files:
        log.warning("No FBref CSV files found in data/raw/fbref/")
        return pd.DataFrame()

    dfs = []
    for f in csv_files:
        if f.name.startswith("_"):
            continue
        try:
            df = pd.read_csv(f)
            dfs.append(df)
            log.info(f"  Loaded {len(df)} rows from {f.name}")
        except Exception as e:
            log.warning(f"  Failed to read {f.name}: {e}")

    if not dfs:
        return pd.DataFrame()

    combined = pd.concat(dfs, ignore_index=True)
    log.info(f"Total FBref records: {len(combined)} across {len(dfs)} seasons")
    return combined


def load_wikipedia_data() -> dict:
    """Load all Wikipedia award JSON files."""
    data = {}
    for f in RAW_WIKI_DIR.glob("*.json"):
        try:
            with open(f, encoding="utf-8") as fh:
                data[f.stem] = json.load(fh)
            log.info(f"  Loaded {len(data[f.stem])} records from {f.name}")
        except Exception as e:
            log.warning(f"  Failed to read {f.name}: {e}")
    return data


# ──────────────────────── Name normalisation ────────────────────────

def _normalize_name(name: str) -> str:
    """Normalise player name for fuzzy matching."""
    if not name or not isinstance(name, str):
        return ""
    # Remove accents roughly, lowercase, strip
    name = name.strip().lower()
    # Remove common suffixes like "(footballer)" 
    name = re.sub(r"\s*\(.*?\)\s*", "", name)
    return name


def _normalize_team(team: str) -> str:
    """Normalise team names for matching."""
    if not team or not isinstance(team, str):
        return ""
    team = team.strip()
    # Common normalisations
    replacements = {
        "FC Barcelona": "Barcelona",
        "Real Madrid CF": "Real Madrid",
        "Atlético Madrid": "Atlético Madrid",
        "Club Atlético de Madrid": "Atlético Madrid",
        "Athletic Bilbao": "Athletic Club",
        "Athletic Club de Bilbao": "Athletic Club",
        "Sevilla FC": "Sevilla",
        "Valencia CF": "Valencia",
        "Real Sociedad": "Real Sociedad",
        "Villarreal CF": "Villarreal",
        "Real Betis": "Real Betis",
        "RCD Espanyol": "Espanyol",
        "Deportivo de La Coruña": "Deportivo La Coruña",
    }
    return replacements.get(team, team)


def _season_to_year(season_str: str) -> int:
    """Extract start year from season string like '2023-2024' or '2023/2024'."""
    match = re.search(r"(\d{4})", season_str)
    return int(match.group(1)) if match else 0


# ──────────────────────── Build player profiles ────────────────────────

def build_player_profiles(
    fbref_df: pd.DataFrame,
    wiki_data: dict,
    forwards_only: bool = False,
) -> dict:
    """
    Build comprehensive player profiles combining FBref stats and Wikipedia awards.

    Returns dict of player_name -> profile dict compatible with analysis.py.
    """
    # ── Step 1: Build per-player season histories from FBref ──
    players = defaultdict(lambda: {
        "career_goals": 0,
        "team": "",
        "teams": [],
        "position": "",
        "nationality": "",
        "seasons": [],
        "career_awards": [],
        "total_la_liga_titles": 0,
        "total_champions_league_titles": 0,
    })

    if not fbref_df.empty:
        # Ensure required columns exist
        for col in ["player", "team", "season", "goals", "assists"]:
            if col not in fbref_df.columns:
                fbref_df[col] = "" if col in ["player", "team", "season"] else 0

        for _, row in fbref_df.iterrows():
            name = str(row.get("player", "")).strip()
            if not name or name == "nan":
                continue

            team = _normalize_team(str(row.get("team", "")))
            position = str(row.get("position", ""))
            season = str(row.get("season", ""))
            goals = int(row.get("goals", 0))
            assists = int(row.get("assists", 0))
            matches = int(row.get("matches_played", 0))
            minutes = int(row.get("minutes", 0))

            p = players[name]
            p["career_goals"] += goals

            if team and team not in p["teams"]:
                p["teams"].append(team)
            if not p["team"]:
                p["team"] = team

            if position and not p["position"]:
                p["position"] = position

            nationality = str(row.get("nationality", ""))
            if nationality and nationality != "nan" and not p["nationality"]:
                p["nationality"] = nationality

            p["seasons"].append({
                "season": season.replace("-", "/"),
                "team": team,
                "goals": goals,
                "assists": assists,
                "matches_played": matches,
                "minutes": minutes,
                "awards": [],
                "team_achievements": [],
                "cup_final_winner": False,
                "cl_achievements": [],
            })

        # Set primary team to the one with most seasons
        for name, p in players.items():
            if p["teams"]:
                from collections import Counter
                team_counts = Counter(s["team"] for s in p["seasons"] if s.get("team"))
                if team_counts:
                    p["team"] = team_counts.most_common(1)[0][0]

    # ── Step 2: Enrich with Wikipedia awards ──
    name_lookup = {_normalize_name(name): name for name in players}

    def _find_player(wiki_name: str) -> str | None:
        """Match a Wikipedia name to an existing player entry (exact normalized match only).
        
        We intentionally avoid fuzzy/partial matching to prevent incorrect merges
        (e.g., 'Ronaldo' != 'Cristiano Ronaldo').
        """
        norm = _normalize_name(wiki_name)
        if norm in name_lookup:
            return name_lookup[norm]
        return None

    # Pichichi Trophy (La Liga top scorer)
    for record in wiki_data.get("pichichi", []):
        player_name = record.get("player", "")
        if not player_name:
            continue
        matched = _find_player(player_name)
        if matched:
            season = record.get("season", "")
            for s in players[matched]["seasons"]:
                if season in s["season"] or s["season"] in season:
                    if "La Liga Golden Boot" not in s["awards"]:
                        s["awards"].append("La Liga Golden Boot")
                    break
        else:
            # Create a new player entry from award data
            team = _normalize_team(record.get("team", ""))
            season = record.get("season", "")
            goals = record.get("goals", 0)
            p = players[player_name]
            p["team"] = team
            if team and team not in p["teams"]:
                p["teams"].append(team)
            p["career_goals"] += goals
            p["seasons"].append({
                "season": season,
                "team": team,
                "goals": goals,
                "assists": 0,
                "matches_played": 0,
                "minutes": 0,
                "awards": ["La Liga Golden Boot"],
                "team_achievements": [],
                "cup_final_winner": False,
                "cl_achievements": [],
            })
            name_lookup[_normalize_name(player_name)] = player_name

    # Ballon d'Or
    for record in wiki_data.get("ballon_dor", []):
        player_name = record.get("player", "")
        if not player_name:
            continue
        award_name = record.get("award", "Ballon d'Or Win")
        matched = _find_player(player_name)
        target = matched or player_name
        if not matched:
            # Create a new minimal entry
            team = _normalize_team(record.get("team", ""))
            p = players[target]
            if team:
                p["team"] = team
                if team not in p["teams"]:
                    p["teams"].append(team)
            name_lookup[_normalize_name(player_name)] = target
        if award_name:
            players[target]["career_awards"].append(award_name)

    # La Liga Best Player
    for record in wiki_data.get("la_liga_best_player", []):
        player = _find_player(record.get("player", ""))
        if player:
            season = record.get("season", "")
            for s in players[player]["seasons"]:
                if season in s["season"] or s["season"] in season:
                    if "La Liga Best Player Award" not in s["awards"]:
                        s["awards"].append("La Liga Best Player Award")
                    break

    # La Liga titles — map champion team to all players of that team in that season
    la_liga_champions = {}
    for record in wiki_data.get("la_liga_titles", []):
        season = record.get("season", "")
        champion = _normalize_team(record.get("champion", ""))
        if season and champion:
            la_liga_champions[season] = champion

    for name, p in players.items():
        title_count = 0
        for s in p["seasons"]:
            season_str_val = s.get("season", "")
            team = _normalize_team(s.get("team", ""))
            for champ_season, champ_team in la_liga_champions.items():
                if (champ_season in season_str_val or season_str_val in champ_season) and team == champ_team:
                    if "La Liga Title" not in s["team_achievements"]:
                        s["team_achievements"].append("La Liga Title")
                    title_count += 1
                    break
        p["total_la_liga_titles"] = title_count

    # Champions League winners — map winner team to players
    cl_winners = {}
    for record in wiki_data.get("champions_league", []):
        season = record.get("season", "")
        winner = _normalize_team(record.get("winner", ""))
        if season and winner:
            cl_winners[season] = winner

    for name, p in players.items():
        cl_count = 0
        for s in p["seasons"]:
            season_str_val = s.get("season", "")
            team = _normalize_team(s.get("team", ""))
            for cl_season, cl_team in cl_winners.items():
                if (cl_season in season_str_val or season_str_val in cl_season) and team == cl_team:
                    if "Champions League Win" not in s["team_achievements"]:
                        s["team_achievements"].append("Champions League Win")
                    cl_count += 1
                    break
        p["total_champions_league_titles"] = cl_count

    # ── Step 3: Filter to forwards if requested ──
    if forwards_only:
        players = {
            name: p for name, p in players.items()
            if p.get("position", "") in FORWARD_POSITIONS or not p.get("position")
        }
        log.info(f"Filtered to {len(players)} forwards")

    # ── Step 4: Sort seasons chronologically ──
    for p in players.values():
        p["seasons"].sort(key=lambda s: s.get("season", ""))

    return dict(players)


# ──────────────────────── Output ────────────────────────

def save_dataset(players: dict, output_path: Path):
    """Save the merged dataset as JSON."""
    import time

    dataset = {
        "metadata": {
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_players": len(players),
            "sources": {
                "stats": "FBref.com (Sports Reference / StatsBomb)",
                "awards": "Wikipedia",
            },
            "description": (
                "Comprehensive La Liga player statistics combining season-by-season "
                "performance data from FBref with awards and honours from Wikipedia."
            ),
        },
        "players": players,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    log.info(f"Saved {len(players)} player profiles to {output_path}")

    # Also generate a summary CSV for quick inspection
    summary_rows = []
    for name, p in players.items():
        summary_rows.append({
            "player": name,
            "team": p.get("team", ""),
            "position": p.get("position", ""),
            "career_goals": p.get("career_goals", 0),
            "total_seasons": len(p.get("seasons", [])),
            "la_liga_titles": p.get("total_la_liga_titles", 0),
            "cl_titles": p.get("total_champions_league_titles", 0),
            "ballon_dor_wins": p.get("career_awards", []).count("Ballon d'Or Win"),
        })

    if summary_rows:
        summary_df = pd.DataFrame(summary_rows)
        summary_df = summary_df.sort_values("career_goals", ascending=False)
        summary_csv = output_path.parent / "players_summary.csv"
        summary_df.to_csv(summary_csv, index=False)
        log.info(f"Saved summary CSV to {summary_csv}")


# ──────────────────────── CLI ────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Merge FBref + Wikipedia data into unified dataset")
    parser.add_argument("--forwards-only", action="store_true", help="Only include forward positions")
    parser.add_argument("--output", type=str, default=str(FINAL_JSON), help="Output JSON path")
    args = parser.parse_args()

    log.info("Loading FBref data...")
    fbref_df = load_fbref_data()

    log.info("Loading Wikipedia data...")
    wiki_data = load_wikipedia_data()

    if fbref_df.empty and not wiki_data:
        log.error("No data found! Run scrape_fbref.py and scrape_wikipedia.py first.")
        sys.exit(1)

    log.info("Building player profiles...")
    players = build_player_profiles(
        fbref_df,
        wiki_data,
        forwards_only=args.forwards_only,
    )

    output_path = Path(args.output)
    save_dataset(players, output_path)

    # Print top 10 by career goals
    top = sorted(players.items(), key=lambda x: x[1]["career_goals"], reverse=True)[:10]
    log.info("Top 10 by career goals:")
    for i, (name, p) in enumerate(top, 1):
        log.info(f"  {i}. {name} ({p['team']}) — {p['career_goals']} goals, "
                 f"{p['total_la_liga_titles']} titles")


if __name__ == "__main__":
    main()
