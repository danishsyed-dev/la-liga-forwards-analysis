"""
Tests for built-in verified data source handler.
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from handlers.builtin_data_handler import load_verified_builtin_players


class TestBuiltInDataSource:
    """Test verified built-in data source loading."""

    def test_load_verified_builtin_players_returns_non_empty_dict(self):
        """Built-in verified data should load into player dictionary."""
        players = load_verified_builtin_players()
        assert isinstance(players, dict)
        assert len(players) > 0

    def test_load_verified_builtin_players_includes_core_players(self):
        """Built-in verified data should include known legends."""
        players = load_verified_builtin_players()
        assert "Lionel Messi" in players
        assert "Cristiano Ronaldo" in players

    def test_loaded_player_shape_matches_expected_internal_format(self):
        """Loaded players should match the app's internal player structure."""
        players = load_verified_builtin_players()
        messi = players["Lionel Messi"]
        assert "career_goals" in messi
        assert "seasons" in messi
        assert "career_awards" in messi
        assert isinstance(messi["seasons"], list)
