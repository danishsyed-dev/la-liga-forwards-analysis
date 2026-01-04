"""
Radar chart visualization for multi-dimensional player comparison.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Any
from pathlib import Path


# Default color scheme for players
DEFAULT_COLORS: Dict[str, str] = {
    'Lionel Messi': '#FFD700',      # Gold
    'Cristiano Ronaldo': '#DC143C',  # Crimson
    'Luis Suárez': '#32CD32',        # Lime Green
    'Karim Benzema': '#00CED1',      # Dark Turquoise
    'Neymar Jr.': '#4B0082',         # Indigo
    'Gareth Bale': '#808080',        # Gray
    'Raúl González': '#FF00FF'       # Magenta
}


def extract_player_stats(players: Dict[str, Any]) -> pd.DataFrame:
    """
    Extract statistics from player data for radar chart.
    
    Args:
        players: Dictionary of player data
    
    Returns:
        DataFrame with player statistics
    """
    player_stats = []
    
    for player_name, data in players.items():
        stats = {}
        stats['Player'] = player_name
        stats['Career Goals'] = data.get('career_goals', 0)
        stats['La Liga Titles'] = data.get('total_la_liga_titles', 0)
        stats['Champions League Titles'] = data.get('total_champions_league_titles', 0)
        
        # Count Ballon d'Or Wins
        ballon_dor_wins = data.get('career_awards', []).count("Ballon d'Or Win")
        stats["Ballon d'Or Wins"] = ballon_dor_wins
        
        # Initialize counts
        golden_boots = 0
        seasons_20_goals = 0
        seasons_10_assists = 0
        cup_final_wins = 0
        cl_top_scorer = 0
        
        for season in data.get('seasons', []):
            # Check for La Liga Golden Boot awards
            if 'La Liga Golden Boot' in season.get('awards', []):
                golden_boots += 1
            
            # Check for seasons with 20+ goals
            if season.get('goals', 0) >= 20:
                seasons_20_goals += 1
            
            # Check for seasons with 10+ assists
            if season.get('assists', 0) >= 10:
                seasons_10_assists += 1
            
            # Check for cup final wins
            if season.get('cup_final_winner', False):
                cup_final_wins += 1
            
            # Check for CL Top Scorer awards
            cl_achievements = season.get('cl_achievements', [])
            cl_top_scorer += cl_achievements.count('CL Top Scorer')
        
        stats['La Liga Golden Boots'] = golden_boots
        stats['20+ Goal Seasons'] = seasons_20_goals
        stats['10+ Assist Seasons'] = seasons_10_assists
        stats['Cup Final Wins'] = cup_final_wins
        stats['CL Top Scorer Awards'] = cl_top_scorer
        
        player_stats.append(stats)
    
    return pd.DataFrame(player_stats)


def normalize_stats(stats_df: pd.DataFrame, metrics: List[str]) -> pd.DataFrame:
    """
    Normalize statistics for radar chart plotting.
    
    Args:
        stats_df: DataFrame with player statistics
        metrics: List of metric columns to normalize
    
    Returns:
        DataFrame with normalized values (0-1)
    """
    normalized_stats = stats_df.copy()
    
    for metric in metrics:
        max_value = normalized_stats[metric].max()
        min_value = normalized_stats[metric].min()
        
        # Avoid division by zero
        if max_value > min_value:
            normalized_stats[metric] = (normalized_stats[metric] - min_value) / (max_value - min_value)
        else:
            normalized_stats[metric] = 0
    
    return normalized_stats


def create_radar_chart(
    players: Dict[str, Any],
    output_path: Optional[Path] = None,
    show: bool = False,
    figsize: tuple = (12, 12),
    colors: Optional[Dict[str, str]] = None
) -> plt.Figure:
    """
    Create a radar chart comparing multiple players.
    
    Args:
        players: Dictionary of player data
        output_path: Path to save the chart image (optional)
        show: Whether to display the chart
        figsize: Figure size as (width, height)
        colors: Dictionary mapping player names to colors
    
    Returns:
        matplotlib Figure object
    """
    if colors is None:
        colors = DEFAULT_COLORS
    
    # Extract and prepare data
    stats_df = extract_player_stats(players)
    
    metrics = [
        'Career Goals', 'La Liga Titles', 'Champions League Titles',
        "Ballon d'Or Wins", 'La Liga Golden Boots', '20+ Goal Seasons',
        '10+ Assist Seasons', 'Cup Final Wins', 'CL Top Scorer Awards'
    ]
    
    normalized_stats = normalize_stats(stats_df, metrics)
    
    # Prepare angles for radar chart
    num_metrics = len(metrics)
    angles = np.linspace(0, 2 * np.pi, num_metrics, endpoint=False).tolist()
    angles += angles[:1]  # Close the plot
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(polar=True))
    
    # Plot each player
    for _, row in normalized_stats.iterrows():
        player_name = row['Player']
        values = row[metrics].tolist()
        values += values[:1]  # Close the plot
        
        color = colors.get(player_name, '#1f77b4')  # Default to blue
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=player_name, color=color)
        ax.fill(angles, values, alpha=0.1, color=color)
    
    # Customize chart
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics, size=10)
    ax.tick_params(axis='x', which='major', pad=15)
    ax.set_rlabel_position(0)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"], color="grey", size=8)
    ax.set_ylim(0, 1)
    
    # Add legend and title
    ax.set_title('Comparison of La Liga Forwards', size=18, y=1.05)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.15), fontsize=10)
    
    plt.tight_layout()
    
    if output_path:
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    
    return fig


def main():
    """Run radar chart generation as a standalone script."""
    import sys
    
    # Add parent directories to path
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root / 'src'))
    
    from core.players_data import players
    
    outputs_dir = project_root / 'outputs'
    outputs_dir.mkdir(exist_ok=True)
    
    output_path = outputs_dir / 'player_radar_chart.png'
    create_radar_chart(players, output_path=output_path, show=True)
    print(f"✅ Radar chart saved to: {output_path}")


if __name__ == '__main__':
    main()
