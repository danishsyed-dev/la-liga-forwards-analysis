"""
Tests for the core analysis module.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from core.analysis import calculate_player_score
from core.players_data import players, points_system


class TestScoreCalculation:
    """Test player score calculation functions."""
    
    def test_calculate_player_score_messi(self):
        """Test score calculation for Messi."""
        messi_data = players.get('Lionel Messi')
        assert messi_data is not None
        
        score = calculate_player_score(messi_data, points_system)
        assert isinstance(score, int)
        assert score > 0
    
    def test_calculate_player_score_empty_player(self):
        """Test score calculation for player with minimal data."""
        empty_player = {
            'career_goals': 0,
            'seasons': [],
            'career_awards': [],
            'total_la_liga_titles': 0,
            'total_champions_league_titles': 0
        }
        
        score = calculate_player_score(empty_player, points_system)
        assert score == 0
    
    def test_career_goals_bonus_200_plus(self):
        """Test that 200+ goals bonus is applied."""
        player = {
            'career_goals': 250,
            'seasons': [],
            'career_awards': [],
            'total_la_liga_titles': 0,
            'total_champions_league_titles': 0
        }
        
        score = calculate_player_score(player, points_system)
        assert score >= points_system.get('200+ La Liga Goals', 0)
    
    def test_career_goals_bonus_100_plus(self):
        """Test that 100+ goals bonus is applied (but not 200+)."""
        player = {
            'career_goals': 150,  # Between 100 and 200
            'seasons': [],
            'career_awards': [],
            'total_la_liga_titles': 0,
            'total_champions_league_titles': 0
        }
        
        score = calculate_player_score(player, points_system)
        expected_bonus = points_system.get('100+ La Liga Goals', 0)
        assert score >= expected_bonus
        # Should NOT get 200+ bonus
        assert score < points_system.get('200+ La Liga Goals', 0) + expected_bonus
    
    def test_la_liga_titles_scoring(self):
        """Test La Liga titles add to score."""
        player = {
            'career_goals': 0,
            'seasons': [],
            'career_awards': [],
            'total_la_liga_titles': 5,
            'total_champions_league_titles': 0
        }
        
        score = calculate_player_score(player, points_system)
        expected = 5 * points_system.get('La Liga Title', 0)
        assert score == expected
    
    def test_all_players_have_positive_scores(self):
        """Test that all predefined players have positive scores."""
        for player_name, player_data in players.items():
            score = calculate_player_score(player_data, points_system)
            assert score > 0, f"{player_name} should have a positive score"


class TestPlayersData:
    """Test player data structure."""
    
    def test_players_not_empty(self):
        """Test that players dictionary is not empty."""
        assert len(players) > 0
    
    def test_all_players_have_required_fields(self):
        """Test all players have required data fields."""
        required_fields = [
            'career_goals',
            'seasons',
            'career_awards',
            'total_la_liga_titles',
            'total_champions_league_titles'
        ]
        
        for player_name, player_data in players.items():
            for field in required_fields:
                assert field in player_data, f"{player_name} missing field: {field}"
    
    def test_points_system_not_empty(self):
        """Test that points system is defined."""
        assert len(points_system) > 0
    
    def test_points_system_values_positive(self):
        """Test all point values are positive."""
        for award, points in points_system.items():
            assert points > 0, f"Award '{award}' should have positive points"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
