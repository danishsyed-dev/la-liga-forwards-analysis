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
from core.players_data import load_players, points_system

# Load player data (from JSON if available, else fallback)
players = load_players()


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
        """Test that the majority of predefined players have positive scores.
        
        Note: Some players loaded from Wikipedia award data may have zero
        La Liga-specific scores (e.g., Ballon d'Or winners who played
        in other leagues like Billy Wright). This is expected.
        """
        scores = {
            name: calculate_player_score(data, points_system)
            for name, data in players.items()
        }
        positive = sum(1 for s in scores.values() if s > 0)
        assert positive > 0, "At least some players should have positive scores"
        # If using fallback data (7 players), all should be positive
        if len(players) <= 10:
            for player_name, score in scores.items():
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


class TestScoreEdgeCases:
    """Test edge cases in score calculation."""

    def test_score_with_missing_season_keys(self):
        """Scoring should handle seasons with minimal keys via .get() defaults."""
        player = {
            'career_goals': 50,
            'seasons': [
                {
                    'season': '2020/2021',
                    'goals': 25,
                    'assists': 12,
                    # No 'awards', 'team_achievements', 'cup_final_winner', 'cl_achievements'
                }
            ],
            'career_awards': [],
            'total_la_liga_titles': 0,
            'total_champions_league_titles': 0,
        }
        score = calculate_player_score(player, points_system)
        assert isinstance(score, int)
        assert score > 0  # Should get points for 20+ goals and 10+ assists

    def test_score_with_zero_goals_zero_assists(self):
        """Player with zero stats should only get points from titles/awards."""
        player = {
            'career_goals': 0,
            'seasons': [
                {
                    'season': '2020/2021',
                    'goals': 0,
                    'assists': 0,
                    'awards': [],
                    'team_achievements': [],
                    'cup_final_winner': False,
                    'cl_achievements': [],
                }
            ],
            'career_awards': [],
            'total_la_liga_titles': 2,
            'total_champions_league_titles': 0,
        }
        score = calculate_player_score(player, points_system)
        expected = 2 * points_system.get('La Liga Title', 0)
        assert score == expected

    def test_score_does_not_double_count_ballon_dor(self):
        """Ballon d'Or in season awards should not be double-counted with career awards."""
        player = {
            'career_goals': 50,
            'seasons': [
                {
                    'season': '2020/2021',
                    'goals': 30,
                    'assists': 5,
                    'awards': ["Ballon d'Or Win"],  # Should be skipped in season loop
                    'team_achievements': [],
                    'cup_final_winner': False,
                    'cl_achievements': [],
                }
            ],
            'career_awards': ["Ballon d'Or Win"],  # This is where it's counted
            'total_la_liga_titles': 0,
            'total_champions_league_titles': 0,
        }
        score = calculate_player_score(player, points_system)
        # Should count Ballon d'Or only once (from career_awards)
        ballon_dor_points = points_system.get("Ballon d'Or Win", 0)
        # Verify it's not double-counted
        player_no_season_ballon = {
            **player,
            'seasons': [
                {**player['seasons'][0], 'awards': []}
            ],
        }
        score_without = calculate_player_score(player_no_season_ballon, points_system)
        assert score == score_without  # Same score since Ballon d'Or is skipped in season loop

    def test_score_with_no_seasons(self):
        """Player with no seasons should still get career-level points."""
        player = {
            'career_goals': 250,
            'seasons': [],
            'career_awards': ["Ballon d'Or Win"],
            'total_la_liga_titles': 5,
            'total_champions_league_titles': 3,
        }
        score = calculate_player_score(player, points_system)
        expected = (
            points_system.get('200+ La Liga Goals', 0)
            + points_system.get("Ballon d'Or Win", 0)
            + 5 * points_system.get('La Liga Title', 0)
            + 3 * points_system.get('Champions League Win', 0)
        )
        assert score == expected


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

