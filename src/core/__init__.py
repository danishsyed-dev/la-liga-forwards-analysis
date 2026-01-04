"""
Core analysis modules for La Liga Forwards Analysis.
"""

from .analysis import calculate_player_score
from .players_data import players, points_system

__all__ = ["calculate_player_score", "players", "points_system"]
