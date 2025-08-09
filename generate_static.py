#!/usr/bin/env python3
"""
Generate static HTML version of La Liga Forwards Analysis
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
import sys
import os
import json

# Add scripts directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from players_data import players, points_system
from analysis import calculate_player_score

def calculate_all_scores():
    """Calculate scores for all players with accurate data"""
    player_scores = {}
    detailed_stats = {}
    
    for player_name, data in players.items():
        score = calculate_player_score(data, points_system)
        player_scores[player_name] = score
        
        # Calculate detailed stats with proper aggregation
        stats = {
            'Career Goals': data.get('career_goals', 0),
            'La Liga Titles': data.get('total_la_liga_titles', 0),
            'Champions League Titles': data.get('total_champions_league_titles', 0),
            'Ballon d\'Or Wins': data.get('career_awards', []).count('Ballon d\'Or Win'),
            'Total Score': score
        }
        
        # Count season achievements properly
        golden_boots = 0
        seasons_20_goals = 0
        seasons_10_assists = 0
        cup_final_wins = 0
        cl_top_scorer = 0
        la_liga_best_player = 0
        total_season_goals = 0
        total_season_assists = 0
        
        for season in data.get('seasons', []):
            # Count awards
            if 'La Liga Golden Boot' in season.get('awards', []):
                golden_boots += 1
            if 'La Liga Best Player Award' in season.get('awards', []):
                la_liga_best_player += 1
                
            # Count achievements
            if season.get('goals', 0) >= 20:
                seasons_20_goals += 1
            if season.get('assists', 0) >= 10:
                seasons_10_assists += 1
            if season.get('cup_final_winner', False):
                cup_final_wins += 1
                
            # Count CL achievements
            cl_achievements = season.get('cl_achievements', [])
            cl_top_scorer += cl_achievements.count('CL Top Scorer')
            
            # Sum totals
            total_season_goals += season.get('goals', 0)
            total_season_assists += season.get('assists', 0)
        
        stats.update({
            'La Liga Golden Boots': golden_boots,
            'La Liga Best Player Awards': la_liga_best_player,
            '20+ Goal Seasons': seasons_20_goals,
            '10+ Assist Seasons': seasons_10_assists,
            'Cup Final Wins': cup_final_wins,
            'CL Top Scorer Awards': cl_top_scorer,
            'Season Goals (Sample)': total_season_goals,
            'Season Assists (Sample)': total_season_assists
        })
        
        detailed_stats[player_name] = stats
    
    # Create DataFrames
    scores_df = pd.DataFrame(list(player_scores.items()), columns=['Player', 'Score'])
    scores_df = scores_df.sort_values(by='Score', ascending=False).reset_index(drop=True)
    scores_df['Rank'] = scores_df.index + 1
    
    stats_df = pd.DataFrame.from_dict(detailed_stats, orient='index')
    stats_df.reset_index(inplace=True)
    stats_df.rename(columns={'index': 'Player'}, inplace=True)
    
    return scores_df, stats_df

def create_bar_chart(scores_df):
    """Create improved interactive bar chart"""
    # Add custom colors based on ranking
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
    
    fig = px.bar(
        scores_df, 
        x='Player', 
        y='Score',
        title="🏆 La Liga Greatest Forwards - Overall Rankings",
        color='Score',
        color_continuous_scale='Blues',
        height=700,
        text='Score'
    )
    
    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Total Points: %{y}<br>Rank: #%{customdata}<extra></extra>',
        customdata=scores_df['Rank']
    )
    
    fig.update_layout(
        xaxis_title="<b>Player</b>",
        yaxis_title="<b>Total Points</b>",
        font=dict(size=14, family="Arial, sans-serif"),
        title_font_size=24,
        title_x=0.5,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=80, b=100, l=60, r=60),
        xaxis=dict(
            tickangle=-45,
            gridcolor='rgba(128,128,128,0.2)'
        ),
        yaxis=dict(
            gridcolor='rgba(128,128,128,0.2)'
        )
    )
    return fig

def create_radar_chart(stats_df):
    """Create improved radar chart for top 5 players"""
    # Select top 5 players
    top_players = stats_df.nlargest(5, 'Total Score')
    
    radar_metrics = [
        'Career Goals', 'La Liga Titles', 'Champions League Titles',
        'Ballon d\'Or Wins', 'La Liga Golden Boots', '20+ Goal Seasons',
        'La Liga Best Player Awards', 'CL Top Scorer Awards'
    ]
    
    # Normalize data for radar chart (0-1 scale)
    normalized_stats = top_players.copy()
    for metric in radar_metrics:
        max_val = stats_df[metric].max()
        min_val = stats_df[metric].min()
        if max_val > min_val:
            normalized_stats[metric] = (normalized_stats[metric] - min_val) / (max_val - min_val)
        else:
            normalized_stats[metric] = 0.5  # Default middle value if all same
    
    # Create radar chart with better colors
    fig = go.Figure()
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']
    
    for i, (_, player_data) in enumerate(normalized_stats.iterrows()):
        fig.add_trace(go.Scatterpolar(
            r=[player_data[metric] for metric in radar_metrics],
            theta=radar_metrics,
            fill='toself',
            name=player_data['Player'],
            line_color=colors[i % len(colors)],
            fillcolor=colors[i % len(colors)],
            opacity=0.15,
            line=dict(width=3)
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickvals=[0, 0.25, 0.5, 0.75, 1],
                ticktext=['0%', '25%', '50%', '75%', '100%']
            ),
            angularaxis=dict(
                tickfont_size=12
            )
        ),
        showlegend=True,
        title="🎯 Top 5 Players - Multi-Dimensional Comparison",
        height=800,
        font=dict(size=14, family="Arial, sans-serif"),
        title_font_size=24,
        title_x=0.5,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_scatter_plot(stats_df):
    """Create improved scatter plot"""
    fig = px.scatter(
        stats_df,
        x='Career Goals',
        y='Total Score',
        size='Champions League Titles',
        color='Ballon d\'Or Wins',
        hover_name='Player',
        title="📈 Career Goals vs Total Score Analysis",
        height=600,
        size_max=30,
        color_continuous_scale='viridis'
    )
    
    # Add custom hover template
    fig.update_traces(
        hovertemplate='<b>%{hovertext}</b><br>' +
                      'Career Goals: %{x}<br>' +
                      'Total Score: %{y}<br>' +
                      'Champions League Titles: %{marker.size}<br>' +
                      'Ballon d\'Or Wins: %{marker.color}<extra></extra>'
    )
    
    fig.update_layout(
        xaxis_title="<b>Career Goals in La Liga</b>",
        yaxis_title="<b>Total Score</b>",
        font=dict(size=14, family="Arial, sans-serif"),
        title_font_size=20,
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(128,128,128,0.2)'),
        yaxis=dict(gridcolor='rgba(128,128,128,0.2)')
    )
    
    return fig

def create_achievements_chart(stats_df):
    """Create awards comparison chart"""
    awards_cols = ['Ballon d\'Or Wins', 'La Liga Golden Boots', 'La Liga Best Player Awards', 'CL Top Scorer Awards']
    
    fig = go.Figure()
    
    for col in awards_cols:
        fig.add_trace(go.Bar(
            name=col.replace('Awards', '').replace('Wins', ''),
            x=stats_df['Player'],
            y=stats_df[col],
            text=stats_df[col],
            textposition='auto'
        ))
    
    fig.update_layout(
        title="🏆 Individual Awards Comparison",
        xaxis_title="<b>Player</b>",
        yaxis_title="<b>Number of Awards</b>",
        barmode='group',
        height=600,
        font=dict(size=14, family="Arial, sans-serif"),
        title_font_size=20,
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            tickangle=-45,
            gridcolor='rgba(128,128,128,0.2)'
        ),
        yaxis=dict(gridcolor='rgba(128,128,128,0.2)'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def generate_html_page():
    """Generate the complete HTML page with improved UI"""
    scores_df, stats_df = calculate_all_scores()
    
    # Create all charts
    bar_chart = create_bar_chart(scores_df)
    radar_chart = create_radar_chart(stats_df)
    scatter_chart = create_scatter_plot(stats_df)
    achievements_chart = create_achievements_chart(stats_df)
    
    # Convert charts to HTML
    bar_html = pyo.plot(bar_chart, output_type='div', include_plotlyjs=False)
    radar_html = pyo.plot(radar_chart, output_type='div', include_plotlyjs=False)
    scatter_html = pyo.plot(scatter_chart, output_type='div', include_plotlyjs=False)
    achievements_html = pyo.plot(achievements_chart, output_type='div', include_plotlyjs=False)
    
    # Create better formatted stats table
    display_stats = stats_df[['Player', 'Total Score', 'Career Goals', 'La Liga Titles', 
                             'Champions League Titles', 'Ballon d\'Or Wins', 'La Liga Golden Boots']].round(0)
    stats_html = display_stats.to_html(
        classes='table table-striped table-hover table-sm', 
        table_id='stats-table', 
        index=False,
        escape=False
    )
    
    # Generate complete improved HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚽ La Liga Greatest Forwards Analysis</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        :root {{
            --primary-color: #1f77b4;
            --secondary-color: #ff7f0e;
            --success-color: #2ca02c;
            --danger-color: #d62728;
            --dark-color: #2c3e50;
            --light-bg: #f8f9fa;
        }}
        
        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--light-bg);
            line-height: 1.6;
        }}
        
        .hero {{
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--dark-color) 100%);
            color: white;
            padding: 80px 0;
            margin-bottom: 50px;
            position: relative;
            overflow: hidden;
        }}
        
        .hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="rgba(255,255,255,0.1)"/></svg>') repeat;
            animation: float 20s infinite linear;
        }}
        
        @keyframes float {{
            0% {{ transform: translateY(0px) translateX(0px); }}
            100% {{ transform: translateY(-100px) translateX(-100px); }}
        }}
        
        .hero-content {{
            position: relative;
            z-index: 1;
        }}
        
        .navbar {{
            background-color: var(--dark-color) !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .card {{
            border: none;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
            margin-bottom: 40px;
            border-radius: 15px;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.12);
        }}
        
        .card-header {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            border-bottom: none;
            padding: 20px 25px;
        }}
        
        .card-header h3 {{
            margin: 0;
            font-weight: 600;
            font-size: 1.3rem;
        }}
        
        .chart-container {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin: 20px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }}
        
        .stats-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .stats-number {{
            font-size: 2.5rem;
            font-weight: bold;
            display: block;
        }}
        
        .stats-label {{
            font-size: 0.9rem;
            opacity: 0.9;
        }}
        
        #stats-table {{
            font-size: 0.95rem;
            border-radius: 10px;
            overflow: hidden;
        }}
        
        #stats-table th {{
            background: var(--primary-color);
            color: white;
            font-weight: 600;
            border: none;
            padding: 15px;
        }}
        
        #stats-table td {{
            padding: 12px 15px;
            border-color: #e9ecef;
        }}
        
        #stats-table tr:hover {{
            background-color: rgba(31, 119, 180, 0.05);
        }}
        
        .scoring-system {{
            background: linear-gradient(135deg, #2c3e50 0%, #4a6741 100%);
            color: white;
            border-radius: 15px;
            padding: 30px;
        }}
        
        .scoring-system h5 {{
            color: #ffd700;
            margin-bottom: 20px;
        }}
        
        .scoring-system ul li {{
            padding: 5px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        
        .footer {{
            background: linear-gradient(135deg, var(--dark-color) 0%, #1a252f 100%);
            color: white;
            padding: 60px 0 40px;
            margin-top: 80px;
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(31, 119, 180, 0.3);
        }}
        
        .section-divider {{
            height: 4px;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            border: none;
            border-radius: 2px;
            margin: 50px 0;
        }}
        
        @media (max-width: 768px) {{
            .hero {{
                padding: 50px 0;
            }}
            
            .chart-container {{
                padding: 20px 15px;
            }}
            
            .card-header {{
                padding: 15px 20px;
            }}
        }}
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark sticky-top">
        <div class="container">
            <a class="navbar-brand" href="#" style="font-size: 1.5rem; font-weight: bold;">
                <i class="fas fa-futbol me-2"></i>La Liga Analysis
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="#overview"><i class="fas fa-home me-1"></i>Overview</a>
                    <a class="nav-link" href="#rankings"><i class="fas fa-chart-bar me-1"></i>Rankings</a>
                    <a class="nav-link" href="#comparison"><i class="fas fa-radar-chart me-1"></i>Comparison</a>
                    <a class="nav-link" href="#stats"><i class="fas fa-table me-1"></i>Statistics</a>
                </div>
            </div>
        </div>
    </nav>

    <div class="hero" id="overview">
        <div class="hero-content">
            <div class="container text-center">
                <h1 class="display-3 fw-bold mb-4">
                    <i class="fas fa-futbol me-3"></i>La Liga Greatest Forwards
                </h1>
                <p class="lead mb-4 fs-4">Comprehensive Data-Driven Analysis</p>
                <p class="fs-5 mb-4">Advanced scoring system based on goals, assists, titles, and individual achievements</p>
                <div class="row justify-content-center mt-5">
                    <div class="col-md-3 col-sm-6 mb-3">
                        <div class="stats-card">
                            <span class="stats-number">7</span>
                            <span class="stats-label">Legendary Players</span>
                        </div>
                    </div>
                    <div class="col-md-3 col-sm-6 mb-3">
                        <div class="stats-card">
                            <span class="stats-number">15+</span>
                            <span class="stats-label">Metrics Analyzed</span>
                        </div>
                    </div>
                    <div class="col-md-3 col-sm-6 mb-3">
                        <div class="stats-card">
                            <span class="stats-number">50+</span>
                            <span class="stats-label">Major Trophies</span>
                        </div>
                    </div>
                    <div class="col-md-3 col-sm-6 mb-3">
                        <div class="stats-card">
                            <span class="stats-number">1000+</span>
                            <span class="stats-label">Career Goals</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="container" id="rankings">
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title mb-0">
                            <i class="fas fa-trophy me-2"></i>Overall Rankings
                        </h3>
                    </div>
                    <div class="card-body">
                        <div class="chart-container">
                            {bar_html}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <hr class="section-divider">

        <div class="row" id="comparison">
            <div class="col-lg-6 mb-4">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title mb-0">
                            <i class="fas fa-chart-radar me-2"></i>Multi-Dimensional Analysis
                        </h3>
                    </div>
                    <div class="card-body">
                        <div class="chart-container">
                            {radar_html}
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-lg-6 mb-4">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title mb-0">
                            <i class="fas fa-chart-scatter me-2"></i>Goals vs Score Analysis
                        </h3>
                    </div>
                    <div class="card-body">
                        <div class="chart-container">
                            {scatter_html}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title mb-0">
                            <i class="fas fa-medal me-2"></i>Individual Awards Comparison
                        </h3>
                    </div>
                    <div class="card-body">
                        <div class="chart-container">
                            {achievements_html}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <hr class="section-divider">

        <div class="row" id="stats">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title mb-0">
                            <i class="fas fa-table me-2"></i>Comprehensive Statistics
                        </h3>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            {stats_html}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <hr class="section-divider">

        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title mb-0">
                            <i class="fas fa-calculator me-2"></i>Scoring System Explained
                        </h3>
                    </div>
                    <div class="card-body">
                        <div class="scoring-system">
                            <div class="row">
                                <div class="col-md-6">
                                    <h5><i class="fas fa-award me-2"></i>Individual Awards</h5>
                                    <ul class="list-unstyled">
                                        <li><i class="fas fa-star text-warning me-2"></i>Ballon d'Or Win: <strong>5 points</strong></li>
                                        <li><i class="fas fa-crown text-warning me-2"></i>La Liga Best Player: <strong>4 points</strong></li>
                                        <li><i class="fas fa-boot text-warning me-2"></i>La Liga Golden Boot: <strong>3 points</strong></li>
                                        <li><i class="fas fa-trophy text-warning me-2"></i>CL Top Scorer: <strong>5 points</strong></li>
                                        <li><i class="fas fa-medal text-warning me-2"></i>200+ La Liga Goals: <strong>5 points</strong></li>
                                        <li><i class="fas fa-target text-warning me-2"></i>20+ Goal Season: <strong>2 points</strong></li>
                                    </ul>
                                </div>
                                <div class="col-md-6">
                                    <h5><i class="fas fa-users me-2"></i>Team Achievements</h5>
                                    <ul class="list-unstyled">
                                        <li><i class="fas fa-trophy text-primary me-2"></i>Champions League Win: <strong>5 points</strong></li>
                                        <li><i class="fas fa-trophy text-success me-2"></i>La Liga Title: <strong>1 point</strong></li>
                                        <li><i class="fas fa-hands-helping text-info me-2"></i>10+ Assist Season: <strong>1 point</strong></li>
                                        <li><i class="fas fa-cup text-secondary me-2"></i>Cup Final Winner: <strong>1 point</strong></li>
                                        <li><i class="fas fa-certificate text-warning me-2"></i>Other Trophies: <strong>1 point</strong></li>
                                        <li><i class="fas fa-graduation-cap text-info me-2"></i>100+ La Liga Goals: <strong>2 points</strong></li>
                                    </ul>
                                </div>
                            </div>
                            <div class="mt-4 p-3 bg-dark bg-opacity-25 rounded">
                                <h6 class="text-center mb-0">
                                    <i class="fas fa-info-circle me-2"></i>
                                    Scoring combines career achievements, seasonal performance, and team success to rank the greatest La Liga forwards objectively
                                </h6>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="footer">
        <div class="container text-center">
            <div class="row">
                <div class="col-md-12">
                    <h4 class="mb-4">
                        <i class="fas fa-futbol me-2"></i>La Liga Greatest Forwards Analysis
                    </h4>
                    <p class="lead mb-4">Data-driven analysis of La Liga's most legendary forwards</p>
                    <div class="row justify-content-center mb-4">
                        <div class="col-md-3 mb-3">
                            <div class="d-flex flex-column align-items-center">
                                <i class="fas fa-database fa-2x mb-2 text-primary"></i>
                                <span>Comprehensive Data</span>
                            </div>
                        </div>
                        <div class="col-md-3 mb-3">
                            <div class="d-flex flex-column align-items-center">
                                <i class="fas fa-chart-line fa-2x mb-2 text-success"></i>
                                <span>Advanced Analytics</span>
                            </div>
                        </div>
                        <div class="col-md-3 mb-3">
                            <div class="d-flex flex-column align-items-center">
                                <i class="fas fa-trophy fa-2x mb-2 text-warning"></i>
                                <span>Historical Achievements</span>
                            </div>
                        </div>
                        <div class="col-md-3 mb-3">
                            <div class="d-flex flex-column align-items-center">
                                <i class="fas fa-code fa-2x mb-2 text-info"></i>
                                <span>Open Source</span>
                            </div>
                        </div>
                    </div>
                    <div class="mb-4">
                        <a href="https://github.com/danishsyed-dev/la-liga-forwards-analysis" class="btn btn-primary btn-lg me-3">
                            <i class="fab fa-github me-2"></i>View Source Code
                        </a>
                        <a href="https://la-liga-forwards-analysis.streamlit.app" class="btn btn-outline-light btn-lg">
                            <i class="fas fa-play me-2"></i>Interactive Version
                        </a>
                    </div>
                    <hr class="my-4" style="border-color: rgba(255,255,255,0.2);">
                    <div class="row">
                        <div class="col-md-6">
                            <p class="mb-0">
                                <i class="fas fa-code me-1"></i>Built by <strong>Danish Syed</strong>
                            </p>
                        </div>
                        <div class="col-md-6">
                            <p class="mb-0">
                                <i class="fas fa-database me-1"></i>Data from La Liga Historical Records
                            </p>
                        </div>
                    </div>
                    <p class="mt-3 mb-0 text-muted">
                        <small>© 2025 La Liga Forwards Analysis. Made with ❤️ using Python, Plotly & Bootstrap</small>
                    </p>
                </div>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Smooth scrolling for navbar links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});
        
        // Add loading animation for charts
        window.addEventListener('load', function() {{
            document.querySelectorAll('.chart-container').forEach(container => {{
                container.style.opacity = '0';
                container.style.transform = 'translateY(20px)';
                container.style.transition = 'all 0.6s ease';
                
                setTimeout(() => {{
                    container.style.opacity = '1';
                    container.style.transform = 'translateY(0)';
                }}, 200);
            }});
        }});
    </script>
</body>
</html>
"""
    
    return html_content

if __name__ == "__main__":
    # Create outputs directory if it doesn't exist
    os.makedirs('docs', exist_ok=True)
    
    # Generate HTML
    html_content = generate_html_page()
    
    # Save to docs/index.html (GitHub Pages looks for this)
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Static HTML generated successfully!")
    print("📁 File saved to: docs/index.html")
    print("🌐 Ready for GitHub Pages deployment!")
