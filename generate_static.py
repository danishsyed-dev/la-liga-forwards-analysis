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
    """Calculate scores for all players"""
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

def create_bar_chart(scores_df):
    """Create interactive bar chart"""
    fig = px.bar(
        scores_df, 
        x='Player', 
        y='Score',
        title="La Liga Greatest Forwards - Total Scores",
        color='Score',
        color_continuous_scale='viridis',
        height=600
    )
    fig.update_layout(
        xaxis_title="Player",
        yaxis_title="Total Points",
        font=dict(size=14),
        title_font_size=20
    )
    return fig

def create_radar_chart(stats_df):
    """Create radar chart for top 5 players"""
    # Select top 5 players
    top_players = stats_df.nlargest(5, 'Total Score')
    
    radar_metrics = ['Career Goals', 'La Liga Titles', 'Champions League Titles',
                    'Ballon d\'Or Wins', 'La Liga Golden Boots', '20+ Goal Seasons',
                    '10+ Assist Seasons', 'Cup Final Wins', 'CL Top Scorer Awards']
    
    # Normalize data for radar chart
    normalized_stats = top_players.copy()
    for metric in radar_metrics:
        max_val = stats_df[metric].max()
        min_val = stats_df[metric].min()
        if max_val > min_val:
            normalized_stats[metric] = (normalized_stats[metric] - min_val) / (max_val - min_val)
        else:
            normalized_stats[metric] = 0
    
    # Create radar chart
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
            opacity=0.1
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title="Top 5 La Liga Forwards - Radar Comparison",
        height=700,
        font=dict(size=14),
        title_font_size=20
    )
    
    return fig

def create_scatter_plot(stats_df):
    """Create scatter plot"""
    fig = px.scatter(
        stats_df,
        x='Career Goals',
        y='La Liga Titles',
        size='Champions League Titles',
        color='Ballon d\'Or Wins',
        hover_name='Player',
        title="Goals vs La Liga Titles (Size: CL Titles, Color: Ballon d'Or)",
        height=600
    )
    fig.update_layout(
        font=dict(size=14),
        title_font_size=20
    )
    return fig

def generate_html_page():
    """Generate the complete HTML page"""
    scores_df, stats_df = calculate_all_scores()
    
    # Create charts
    bar_chart = create_bar_chart(scores_df)
    radar_chart = create_radar_chart(stats_df)
    scatter_chart = create_scatter_plot(stats_df)
    
    # Convert charts to HTML
    bar_html = pyo.plot(bar_chart, output_type='div', include_plotlyjs=False)
    radar_html = pyo.plot(radar_chart, output_type='div', include_plotlyjs=False)
    scatter_html = pyo.plot(scatter_chart, output_type='div', include_plotlyjs=False)
    
    # Create stats table HTML
    stats_html = stats_df.to_html(classes='table table-striped table-hover', table_id='stats-table', index=False)
    
    # Generate complete HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚽ La Liga Greatest Forwards Analysis</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8f9fa;
        }}
        .hero {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 0;
            margin-bottom: 40px;
        }}
        .card {{
            border: none;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }}
        .navbar {{
            background-color: #2c3e50 !important;
        }}
        .btn-primary {{
            background-color: #667eea;
            border-color: #667eea;
        }}
        .btn-primary:hover {{
            background-color: #5a6fd8;
            border-color: #5a6fd8;
        }}
        #stats-table {{
            font-size: 0.9rem;
        }}
        .chart-container {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .footer {{
            background-color: #2c3e50;
            color: white;
            padding: 40px 0;
            margin-top: 50px;
        }}
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="#" style="font-size: 1.5rem; font-weight: bold;">⚽ La Liga Analysis</a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="#overview">Overview</a>
                <a class="nav-link" href="#charts">Charts</a>
                <a class="nav-link" href="#stats">Statistics</a>
            </div>
        </div>
    </nav>

    <div class="hero" id="overview">
        <div class="container text-center">
            <h1 class="display-4 fw-bold mb-4">⚽ La Liga Greatest Forwards Analysis</h1>
            <p class="lead mb-4">Comprehensive statistical analysis of the greatest forwards in La Liga history</p>
            <p>Using advanced scoring system based on goals, assists, titles, and individual achievements</p>
        </div>
    </div>

    <div class="container" id="charts">
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title mb-0">📊 Overall Rankings</h3>
                    </div>
                    <div class="card-body">
                        <div class="chart-container">
                            {bar_html}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title mb-0">🎯 Multi-Dimensional Comparison</h3>
                    </div>
                    <div class="card-body">
                        <div class="chart-container">
                            {radar_html}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title mb-0">📈 Goals vs Titles Analysis</h3>
                    </div>
                    <div class="card-body">
                        <div class="chart-container">
                            {scatter_html}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row" id="stats">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title mb-0">📋 Detailed Statistics</h3>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            {stats_html}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title mb-0">🏆 Scoring System</h3>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <h5>Individual Awards</h5>
                                <ul>
                                    <li>Ballon d'Or Win: <strong>5 points</strong></li>
                                    <li>La Liga Best Player: <strong>4 points</strong></li>
                                    <li>La Liga Golden Boot: <strong>3 points</strong></li>
                                    <li>CL Top Scorer: <strong>5 points</strong></li>
                                </ul>
                            </div>
                            <div class="col-md-6">
                                <h5>Team Achievements</h5>
                                <ul>
                                    <li>Champions League Win: <strong>5 points</strong></li>
                                    <li>La Liga Title: <strong>1 point</strong></li>
                                    <li>200+ La Liga Goals: <strong>5 points</strong></li>
                                    <li>20+ Goal Season: <strong>2 points</strong></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="footer">
        <div class="container text-center">
            <h5>⚽ La Liga Greatest Forwards Analysis</h5>
            <p>Data-driven analysis of La Liga's legendary forwards</p>
            <p>
                <a href="https://github.com/danishsyed-dev/la-liga-forwards-analysis" class="btn btn-primary">
                    View on GitHub
                </a>
            </p>
            <p class="mb-0">Built by Danish Syed | Data from La Liga Historical Records</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
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
