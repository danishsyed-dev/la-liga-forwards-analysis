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
    Validate uploaded CSV format - handles both custom template and football statistics formats
    Returns (is_valid, message)
    """
    format_type = detect_csv_format(df)
    
    if format_type == 'football_stats':
        return validate_football_stats_format(df)
    elif format_type == 'custom_template':
        return validate_custom_template_format(df)
    else:
        # Try both validations and return the more informative error
        custom_valid, custom_msg = validate_custom_template_format(df)
        football_valid, football_msg = validate_football_stats_format(df)
        
        if not custom_valid and not football_valid:
            return False, f"CSV format not recognized.\n\n**Custom Template Format**: {custom_msg}\n\n**Football Stats Format**: {football_msg}"
        elif custom_valid:
            return True, custom_msg
        else:
            return True, football_msg


def validate_football_stats_format(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate football statistics CSV format
    Returns (is_valid, message)
    """
    # Required columns for football stats
    required_columns = ['Player']
    recommended_columns = ['Goals', 'Assists', 'Squad', 'Pos']
    
    # Check for required columns
    missing_required = [col for col in required_columns if col not in df.columns]
    if missing_required:
        available_cols = ', '.join(df.columns[:10])
        if len(df.columns) > 10:
            available_cols += f"... (+{len(df.columns)-10} more)"
        return False, f"Missing required columns: {', '.join(missing_required)}\n\nAvailable columns: {available_cols}\n\n💡 For football statistics, we need at least: Player"
    
    # Check for recommended columns
    missing_recommended = [col for col in recommended_columns if col not in df.columns]
    recommendations = []
    if missing_recommended:
        recommendations.append(f"Consider adding columns: {', '.join(missing_recommended)}")
    
    # Check player names
    if df['Player'].isnull().any() or (df['Player'] == '').any():
        empty_count = df['Player'].isnull().sum() + (df['Player'] == '').sum()
        return False, f"Found {empty_count} empty player names. Please ensure all players have names."
    
    # Basic stats
    num_players = len(df)
    has_goals = 'Goals' in df.columns
    has_assists = 'Assists' in df.columns
    
    success_msg = f"✅ Valid football statistics format! Found {num_players} players"
    if has_goals:
        try:
            total_goals = pd.to_numeric(df['Goals'], errors='coerce').sum()
            if not pd.isna(total_goals):
                success_msg += f" with {int(total_goals)} total goals"
        except:
            pass
    
    if recommendations:
        success_msg += f"\n\n💡 {'; '.join(recommendations)}"
    
    return True, success_msg


def validate_custom_template_format(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate custom template CSV format (original validation)
    Returns (is_valid, message)
    """
    required_columns = [
        'player_name', 
        'career_goals', 
        'total_la_liga_titles', 
        'total_champions_league_titles'
    ]
    
    # Create a mapping of column names (case-insensitive, flexible matching)
    df_columns_lower = [col.lower().strip() for col in df.columns]
    
    # Check for required columns with flexible matching
    missing_columns = []
    found_columns = {}
    
    for req_col in required_columns:
        req_col_lower = req_col.lower()
        found = False
        
        # Try exact match first
        if req_col in df.columns or req_col_lower in df_columns_lower:
            found = True
            found_columns[req_col] = req_col if req_col in df.columns else df.columns[df_columns_lower.index(req_col_lower)]
        else:
            # Try partial matches for common variations
            for df_col, df_col_lower in zip(df.columns, df_columns_lower):
                if any(keyword in df_col_lower for keyword in req_col_lower.split('_')):
                    found = True
                    found_columns[req_col] = df_col
                    break
        
        if not found:
            missing_columns.append(req_col)
    
    if missing_columns:
        available_cols = ', '.join(df.columns[:10])  # Show first 10 columns
        if len(df.columns) > 10:
            available_cols += f"... (+{len(df.columns)-10} more)"
        return False, f"Missing required columns: {', '.join(missing_columns)}\n\nAvailable columns: {available_cols}\n\n💡 Required columns should be: player_name, career_goals, total_la_liga_titles, total_champions_league_titles"
    
    # Check data types for numeric columns
    numeric_columns = ['career_goals', 'total_la_liga_titles', 'total_champions_league_titles']
    for req_col in numeric_columns:
        if req_col in found_columns:
            actual_col = found_columns[req_col]
            try:
                # Try to convert to numeric, allowing for some flexibility
                numeric_data = pd.to_numeric(df[actual_col], errors='coerce')
                if numeric_data.isna().all():
                    return False, f"Column '{actual_col}' must contain numeric values (found all non-numeric data)"
                elif numeric_data.isna().sum() > len(df) * 0.5:  # More than 50% are NaN
                    return False, f"Column '{actual_col}' has too many non-numeric values. Please check your data format."
            except Exception as e:
                return False, f"Column '{actual_col}' validation failed: {str(e)}"
    
    # Check for empty player names
    player_col = found_columns.get('player_name', 'player_name')
    if player_col in df.columns:
        if df[player_col].isnull().any() or (df[player_col] == '').any():
            empty_count = df[player_col].isnull().sum() + (df[player_col] == '').sum()
            return False, f"Found {empty_count} empty player names. Please ensure all players have names."
    
    return True, f"✅ Valid custom template format! Found {len(df)} players with required columns."


def process_uploaded_data(df: pd.DataFrame) -> Dict:
    """
    Convert uploaded CSV to internal data structure compatible with existing analysis
    Automatically detects and handles both custom template and football statistics formats
    """
    # Detect the format of the uploaded data
    format_type = detect_csv_format(df)
    
    if format_type == 'football_stats':
        # Use football statistics transformation
        return transform_football_stats_data(df)
    elif format_type == 'custom_template':
        # Use original custom template processing
        return process_custom_template_data(df)
    else:
        # Try to process as custom template by default
        return process_custom_template_data(df)


def process_custom_template_data(df: pd.DataFrame) -> Dict:
    """
    Convert custom template CSV to internal data structure (original functionality)
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

def diagnose_csv_issues(uploaded_file) -> str:
    """
    Diagnose common CSV issues and provide helpful suggestions
    """
    try:
        uploaded_file.seek(0)
        
        # Read first few lines as text to analyze structure
        first_lines = []
        for i, line in enumerate(uploaded_file):
            if i >= 5:  # Just check first 5 lines
                break
            if isinstance(line, bytes):
                line = line.decode('utf-8', errors='ignore')
            first_lines.append(line.strip())
        
        analysis = []
        analysis.append("📋 **CSV Structure Analysis:**\n")
        
        # Check common separators
        separators = {',': 'comma', ';': 'semicolon', '\t': 'tab', '|': 'pipe'}
        separator_counts = {}
        
        for line in first_lines[:2]:  # Check header and first data row
            for sep, name in separators.items():
                count = line.count(sep)
                if sep not in separator_counts:
                    separator_counts[sep] = []
                separator_counts[sep].append(count)
        
        # Analyze separator consistency
        for sep, name in separators.items():
            if sep in separator_counts and separator_counts[sep]:
                avg_count = sum(separator_counts[sep]) / len(separator_counts[sep])
                if avg_count > 0:
                    analysis.append(f"- **{name.title()} ({sep})**: {avg_count:.1f} per line")
        
        # Check for quotes
        has_quotes = any('"' in line for line in first_lines)
        analysis.append(f"- **Quotes**: {'Found' if has_quotes else 'Not found'}")
        
        # Check line length consistency
        line_lengths = [len(line) for line in first_lines if line.strip()]
        if line_lengths:
            avg_length = sum(line_lengths) / len(line_lengths)
            analysis.append(f"- **Average line length**: {avg_length:.0f} characters")
        
        analysis.append(f"\n**First few lines:**")
        for i, line in enumerate(first_lines[:3]):
            analysis.append(f"{i+1}. `{line[:100]}{'...' if len(line) > 100 else ''}`")
        
        return "\n".join(analysis)
        
    except Exception as e:
        return f"Could not analyze file: {str(e)}"

def transform_football_stats_data(df: pd.DataFrame) -> Dict:
    """
    Transform real football statistics CSV data to internal format
    Handles data with columns like Player, Squad, Goals, Assists, etc.
    Returns processed player data compatible with the analysis system
    """
    processed_players = {}
    
    # Get column mappings (flexible to handle different naming)
    player_col = 'Player' if 'Player' in df.columns else None
    goals_col = 'Goals' if 'Goals' in df.columns else None
    assists_col = 'Assists' if 'Assists' in df.columns else None
    squad_col = 'Squad' if 'Squad' in df.columns else None
    
    if not player_col:
        return {}
    
    for _, row in df.iterrows():
        player_name = str(row[player_col]).strip()
        
        if not player_name or player_name == 'nan':
            continue
            
        # Extract available data
        goals = 0
        assists = 0
        squad = "Unknown"
        
        try:
            if goals_col and pd.notna(row[goals_col]):
                goals = int(float(row[goals_col]))
        except (ValueError, TypeError):
            goals = 0
            
        try:
            if assists_col and pd.notna(row[assists_col]):
                assists = int(float(row[assists_col]))
        except (ValueError, TypeError):
            assists = 0
            
        if squad_col and pd.notna(row[squad_col]):
            squad = str(row[squad_col]).strip()
        
        # Create basic career data structure
        # Since we don't have historical data, we'll use current season stats
        career_data = {
            'career_goals': goals,  # Use current season goals as approximation
            'total_la_liga_titles': 0,  # Not available in stats data
            'total_champions_league_titles': 0,  # Not available in stats data
            'seasons': []
        }
        
        # Create a single season entry with available data
        if goals > 0 or assists > 0:
            season = {
                'season': '2022/2023',  # Based on your CSV filename
                'goals': goals,
                'assists': assists,
                'awards': [],
                'team_achievements': [],
                'cup_final_winner': False,
                'cl_achievements': [],
                'squad': squad
            }
            
            # Add some basic awards based on performance
            if goals >= 20:
                season['awards'].append('Top Scorer Candidate')
            if assists >= 10:
                season['awards'].append('Top Assists Provider')
            
            career_data['seasons'].append(season)
        
        # Add empty career awards for now
        career_data['career_awards'] = []
        
        processed_players[player_name] = career_data
    
    return processed_players


def detect_csv_format(df: pd.DataFrame) -> str:
    """
    Detect if CSV is in football statistics format or custom template format
    Returns 'football_stats' or 'custom_template'
    """
    # Check for football statistics columns
    football_cols = ['Player', 'Squad', 'Goals', 'Assists', 'Pos', 'Comp']
    has_football_cols = sum(1 for col in football_cols if col in df.columns)
    
    # Check for custom template columns
    template_cols = ['player_name', 'career_goals', 'total_la_liga_titles', 'total_champions_league_titles']
    has_template_cols = sum(1 for col in template_cols if col in df.columns)
    
    if has_football_cols >= 4:  # At least 4 football stat columns
        return 'football_stats'
    elif has_template_cols >= 3:  # At least 3 template columns
        return 'custom_template'
    else:
        return 'unknown'


def validate_and_preview_data(uploaded_file) -> Tuple[bool, pd.DataFrame, str]:
    """
    Validate uploaded file and return preview
    Returns (success, dataframe, message)
    """
    try:
        # Reset file pointer to beginning
        uploaded_file.seek(0)
        
        # Try different delimiters and encodings
        delimiters = [',', ';', '\t', '|']
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        df = None
        successful_params = None
        
        for encoding in encodings:
            for delimiter in delimiters:
                try:
                    uploaded_file.seek(0)  # Reset file pointer
                    
                    # Read with specific delimiter and encoding
                    df = pd.read_csv(
                        uploaded_file, 
                        delimiter=delimiter, 
                        encoding=encoding,
                        skipinitialspace=True,
                        quotechar='"',
                        na_values=['', 'NA', 'N/A', 'null', 'NULL']
                    )
                    
                    # Check if we got reasonable results
                    if len(df.columns) >= 4 and len(df) > 0:
                        successful_params = (delimiter, encoding)
                        break
                        
                except Exception as e:
                    continue
                    
            if df is not None and successful_params:
                break
        
        if df is None or df.empty:
            return False, pd.DataFrame(), "Could not parse CSV file. Please check the format and try again."
        
        # Clean column names - remove extra spaces
        df.columns = df.columns.str.strip()
        
        # Show parsing info
        delimiter_used, encoding_used = successful_params if successful_params else (',', 'utf-8')
        
        # Validate format - this will automatically detect the format type
        is_valid, validation_message = validate_csv_format(df)
        
        if not is_valid:
            return False, df, f"{validation_message}\n\n📋 Parsed with delimiter: '{delimiter_used}', encoding: '{encoding_used}'"
        
        # Show success info based on detected format
        format_type = detect_csv_format(df)
        num_players = len(df)
        
        if format_type == 'football_stats':
            total_goals = 0
            if 'Goals' in df.columns:
                try:
                    total_goals = pd.to_numeric(df['Goals'], errors='coerce').sum()
                    if pd.isna(total_goals):
                        total_goals = 0
                except:
                    total_goals = 0
            
            success_message = f"✅ Football statistics format detected! Found {num_players} players"
            if total_goals > 0:
                success_message += f" with {int(total_goals)} total goals"
            success_message += f"\n📋 Parsed with delimiter: '{delimiter_used}', encoding: '{encoding_used}'"
        else:
            # Custom template format
            total_goals = df['career_goals'].sum() if 'career_goals' in df.columns else 0
            success_message = f"✅ Custom template format detected! Found {num_players} players with {total_goals} total career goals\n📋 Parsed with delimiter: '{delimiter_used}', encoding: '{encoding_used}'"
        
        return True, df, success_message
        
    except Exception as e:
        return False, pd.DataFrame(), f"Error reading file: {str(e)}\n\n💡 Tips:\n- Ensure your CSV uses comma (,) or semicolon (;) separators\n- Save as CSV (UTF-8) format\n- Check for special characters in player names"
