"""
Bar chart visualization for player score comparison.
"""

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from typing import Optional


def create_bar_chart(
    scores_df: pd.DataFrame,
    output_path: Optional[Path] = None,
    show: bool = False,
    figsize: tuple = (10, 6),
    color: str = 'teal'
) -> plt.Figure:
    """
    Create a bar chart showing player scores.
    
    Args:
        scores_df: DataFrame with 'Player' and 'Score' columns
        output_path: Path to save the chart image (optional)
        show: Whether to display the chart
        figsize: Figure size as (width, height)
        color: Bar color
    
    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(scores_df['Player'], scores_df['Score'], color=color)
    ax.set_xlabel('Player')
    ax.set_ylabel('Total Points')
    ax.set_title("All-Time Greatest Forwards of La Liga")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    if output_path:
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    
    return fig


def main():
    """Run bar chart generation as a standalone script."""
    from pathlib import Path
    import sys
    
    # Add parent directories to path
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))
    
    outputs_dir = project_root / 'outputs'
    outputs_dir.mkdir(exist_ok=True)
    
    # Load scores data
    scores_path = outputs_dir / 'player_scores.csv'
    
    if not scores_path.exists():
        print("❌ Player scores CSV not found. Please run the scoring script first.")
        return
    
    scores_df = pd.read_csv(scores_path)
    
    output_path = outputs_dir / 'player_scores_bar.png'
    create_bar_chart(scores_df, output_path=output_path, show=True)
    print(f"✅ Bar chart saved to: {output_path}")


if __name__ == '__main__':
    main()
