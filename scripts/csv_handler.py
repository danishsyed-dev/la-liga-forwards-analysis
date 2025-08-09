"""
CSV Handler for Dynamic Player Data Analysis
Handles CSV upload, validation, and conversion for the La Liga Forwards Analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, List
import streamlit as st


def create_csv_template() -> str:
    """Create a CSV template for users to download with proper format"""
    template_data = {
        'player_name': [
            'Example Player 1', 
            'Example Player 2', 
            'Example Player 3'
        ],
        'career_goals': [250, 180, 320],
        'total_la_liga_titles': [3, 1, 5],
        'total_champions_league_titles': [2, 0, 4],
        'ballon_dor_wins': [1, 0, 2],
        'la_liga_golden_boots': [2, 1, 3],
        'la_liga_best_player_awards': [1, 0, 2],
        
        # Season 1 data
        'season_1_goals': [35, 25, 42],
        'season_1_assists': [12, 8, 15],
        'season_1_awards': [
            'La Liga Golden Boot,La Liga Best Player Award', 
            '', 
            'Ballon d\'Or Win,La Liga Golden Boot'
        ],
        'season_1_team_achievements': [
            'La Liga Title,Copa del Rey',
            'Copa del Rey',
            'La Liga Title,Champions League Win'
        ],
        
        # Season 2 data
        'season_2_goals': [40, 30, 38],
        'season_2_assists': [15, 10, 12],
        'season_2_awards': [
            'Ballon d\'Or Win,La Liga Golden Boot', 
            'La Liga Golden Boot', 
            'La Liga Best Player Award'
        ],
        'season_2_team_achievements': [
            'Champions League Win,La Liga Title',
            'La Liga Title',
            'Copa del Rey'
        ],
        
        # Season 3 data
        'season_3_goals': [38, 22, 35],
        'season_3_assists': [10, 6, 18],
        'season_3_awards': [
            'La Liga Best Player Award', 
            '', 
            'Ballon d\'Or Win,La Liga Golden Boot,Most Assists in La Liga Season'
        ],
        'season_3_team_achievements': [
            'La Liga Title',
            '',
            'Champions League Win,La Liga Title'
        ]
    }
    
    template_df = pd.DataFrame(template_data)
    return template_df.to_csv(index=False)

def create_simple_template() -> str:
    """Create a simplified CSV template for easier user input"""
    simple_data = {
        'player_name': [
            'Lionel Messi Example',
            'Cristiano Ronaldo Example', 
            'Your Player Name'
        ],
        'career_goals': [474, 311, 150],
        'total_la_liga_titles': [10, 2, 1],
        'total_champions_league_titles': [4, 4, 0],
        'ballon_dor_wins': [4, 4, 0],
        'best_season_goals': [50, 48, 25],
        'best_season_assists': [18, 16, 10],
        'main_awards': [
            'Ballon d\'Or Win,La Liga Golden Boot',
            'Ballon d\'Or Win,La Liga Golden Boot',
            'Your Awards Here'
        ],
        'notes': [
            'Barcelona Legend',
            'Real Madrid Legend',
            'Add your notes'
        ]
    }
    
    simple_df = pd.DataFrame(simple_data)
    return simple_df.to_csv(index=False)


def validate_csv_format(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate uploaded CSV format
    Returns (is_valid, message)
    """
    required_columns = [
        'player_name', 
        'career_goals', 
        'total_la_liga_titles', 
        'total_champions_league_titles'
    ]
    
    # Check for required columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    # Check data types
    numeric_columns = ['career_goals', 'total_la_liga_titles', 'total_champions_league_titles']
    for col in numeric_columns:
        if col in df.columns:
            try:
                pd.to_numeric(df[col], errors='raise')
            except:
                return False, f"Column '{col}' must contain numeric values"
    
    # Check for empty player names
    if df['player_name'].isnull().any() or (df['player_name'] == '').any():
        return False, "Player names cannot be empty"
    
    return True, "Valid format"


def process_uploaded_data(df: pd.DataFrame) -> Dict:
    """
    Convert uploaded CSV to internal data structure compatible with existing analysis
    """
    processed_players = {}
    
    for _, row in df.iterrows():
        player_name = str(row['player_name']).strip()
        
        if not player_name:
            continue
            
        # Extract basic career data
        career_data = {
            'career_goals': int(row.get('career_goals', 0)),
            'total_la_liga_titles': int(row.get('total_la_liga_titles', 0)),
            'total_champions_league_titles': int(row.get('total_champions_league_titles', 0)),
            'seasons': []
        }
        
        # Process career awards
        ballon_dor_wins = int(row.get('ballon_dor_wins', 0))
        career_data['career_awards'] = ['Ballon d\'Or Win'] * ballon_dor_wins
        
        # Extract season data (up to 3 seasons)
        for i in range(1, 4):
            goals_col = f'season_{i}_goals'
            assists_col = f'season_{i}_assists'
            awards_col = f'season_{i}_awards'
            achievements_col = f'season_{i}_team_achievements'
            
            if goals_col in row and pd.notna(row[goals_col]) and row[goals_col] != '':
                try:
                    goals = int(float(row[goals_col]))
                    assists = int(float(row.get(assists_col, 0))) if pd.notna(row.get(assists_col, 0)) else 0
                    
                    # Process awards
                    awards_str = str(row.get(awards_col, ''))
                    awards = [award.strip() for award in awards_str.split(',') if award.strip()]
                    
                    # Process team achievements
                    achievements_str = str(row.get(achievements_col, ''))
                    team_achievements = [ach.strip() for ach in achievements_str.split(',') if ach.strip()]
                    
                    season = {
                        'season': f'{2020 + i}/{2021 + i}',  # Example seasons
                        'goals': goals,
                        'assists': assists,
                        'awards': awards,
                        'team_achievements': team_achievements,
                        'cup_final_winner': 'Copa del Rey' in team_achievements,
                        'cl_achievements': []
                    }
                    
                    # Add CL achievements if Champions League Win is in team achievements
                    if 'Champions League Win' in team_achievements:
                        if goals >= 10:  # Assume top scorer if high goals
                            season['cl_achievements'].append('CL Top Scorer')
                    
                    career_data['seasons'].append(season)
                    
                except (ValueError, TypeError):
                    continue  # Skip invalid season data
        
        processed_players[player_name] = career_data
    
    return processed_players


def export_analysis_results(scores_df: pd.DataFrame, stats_df: pd.DataFrame) -> Tuple[str, str]:
    """
    Export analysis results as CSV strings
    Returns (scores_csv, stats_csv)
    """
    scores_csv = scores_df.to_csv(index=False)
    stats_csv = stats_df.to_csv(index=False)
    
    return scores_csv, stats_csv


def create_data_info_panel():
    """Create an informational panel about CSV data format"""
    st.markdown("""
    ### 📋 CSV Data Format Guide
    
    **Required Columns:**
    - `player_name`: Player's full name
    - `career_goals`: Total career goals (integer)
    - `total_la_liga_titles`: Number of league titles (integer)  
    - `total_champions_league_titles`: Number of CL titles (integer)
    
    **Optional Columns:**
    - `ballon_dor_wins`: Number of Ballon d'Or wins
    - `season_X_goals`: Goals in season X (X = 1, 2, 3)
    - `season_X_assists`: Assists in season X
    - `season_X_awards`: Awards in season X (comma-separated)
    - `season_X_team_achievements`: Team achievements (comma-separated)
    
    **Example Awards:**
    - `Ballon d'Or Win`
    - `La Liga Golden Boot`
    - `La Liga Best Player Award`
    - `Most Assists in La Liga Season`
    
    **Example Team Achievements:**
    - `La Liga Title`
    - `Champions League Win`
    - `Copa del Rey`
    """)


def create_sample_csv_content() -> str:
    """Create realistic sample CSV data for demonstration"""
    sample_data = {
        'player_name': [
            'Lionel Messi',
            'Cristiano Ronaldo', 
            'Luis Suarez',
            'Karim Benzema',
            'Robert Lewandowski'
        ],
        'career_goals': [474, 311, 147, 238, 89],
        'total_la_liga_titles': [10, 2, 4, 5, 0],
        'total_champions_league_titles': [4, 4, 1, 5, 0],
        'ballon_dor_wins': [4, 4, 0, 1, 0],
        'season_1_goals': [50, 46, 40, 27, 23],
        'season_1_assists': [15, 12, 16, 12, 8],
        'season_1_awards': [
            'Ballon d\'Or Win,La Liga Golden Boot',
            'La Liga Golden Boot',
            'La Liga Golden Boot',
            'Ballon d\'Or Win,La Liga Best Player Award',
            ''
        ],
        'season_1_team_achievements': [
            'La Liga Title,Copa del Rey',
            'La Liga Title',
            'La Liga Title,Copa del Rey',
            'La Liga Title,Champions League Win',
            ''
        ],
        'season_2_goals': [43, 35, 29, 24, 0],
        'season_2_assists': [18, 11, 13, 7, 0],
        'season_2_awards': [
            'La Liga Best Player Award',
            'Ballon d\'Or Win',
            '',
            '',
            ''
        ],
        'season_2_team_achievements': [
            'La Liga Title,Champions League Win,Copa del Rey',
            'Champions League Win',
            'Copa del Rey',
            'Champions League Win',
            ''
        ]
    }
    
    sample_df = pd.DataFrame(sample_data)
    return sample_df.to_csv(index=False)

def validate_and_preview_data(uploaded_file) -> Tuple[bool, pd.DataFrame, str]:
    """
    Validate uploaded file and return preview
    Returns (success, dataframe, message)
    """
    try:
        # Read the CSV
        df = pd.read_csv(uploaded_file)
        
        # Validate format
        is_valid, validation_message = validate_csv_format(df)
        
        if not is_valid:
            return False, df, validation_message
        
        # Show basic info
        num_players = len(df)
        total_goals = df['career_goals'].sum() if 'career_goals' in df.columns else 0
        
        success_message = f"✅ Successfully loaded {num_players} players with {total_goals} total career goals"
        
        return True, df, success_message
        
    except Exception as e:
        return False, pd.DataFrame(), f"Error reading file: {str(e)}"
