"""
Analysis functions for calculating player scores.
"""

from typing import Dict, Any


def calculate_player_score(player_data: Dict[str, Any], points_system: Dict[str, int]) -> int:
    """
    Calculate the total score for a player based on their achievements.
    
    Args:
        player_data: Dictionary containing player statistics and achievements
        points_system: Dictionary mapping achievements to point values
    
    Returns:
        Total score as an integer
    """
    total_score = 0
    
    # Bonus Points for Career Goals
    career_goals = player_data.get('career_goals', 0)
    if career_goals >= 200:
        total_score += points_system.get('200+ La Liga Goals', 0)
    elif career_goals >= 100:
        total_score += points_system.get('100+ La Liga Goals', 0)
    
    # Points for Career Awards (avoid double counting with season awards)
    career_ballons = player_data.get('career_awards', []).count("Ballon d'Or Win")
    total_score += career_ballons * points_system.get("Ballon d'Or Win", 0)
    
    # Points for Total La Liga Titles
    total_la_liga_titles = player_data.get('total_la_liga_titles', 0)
    total_score += total_la_liga_titles * points_system.get('La Liga Title', 0)
    
    # Points for Total Champions League Wins  
    total_ucl_titles = player_data.get('total_champions_league_titles', 0)
    total_score += total_ucl_titles * points_system.get('Champions League Win', 0)
    
    # Calculate points from seasons (avoid double counting titles)
    for season in player_data.get('seasons', []):
        season_score = 0
        
        # Points for 20+ Goals
        if season.get('goals', 0) >= 20:
            season_score += points_system.get('20+ Goal La Liga Season', 0)
        
        # Points for 10+ Assists
        if season.get('assists', 0) >= 10:
            season_score += points_system.get('10+ Assist La Liga Season', 0)
        
        # Points for Individual Awards (excluding Ballon d'Or which is counted above)
        for award in season.get('awards', []):
            if award != "Ballon d'Or Win":  # Prevent double counting
                season_score += points_system.get(award, 0)
        
        # Points for Cup Achievements (avoid double counting major titles)
        for achievement in season.get('team_achievements', []):
            if achievement in ['Copa del Rey', 'Supercopa de España', 'UEFA Super Cup', 'FIFA Club World Cup']:
                season_score += points_system.get('Other Trophies', 0)
        
        # Cup Final Winner
        if season.get('cup_final_winner', False):
            season_score += points_system.get('Cup Final Winner', 0)
        
        # Points for CL Individual Achievements
        for cl_award in season.get('cl_achievements', []):
            season_score += points_system.get(cl_award, 0)
        
        total_score += season_score
    
    return total_score
