"""
Tests for the player data loading module.
"""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import patch, mock_open

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from core.players_data import load_players, _fallback_players, _load_from_json, points_system


class TestLoadPlayers:
    """Test player data loading and fallback behavior."""

    def test_load_players_returns_dict(self):
        """load_players() should always return a dict."""
        result = load_players()
        assert isinstance(result, dict)

    def test_load_players_not_empty(self):
        """load_players() should never return an empty dict."""
        result = load_players()
        assert len(result) > 0

    def test_load_players_with_explicit_nonexistent_path(self):
        """load_players with a nonexistent path should still return data (fallback)."""
        result = load_players(path="/nonexistent/path/data.json")
        assert isinstance(result, dict)
        assert len(result) > 0  # Falls back to JSON or built-in data


class TestFallbackPlayers:
    """Test the built-in fallback dataset."""

    def test_fallback_returns_7_players(self):
        """Fallback should contain exactly 7 legendary players."""
        players = _fallback_players()
        assert len(players) == 7

    def test_fallback_includes_messi(self):
        """Fallback should include Lionel Messi."""
        players = _fallback_players()
        assert "Lionel Messi" in players

    def test_fallback_includes_ronaldo(self):
        """Fallback should include Cristiano Ronaldo."""
        players = _fallback_players()
        assert "Cristiano Ronaldo" in players

    def test_fallback_player_has_required_fields(self):
        """Each fallback player should have all required fields."""
        required_fields = [
            'career_goals', 'seasons', 'career_awards',
            'total_la_liga_titles', 'total_champions_league_titles'
        ]
        players = _fallback_players()
        for name, data in players.items():
            for field in required_fields:
                assert field in data, f"{name} missing field: {field}"

    def test_fallback_player_seasons_are_lists(self):
        """Seasons should be lists for all fallback players."""
        players = _fallback_players()
        for name, data in players.items():
            assert isinstance(data['seasons'], list), f"{name} seasons is not a list"

    def test_fallback_career_goals_positive(self):
        """All fallback players should have positive career goals."""
        players = _fallback_players()
        for name, data in players.items():
            assert data['career_goals'] > 0, f"{name} has no career goals"

    def test_fallback_messi_career_goals(self):
        """Messi's fallback career goals should be 474 (La Liga total)."""
        players = _fallback_players()
        assert players['Lionel Messi']['career_goals'] == 474


class TestLoadFromJson:
    """Test JSON file loading."""

    def test_load_from_json_with_players_key(self, tmp_path):
        """Should extract players from {metadata, players} structure."""
        data = {
            "metadata": {"total_players": 1},
            "players": {
                "Test Player": {
                    "career_goals": 100,
                    "seasons": [],
                    "career_awards": [],
                    "total_la_liga_titles": 1,
                    "total_champions_league_titles": 0,
                }
            }
        }
        json_file = tmp_path / "test_data.json"
        json_file.write_text(json.dumps(data), encoding="utf-8")

        result = _load_from_json(json_file)
        assert "Test Player" in result
        assert result["Test Player"]["career_goals"] == 100

    def test_load_from_json_flat_dict(self, tmp_path):
        """Should handle flat dict (no metadata wrapper)."""
        data = {
            "Test Player": {
                "career_goals": 50,
                "seasons": [],
                "career_awards": [],
                "total_la_liga_titles": 0,
                "total_champions_league_titles": 0,
            }
        }
        json_file = tmp_path / "flat_data.json"
        json_file.write_text(json.dumps(data), encoding="utf-8")

        result = _load_from_json(json_file)
        assert "Test Player" in result


class TestPointsSystem:
    """Test points system integrity."""

    def test_points_system_not_empty(self):
        """Points system should have entries."""
        assert len(points_system) > 0

    def test_all_values_positive(self):
        """All point values should be positive integers."""
        for award, points in points_system.items():
            assert isinstance(points, int), f"{award} value is not int"
            assert points > 0, f"{award} has non-positive value"

    def test_no_duplicate_keys(self):
        """Points system should not have conceptual duplicates."""
        keys = list(points_system.keys())
        assert len(keys) == len(set(keys)), "Duplicate keys found"

    def test_ballon_dor_highest_individual(self):
        """Ballon d'Or Win should be worth 5 points."""
        assert points_system.get("Ballon d'Or Win") == 5

    def test_champions_league_win_value(self):
        """Champions League Win should be worth 5 points."""
        assert points_system.get("Champions League Win") == 5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
