"""
Configuration for La Liga data scraping pipeline.

Defines seasons, URLs, directories, and award mappings used by scrapers.
"""

from pathlib import Path

# ──────────────────────── Paths ────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_FBREF_DIR = DATA_DIR / "raw" / "fbref"
RAW_WIKI_DIR = DATA_DIR / "raw" / "wikipedia"
PROCESSED_DIR = DATA_DIR / "processed"
FINAL_JSON = PROCESSED_DIR / "la_liga_all_players.json"

# Ensure dirs exist
for d in [RAW_FBREF_DIR, RAW_WIKI_DIR, PROCESSED_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ──────────────────────── Season range ────────────────────────
# FBref has detailed La Liga stats from ~1988-89 onwards.
# Earlier seasons have limited player-level data.
FBREF_START_SEASON = 1988  # Represents the 1988-1989 season
FBREF_END_SEASON = 2024    # Represents the 2024-2025 season

def season_str(year: int) -> str:
    """Convert start year to season string like '2023-2024'."""
    return f"{year}-{year + 1}"

def season_display(year: int) -> str:
    """Convert start year to display string like '2023/2024'."""
    return f"{year}/{year + 1}"

ALL_SEASONS = [season_str(y) for y in range(FBREF_START_SEASON, FBREF_END_SEASON + 1)]

# ──────────────────────── FBref URLs ────────────────────────
# La Liga competition ID on FBref is 12
FBREF_COMP_ID = 12
FBREF_BASE = "https://fbref.com/en/comps"

def fbref_season_stats_url(season: str) -> str:
    """
    Get the URL for a specific La Liga season's player standard stats.
    Example: https://fbref.com/en/comps/12/2023-2024/stats/2023-2024-La-Liga-Stats
    """
    return f"{FBREF_BASE}/{FBREF_COMP_ID}/{season}/stats/{season}-La-Liga-Stats"

def fbref_current_season_url() -> str:
    """URL for the current season stats (no season prefix in URL)."""
    return f"{FBREF_BASE}/{FBREF_COMP_ID}/stats/La-Liga-Stats"

# ──────────────────────── Wikipedia URLs ────────────────────────
WIKI_URLS = {
    "pichichi": "https://en.wikipedia.org/wiki/Pichichi_Trophy",
    "ballon_dor": "https://en.wikipedia.org/wiki/Ballon_d%27Or",
    "la_liga_best_player": "https://en.wikipedia.org/wiki/La_Liga_Awards",
    "la_liga_titles": "https://en.wikipedia.org/wiki/List_of_Spanish_football_champions",
    "champions_league": "https://en.wikipedia.org/wiki/UEFA_Champions_League",
    "copa_del_rey": "https://en.wikipedia.org/wiki/Copa_del_Rey",
}

# ──────────────────────── Scraper settings ────────────────────────
REQUEST_DELAY_SECONDS = 4        # Delay between FBref page loads
SELENIUM_PAGE_TIMEOUT = 30       # Max seconds to wait for page load
MAX_RETRIES = 3
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)

# ──────────────────────── Position filter ────────────────────────
# FBref position codes for forwards / attacking players
FORWARD_POSITIONS = {"FW", "FW,MF", "MF,FW"}

# ──────────────────────── Award name mapping ────────────────────────
# Maps scraped award names to the internal names used by the scoring engine
AWARD_MAP = {
    # Individual
    "Pichichi Trophy": "La Liga Golden Boot",
    "La Liga Golden Boot": "La Liga Golden Boot",
    "Ballon d'Or": "Ballon d'Or Win",
    "Ballon d'Or Win": "Ballon d'Or Win",
    "FIFA Best Player": "Ballon d'Or Win",  # Treated equivalently
    "La Liga Best Player": "La Liga Best Player Award",
    "La Liga Best Player Award": "La Liga Best Player Award",
    "Alfredo Di Stéfano Trophy": "La Liga Best Player Award",
    # Team
    "La Liga": "La Liga Title",
    "La Liga Title": "La Liga Title",
    "Champions League": "Champions League Win",
    "Champions League Win": "Champions League Win",
    "UEFA Champions League": "Champions League Win",
    "Copa del Rey": "Copa del Rey",
    "Supercopa de España": "Supercopa de España",
    "UEFA Super Cup": "UEFA Super Cup",
    "FIFA Club World Cup": "FIFA Club World Cup",
}

# ──────────────────────── Points system ────────────────────────
# This is the canonical scoring definition, shared with src/core/
POINTS_SYSTEM = {
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
