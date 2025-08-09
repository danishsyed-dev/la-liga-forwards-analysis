import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add scripts directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from players_data import players, points_system
from analysis import calculate_player_score

# Configure page
st.set_page_config(
    page_title="La Liga Forwards Analysis",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("⚽ La Liga Greatest Forwards Analysis")
st.markdown("""
This interactive dashboard analyzes the greatest forwards in La Liga history using a comprehensive scoring system 
that considers goals, assists, titles, awards, and individual achievements.
""")

# Sidebar
st.sidebar.header("🔧 Controls")
st.sidebar.markdown("Use the controls below to customize your analysis:")

# Calculate scores
@st.cache_data
def calculate_all_scores():
    player_scores = {}
    detailed_stats = {}
    
    for player_name, data in players.items():
        score = calculate_player_score(data, points_system)
        player_scores[player_name] = score
        
        # Calculate detailed stats
        stats = {
            'Career Goals': data.get('career_goals', 0),
            'La Liga Titles': data.get('total_la_liga_titles', 0),
            'Champions League Titles': data.get('total_champions_league_titles', 0),
            'Ballon d\'Or Wins': data.get('career_awards', []).count('Ballon d\'Or Win'),
            'Total Score': score
        }
        
        # Count season achievements
        golden_boots = 0
        seasons_20_goals = 0
        seasons_10_assists = 0
        cup_final_wins = 0
        cl_top_scorer = 0
        
        for season in data.get('seasons', []):
            if 'La Liga Golden Boot' in season.get('awards', []):
                golden_boots += 1
            if season.get('goals', 0) >= 20:
                seasons_20_goals += 1
            if season.get('assists', 0) >= 10:
                seasons_10_assists += 1
            if season.get('cup_final_winner', False):
                cup_final_wins += 1
            cl_achievements = season.get('cl_achievements', [])
            cl_top_scorer += cl_achievements.count('CL Top Scorer')
        
        stats.update({
            'La Liga Golden Boots': golden_boots,
            '20+ Goal Seasons': seasons_20_goals,
            '10+ Assist Seasons': seasons_10_assists,
            'Cup Final Wins': cup_final_wins,
            'CL Top Scorer Awards': cl_top_scorer
        })
        
        detailed_stats[player_name] = stats
    
    # Create DataFrames
    scores_df = pd.DataFrame(list(player_scores.items()), columns=['Player', 'Score'])
    scores_df = scores_df.sort_values(by='Score', ascending=False).reset_index(drop=True)
    
    stats_df = pd.DataFrame.from_dict(detailed_stats, orient='index')
    stats_df.reset_index(inplace=True)
    stats_df.rename(columns={'index': 'Player'}, inplace=True)
    
    return scores_df, stats_df

# Get data
scores_df, stats_df = calculate_all_scores()

# Player selection
st.sidebar.subheader("👤 Player Selection")
selected_players = st.sidebar.multiselect(
    "Select players to compare:",
    options=scores_df['Player'].tolist(),
    default=scores_df['Player'].head(3).tolist()
)

# Chart type selection
st.sidebar.subheader("📊 Visualization Type")
chart_type = st.sidebar.selectbox(
    "Choose chart type:",
    ["Bar Chart", "Radar Chart", "Detailed Stats", "Season Analysis"]
)

# Main content
if chart_type == "Bar Chart":
    st.header("📊 Player Rankings - Bar Chart")
    
    if selected_players:
        filtered_df = scores_df[scores_df['Player'].isin(selected_players)]
        
        fig = px.bar(
            filtered_df, 
            x='Player', 
            y='Score',
            title="La Liga Forwards Total Scores",
            color='Score',
            color_continuous_scale='viridis'
        )
        fig.update_layout(
            xaxis_title="Player",
            yaxis_title="Total Points",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Show detailed breakdown
        st.subheader("🔍 Score Breakdown")
        breakdown_df = stats_df[stats_df['Player'].isin(selected_players)][
            ['Player', 'Career Goals', 'La Liga Titles', 'Champions League Titles', 
             'Ballon d\'Or Wins', 'Total Score']
        ]
        st.dataframe(breakdown_df, use_container_width=True)
    else:
        st.warning("Please select at least one player to display the chart.")

elif chart_type == "Radar Chart":
    st.header("🎯 Player Comparison - Radar Chart")
    
    if selected_players:
        # Prepare radar chart data
        radar_metrics = ['Career Goals', 'La Liga Titles', 'Champions League Titles',
                        'Ballon d\'Or Wins', 'La Liga Golden Boots', '20+ Goal Seasons',
                        '10+ Assist Seasons', 'Cup Final Wins', 'CL Top Scorer Awards']
        
        filtered_stats = stats_df[stats_df['Player'].isin(selected_players)]
        
        # Normalize data for radar chart
        normalized_stats = filtered_stats.copy()
        for metric in radar_metrics:
            max_val = stats_df[metric].max()
            min_val = stats_df[metric].min()
            if max_val > min_val:
                normalized_stats[metric] = (normalized_stats[metric] - min_val) / (max_val - min_val)
            else:
                normalized_stats[metric] = 0
        
        # Create radar chart
        fig = go.Figure()
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9F43', '#A55EEA']
        
        for i, (_, player_data) in enumerate(normalized_stats.iterrows()):
            fig.add_trace(go.Scatterpolar(
                r=[player_data[metric] for metric in radar_metrics],
                theta=radar_metrics,
                fill='toself',
                name=player_data['Player'],
                line_color=colors[i % len(colors)],
                fillcolor=colors[i % len(colors)],
                opacity=0.1
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title="La Liga Forwards Comparison - Radar Chart",
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show raw stats for reference
        st.subheader("📋 Raw Statistics")
        display_stats = filtered_stats[['Player'] + radar_metrics]
        st.dataframe(display_stats, use_container_width=True)
    else:
        st.warning("Please select at least one player to display the radar chart.")

elif chart_type == "Detailed Stats":
    st.header("📈 Detailed Player Statistics")
    
    if selected_players:
        filtered_stats = stats_df[stats_df['Player'].isin(selected_players)]
        
        # Create multiple charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Goals vs Titles scatter plot
            fig_scatter = px.scatter(
                filtered_stats,
                x='Career Goals',
                y='La Liga Titles',
                size='Champions League Titles',
                color='Ballon d\'Or Wins',
                hover_name='Player',
                title="Goals vs La Liga Titles (Size: CL Titles, Color: Ballon d'Or)"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        with col2:
            # Awards comparison
            awards_data = filtered_stats[['Player', 'Ballon d\'Or Wins', 'La Liga Golden Boots', 'CL Top Scorer Awards']]
            fig_awards = px.bar(
                awards_data.melt(id_vars='Player', var_name='Award', value_name='Count'),
                x='Player',
                y='Count',
                color='Award',
                title="Individual Awards Comparison",
                barmode='group'
            )
            st.plotly_chart(fig_awards, use_container_width=True)
        
        # Complete stats table
        st.subheader("🗂️ Complete Statistics Table")
        st.dataframe(filtered_stats, use_container_width=True)
    else:
        st.warning("Please select at least one player to display detailed statistics.")

elif chart_type == "Season Analysis":
    st.header("⏰ Season-by-Season Analysis")
    
    # Player selector for season analysis
    season_player = st.selectbox("Select a player for season analysis:", scores_df['Player'].tolist())
    
    if season_player:
        player_data = players[season_player]
        seasons_data = []
        
        for season in player_data['seasons']:
            season_info = {
                'Season': season['season'],
                'Goals': season['goals'],
                'Assists': season['assists'],
                'Awards': ', '.join(season.get('awards', [])),
                'Team Achievements': ', '.join(season.get('team_achievements', [])),
                'CL Achievements': ', '.join(season.get('cl_achievements', [])),
                'Cup Final Winner': '✅' if season.get('cup_final_winner', False) else '❌'
            }
            seasons_data.append(season_info)
        
        seasons_df = pd.DataFrame(seasons_data)
        
        # Goals and assists chart
        col1, col2 = st.columns(2)
        
        with col1:
            fig_goals = px.bar(
                seasons_df,
                x='Season',
                y='Goals',
                title=f"{season_player} - Goals per Season"
            )
            st.plotly_chart(fig_goals, use_container_width=True)
        
        with col2:
            fig_assists = px.bar(
                seasons_df,
                x='Season',
                y='Assists',
                title=f"{season_player} - Assists per Season"
            )
            st.plotly_chart(fig_assists, use_container_width=True)
        
        # Season details table
        st.subheader("📋 Season Details")
        st.dataframe(seasons_df, use_container_width=True)

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.subheader("ℹ️ Scoring System")
st.sidebar.markdown("""
**Points System:**
- Ballon d'Or Win: 5 pts
- Champions League Win: 5 pts
- La Liga Best Player: 4 pts
- La Liga Golden Boot: 3 pts
- 20+ Goal Season: 2 pts
- La Liga Title: 1 pt
- And more...
""")

st.sidebar.markdown("---")
st.sidebar.markdown("**Created by:** Danish Syed")
st.sidebar.markdown("**Data:** La Liga Historical Records")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>⚽ La Liga Greatest Forwards Analysis | Built with Streamlit | 
    <a href="https://github.com/danishsyed-dev/la-liga-forwards-analysis" target="_blank">View on GitHub</a></p>
</div>
""", unsafe_allow_html=True)
