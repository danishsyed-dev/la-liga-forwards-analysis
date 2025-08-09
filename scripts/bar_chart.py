import matplotlib.pyplot as plt
import pandas as pd
import os

# Ensure outputs directory exists
os.makedirs('../outputs', exist_ok=True)

# Load scores data
try:
    scores_df = pd.read_csv('../outputs/player_scores.csv')
except FileNotFoundError:
    print("Player scores CSV not found. Please run players_scores.py first.")
    exit(1)

plt.figure(figsize=(10, 6))
plt.bar(scores_df['Player'], scores_df['Score'], color='teal')
plt.xlabel('Player')
plt.ylabel('Total Points')
plt.title('All-Time Greatest Forwards of La Liga')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('../outputs/player_scores_bar.png', dpi=300, bbox_inches='tight')
plt.show()
