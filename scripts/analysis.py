def calculate_player_score(player_data, points_system):
    total_score = 0
    
    # Bonus Points for Career Goals
    career_goals = player_data.get('career_goals', 0)
    if career_goals >= 200:
        total_score += points_system.get('200+ La Liga Goals', 0)
    elif career_goals >= 100:
        total_score += points_system.get('100+ La Liga Goals', 0)
    
    # Points for Career Awards
    for award in player_data.get('career_awards', []):
        total_score += points_system.get(award, 0)
    
    # Points for Total La Liga Titles
    total_la_liga_titles = player_data.get('total_la_liga_titles', 0)
    total_score += total_la_liga_titles * points_system.get('La Liga Title', 0)
    
    # Points for Total Champions League Wins
    total_ucl_titles = player_data.get('total_champions_league_titles', 0)
    total_score += total_ucl_titles * points_system.get('Champions League Win', 0)
    
    # Calculate points from the best 3 seasons
    for season in player_data['seasons']:
        season_score = 0
        
        # Points for 20+ Goals
        if season['goals'] >= 20:
            season_score += points_system.get('20+ Goal La Liga Season', 0)
        
        # Points for 10+ Assists
        if season['assists'] >= 10:
            season_score += points_system.get('10+ Assist La Liga Season', 0)
        
        # Points for Awards
        for award in season.get('awards', []):
            season_score += points_system.get(award, 0)
        
        # Points for Team Achievements
        for achievement in season.get('team_achievements', []):
            if achievement in ['Copa del Rey', 'Supercopa de España']:
                season_score += points_system.get('Other Trophies', 0)
            # La Liga Title and Champions League Win are already counted in career totals
        
        # Cup Final Winner
        if season.get('cup_final_winner', False):
            season_score += points_system.get('Cup Final Winner', 0)
        
        # Points for CL Achievements
        for cl_award in season.get('cl_achievements', []):
            season_score += points_system.get(cl_award, 0)
        
        total_score += season_score
    
    return total_score
