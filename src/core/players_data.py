"""
Player data and scoring system definitions.

Loads player data from the verified JSON dataset (data/processed/la_liga_all_players.json)
produced by the data pipeline (scripts/scrape_fbref.py + scrape_wikipedia.py + merge_data.py).

Falls back to a minimal built-in dataset if the JSON file is not found.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any

log = logging.getLogger(__name__)

# ──────────────────────── Points System ────────────────────────
# This is project logic (not data), so it stays here as the single source of truth.

points_system: Dict[str, int] = {
    "Ballon d'Or Win": 5,
    "Ballon d'Or 2nd Place": 3,
    "Ballon d'Or 3rd Place": 1,
    "La Liga Title": 1,
    "Champions League Win": 5,
    "La Liga Best Player Award": 4,
    "La Liga Breakthrough Player": 1,
    "La Liga Golden Boot": 3,
    "20+ Goal La Liga Season": 2,
    "Most Assists in La Liga Season": 2,
    "10+ Assist La Liga Season": 1,
    "Cup Final Winner": 1,
    "Other Trophies": 1,
    "200+ La Liga Goals": 5,
    "100+ La Liga Goals": 2,
    "CL Top Scorer": 5,
    "Most Assists in CL Season": 2,
}


# ──────────────────────── Data Loading ────────────────────────

# Path to the verified dataset produced by the scraping pipeline
_DATA_DIR = Path(__file__).resolve().parents[2] / "data"
_VERIFIED_JSON = _DATA_DIR / "processed" / "la_liga_all_players.json"


def load_players(path: Path | str | None = None) -> Dict[str, Dict[str, Any]]:
    """
    Load player data from the verified JSON dataset.

    Priority order:
        1. Explicit path argument
        2. data/processed/la_liga_all_players.json
        3. Minimal fallback dataset (7 legendary players)

    The returned dict is keyed by player name and compatible with
    calculate_player_score() in analysis.py.
    """
    # Try explicit path first
    if path:
        json_path = Path(path)
        if json_path.exists():
            return _load_from_json(json_path)

    # Try the verified dataset
    if _VERIFIED_JSON.exists():
        return _load_from_json(_VERIFIED_JSON)

    # Fallback to built-in minimal dataset
    log.warning(
        "Verified dataset not found at %s. "
        "Run 'python scripts/scrape_fbref.py && python scripts/scrape_wikipedia.py "
        "&& python scripts/merge_data.py' to generate it. "
        "Using minimal fallback data.",
        _VERIFIED_JSON,
    )
    return _fallback_players()


def _load_from_json(path: Path) -> Dict[str, Dict[str, Any]]:
    """Load player data from a JSON file."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    # The JSON has {"metadata": {...}, "players": {...}} structure
    if "players" in data:
        players = data["players"]
    else:
        players = data  # Assume flat dict

    log.info("Loaded %d players from %s", len(players), path)
    return players


def _fallback_players() -> Dict[str, Dict[str, Any]]:
    """
    Minimal fallback dataset with verified career stats for 7 legendary La Liga forwards.

    Sources:
        - Career goals: FBref.com La Liga career totals
        - Awards: Wikipedia (Ballon d'Or, Pichichi Trophy articles)
        - Titles: Wikipedia (club season articles)
    """
    return {
        "Lionel Messi": {
            "career_goals": 474,
            "team": "Barcelona",
            "position": "FW",
            "seasons": [
                {
                    "season": "2011/2012", "team": "Barcelona",
                    "goals": 50, "assists": 15,
                    "awards": ["Ballon d'Or Win", "La Liga Best Player Award", "La Liga Golden Boot"],
                    "team_achievements": ["La Liga Title", "Copa del Rey"],
                    "cup_final_winner": True,
                    "cl_achievements": ["CL Top Scorer"],
                },
                {
                    "season": "2014/2015", "team": "Barcelona",
                    "goals": 43, "assists": 18,
                    "awards": ["La Liga Best Player Award"],
                    "team_achievements": ["La Liga Title", "Champions League Win", "Copa del Rey"],
                    "cup_final_winner": True,
                    "cl_achievements": [],
                },
                {
                    "season": "2009/2010", "team": "Barcelona",
                    "goals": 34, "assists": 11,
                    "awards": ["Ballon d'Or Win", "La Liga Best Player Award", "La Liga Golden Boot"],
                    "team_achievements": ["La Liga Title"],
                    "cup_final_winner": False,
                    "cl_achievements": [],
                },
            ],
            "career_awards": ["Ballon d'Or Win"] * 4,
            "total_la_liga_titles": 10,
            "total_champions_league_titles": 4,
        },
        "Cristiano Ronaldo": {
            "career_goals": 311,
            "team": "Real Madrid",
            "position": "FW",
            "seasons": [
                {
                    "season": "2013/2014", "team": "Real Madrid",
                    "goals": 31, "assists": 11,
                    "awards": ["Ballon d'Or Win"],
                    "team_achievements": ["Champions League Win", "Copa del Rey"],
                    "cup_final_winner": True,
                    "cl_achievements": ["CL Top Scorer"],
                },
                {
                    "season": "2015/2016", "team": "Real Madrid",
                    "goals": 35, "assists": 11,
                    "awards": ["Ballon d'Or Win"],
                    "team_achievements": ["Champions League Win"],
                    "cup_final_winner": False,
                    "cl_achievements": ["CL Top Scorer"],
                },
                {
                    "season": "2011/2012", "team": "Real Madrid",
                    "goals": 46, "assists": 12,
                    "awards": ["La Liga Golden Boot"],
                    "team_achievements": ["La Liga Title"],
                    "cup_final_winner": False,
                    "cl_achievements": [],
                },
            ],
            "career_awards": ["Ballon d'Or Win"] * 4,
            "total_la_liga_titles": 2,
            "total_champions_league_titles": 4,
        },
        "Luis Suárez": {
            "career_goals": 147,
            "team": "Barcelona",
            "position": "FW",
            "seasons": [
                {
                    "season": "2015/2016", "team": "Barcelona",
                    "goals": 40, "assists": 16,
                    "awards": ["La Liga Golden Boot"],
                    "team_achievements": ["La Liga Title", "Copa del Rey"],
                    "cup_final_winner": True, "cl_achievements": [],
                },
                {
                    "season": "2016/2017", "team": "Barcelona",
                    "goals": 29, "assists": 13,
                    "awards": [],
                    "team_achievements": ["Copa del Rey"],
                    "cup_final_winner": True, "cl_achievements": [],
                },
                {
                    "season": "2017/2018", "team": "Barcelona",
                    "goals": 25, "assists": 12,
                    "awards": [],
                    "team_achievements": ["La Liga Title", "Copa del Rey"],
                    "cup_final_winner": True, "cl_achievements": [],
                },
            ],
            "career_awards": [],
            "total_la_liga_titles": 4,
            "total_champions_league_titles": 1,
        },
        "Karim Benzema": {
            "career_goals": 238,
            "team": "Real Madrid",
            "position": "FW",
            "seasons": [
                {
                    "season": "2021/2022", "team": "Real Madrid",
                    "goals": 27, "assists": 12,
                    "awards": ["Ballon d'Or Win", "La Liga Best Player Award"],
                    "team_achievements": ["La Liga Title", "Champions League Win", "Supercopa de España"],
                    "cup_final_winner": True,
                    "cl_achievements": ["CL Top Scorer"],
                },
                {
                    "season": "2015/2016", "team": "Real Madrid",
                    "goals": 24, "assists": 7,
                    "awards": [],
                    "team_achievements": ["Champions League Win"],
                    "cup_final_winner": False, "cl_achievements": [],
                },
                {
                    "season": "2019/2020", "team": "Real Madrid",
                    "goals": 21, "assists": 8,
                    "awards": [],
                    "team_achievements": ["La Liga Title"],
                    "cup_final_winner": False, "cl_achievements": [],
                },
            ],
            "career_awards": ["Ballon d'Or Win"],
            "total_la_liga_titles": 5,
            "total_champions_league_titles": 5,
        },
        "Neymar Jr.": {
            "career_goals": 68,
            "team": "Barcelona",
            "position": "FW",
            "seasons": [
                {
                    "season": "2015/2016", "team": "Barcelona",
                    "goals": 24, "assists": 12,
                    "awards": [],
                    "team_achievements": ["La Liga Title", "Copa del Rey"],
                    "cup_final_winner": True, "cl_achievements": [],
                },
                {
                    "season": "2014/2015", "team": "Barcelona",
                    "goals": 22, "assists": 7,
                    "awards": [],
                    "team_achievements": ["La Liga Title", "Champions League Win", "Copa del Rey"],
                    "cup_final_winner": True, "cl_achievements": [],
                },
                {
                    "season": "2016/2017", "team": "Barcelona",
                    "goals": 13, "assists": 11,
                    "awards": ["Most Assists in La Liga Season"],
                    "team_achievements": ["Copa del Rey"],
                    "cup_final_winner": True, "cl_achievements": [],
                },
            ],
            "career_awards": [],
            "total_la_liga_titles": 2,
            "total_champions_league_titles": 1,
        },
        "Gareth Bale": {
            "career_goals": 81,
            "team": "Real Madrid",
            "position": "FW",
            "seasons": [
                {
                    "season": "2013/2014", "team": "Real Madrid",
                    "goals": 15, "assists": 12,
                    "awards": ["La Liga Breakthrough Player"],
                    "team_achievements": ["Champions League Win", "Copa del Rey"],
                    "cup_final_winner": True, "cl_achievements": [],
                },
                {
                    "season": "2015/2016", "team": "Real Madrid",
                    "goals": 19, "assists": 10,
                    "awards": [],
                    "team_achievements": ["Champions League Win"],
                    "cup_final_winner": False, "cl_achievements": [],
                },
                {
                    "season": "2017/2018", "team": "Real Madrid",
                    "goals": 16, "assists": 2,
                    "awards": [],
                    "team_achievements": ["Champions League Win"],
                    "cup_final_winner": True, "cl_achievements": [],
                },
            ],
            "career_awards": [],
            "total_la_liga_titles": 3,
            "total_champions_league_titles": 5,
        },
        "Raúl González": {
            "career_goals": 228,
            "team": "Real Madrid",
            "position": "FW",
            "seasons": [
                {
                    "season": "1998/1999", "team": "Real Madrid",
                    "goals": 25, "assists": 5,
                    "awards": ["La Liga Golden Boot"],
                    "team_achievements": [],
                    "cup_final_winner": False,
                    "cl_achievements": [],
                },
                {
                    "season": "2000/2001", "team": "Real Madrid",
                    "goals": 24, "assists": 6,
                    "awards": ["Ballon d'Or 2nd Place"],
                    "team_achievements": ["La Liga Title"],
                    "cup_final_winner": False,
                    "cl_achievements": ["CL Top Scorer"],
                },
                {
                    "season": "1999/2000", "team": "Real Madrid",
                    "goals": 17, "assists": 9,
                    "awards": [],
                    "team_achievements": ["Champions League Win"],
                    "cup_final_winner": False,
                    "cl_achievements": ["CL Top Scorer"],
                },
            ],
            "career_awards": [],
            "total_la_liga_titles": 6,
            "total_champions_league_titles": 3,
        },
    }


# ──────────────────────── Legacy compatibility ────────────────────────
# The old code did `from core.players_data import players`
# Keep this as a module-level dict that loads on import.
players = load_players()
