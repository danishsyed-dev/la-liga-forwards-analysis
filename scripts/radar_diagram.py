# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Your existing players dictionary (include the code you provided)
players = {
    'Lionel Messi': {
        'career_goals': 474,
        'seasons': [
            {
                'season': '2011/2012',
                'goals': 50,
                'assists': 15,
                'awards': [
                    'Ballon d\'Or Win',
                    'La Liga Best Player Award',
                    'La Liga Golden Boot',
                    'Most Assists in La Liga Season'
                ],
                'team_achievements': ['La Liga Title', 'Copa del Rey'],
                'cup_final_winner': True,
                'cl_achievements': [
                    'CL Top Scorer',
                    'Most Assists in CL Season'
                ]
            },
            {
                'season': '2014/2015',
                'goals': 43,
                'assists': 18,
                'awards': [
                    'Ballon d\'Or 2nd Place',
                    'La Liga Best Player Award',
                    'Most Assists in La Liga Season'
                ],
                'team_achievements': ['La Liga Title', 'Champions League Win', 'Copa del Rey'],
                'cup_final_winner': True,
                'cl_achievements': [
                    'CL Top Scorer',
                    'Most Assists in CL Season'
                ]
            },
            {
                'season': '2012/2013',
                'goals': 46,
                'assists': 12,
                'awards': [
                    'Ballon d\'Or Win',
                    'La Liga Best Player Award',
                    'La Liga Golden Boot'
                ],
                'team_achievements': ['La Liga Title'],
                'cup_final_winner': False,
                'cl_achievements': []
            }
        ],
        'career_awards': ['Ballon d\'Or Win'] * 6,  # 6 Ballon d'Or wins during his La Liga career
        'total_la_liga_titles': 10,
        'total_champions_league_titles': 4
    },
    'Cristiano Ronaldo': {
        'career_goals': 311,
        'seasons': [
            {
                'season': '2011/2012',
                'goals': 46,
                'assists': 12,
                'awards': [
                    'Ballon d\'Or 2nd Place',
                    'La Liga Best Player Award'
                ],
                'team_achievements': ['La Liga Title'],
                'cup_final_winner': False,
                'cl_achievements': ['CL Top Scorer']
            },
            {
                'season': '2014/2015',
                'goals': 48,
                'assists': 16,
                'awards': [
                    'Ballon d\'Or 2nd Place',
                    'La Liga Best Player Award',
                    'La Liga Golden Boot',
                    'Most Assists in La Liga Season'
                ],
                'team_achievements': ['UEFA Super Cup', 'FIFA Club World Cup'],
                'cup_final_winner': False,
                'cl_achievements': ['CL Top Scorer']
            },
            {
                'season': '2010/2011',
                'goals': 40,
                'assists': 10,
                'awards': [
                    'Ballon d\'Or 2nd Place',
                    'La Liga Golden Boot'
                ],
                'team_achievements': ['Copa del Rey'],
                'cup_final_winner': True,  # Scored the winning goal
                'cl_achievements': ['CL Top Scorer']
            }
        ],
        'career_awards': ['Ballon d\'Or Win'] * 4,
        'total_la_liga_titles': 2,
        'total_champions_league_titles': 4
    },
    'Luis Suárez': {
        'career_goals': 147,
        'seasons': [
            {
                'season': '2015/2016',
                'goals': 40,
                'assists': 16,
                'awards': [
                    'La Liga Golden Boot',
                    'Most Assists in La Liga Season'
                ],
                'team_achievements': ['La Liga Title', 'Copa del Rey'],
                'cup_final_winner': True,
                'cl_achievements': []
            },
            {
                'season': '2016/2017',
                'goals': 29,
                'assists': 13,
                'awards': [
                    '10+ Assist La Liga Season'
                ],
                'team_achievements': ['Copa del Rey'],
                'cup_final_winner': True,
                'cl_achievements': []
            },
            {
                'season': '2017/2018',
                'goals': 25,
                'assists': 12,
                'awards': [
                    '10+ Assist La Liga Season'
                ],
                'team_achievements': ['La Liga Title', 'Copa del Rey'],
                'cup_final_winner': True,
                'cl_achievements': []
            }
        ],
        'career_awards': [],
        'total_la_liga_titles': 4,
        'total_champions_league_titles': 1
    },
    'Karim Benzema': {
        'career_goals': 238,
        'seasons': [
            {
                'season': '2021/2022',
                'goals': 27,
                'assists': 12,
                'awards': [
                    'Ballon d\'Or Win',
                    'La Liga Best Player Award',
                    'La Liga Golden Boot',
                    'Most Assists in La Liga Season'
                ],
                'team_achievements': ['La Liga Title', 'Champions League Win', 'Supercopa de España'],
                'cup_final_winner': True,
                'cl_achievements': [
                    'CL Top Scorer',
                    'Most Assists in CL Season'
                ]
            },
            {
                'season': '2015/2016',
                'goals': 24,
                'assists': 7,
                'awards': [],
                'team_achievements': ['Champions League Win'],
                'cup_final_winner': False,
                'cl_achievements': []
            },
            {
                'season': '2018/2019',
                'goals': 21,
                'assists': 6,
                'awards': [],
                'team_achievements': [],
                'cup_final_winner': False,
                'cl_achievements': []
            }
        ],
        'career_awards': ['Ballon d\'Or Win'],
        'total_la_liga_titles': 4,
        'total_champions_league_titles': 5
    },
    'Neymar Jr.': {
        'career_goals': 68,
        'seasons': [
            {
                'season': '2015/2016',
                'goals': 24,
                'assists': 12,
                'awards': [],
                'team_achievements': ['La Liga Title', 'Copa del Rey'],
                'cup_final_winner': True,
                'cl_achievements': []
            },
            {
                'season': '2014/2015',
                'goals': 22,
                'assists': 7,
                'awards': [],
                'team_achievements': ['La Liga Title', 'Champions League Win', 'Copa del Rey'],
                'cup_final_winner': True,
                'cl_achievements': []
            },
            {
                'season': '2016/2017',
                'goals': 13,
                'assists': 11,
                'awards': ['Most Assists in La Liga Season'],
                'team_achievements': ['Copa del Rey'],
                'cup_final_winner': True,
                'cl_achievements': []
            }
        ],
        'career_awards': [],
        'total_la_liga_titles': 2,
        'total_champions_league_titles': 1
    },
    'Gareth Bale': {
        'career_goals': 81,
        'seasons': [
            {
                'season': '2013/2014',
                'goals': 15,
                'assists': 12,
                'awards': ['La Liga Breakthrough Player'],
                'team_achievements': ['Champions League Win', 'Copa del Rey'],
                'cup_final_winner': True,
                'cl_achievements': []
            },
            {
                'season': '2015/2016',
                'goals': 19,
                'assists': 10,
                'awards': [],
                'team_achievements': ['Champions League Win'],
                'cup_final_winner': False,
                'cl_achievements': []
            },
            {
                'season': '2017/2018',
                'goals': 16,
                'assists': 2,
                'awards': [],
                'team_achievements': ['Champions League Win'],
                'cup_final_winner': True,  # Scored in UCL final
                'cl_achievements': []
            }
        ],
        'career_awards': [],
        'total_la_liga_titles': 3,
        'total_champions_league_titles': 5
    },
    'Raúl González': {
        'career_goals': 228,
        'seasons': [
            {
                'season': '1998/1999',
                'goals': 25,
                'assists': 5,
                'awards': ['La Liga Golden Boot'],
                'team_achievements': [],
                'cup_final_winner': False,
                'cl_achievements': []
            },
            {
                'season': '2000/2001',
                'goals': 24,
                'assists': 6,
                'awards': ['Ballon d\'Or 2nd Place'],
                'team_achievements': ['La Liga Title'],
                'cup_final_winner': False,
                'cl_achievements': ['CL Top Scorer']
            },
            {
                'season': '1999/2000',
                'goals': 17,
                'assists': 9,
                'awards': [],
                'team_achievements': ['Champions League Win'],
                'cup_final_winner': False,
                'cl_achievements': ['CL Top Scorer']
            }
        ],
        'career_awards': [],
        'total_la_liga_titles': 6,
        'total_champions_league_titles': 3
    }
}

# Initialize a list to store player stats
player_stats = []

# Loop through each player and extract stats
for player_name, data in players.items():
    stats = {}
    stats['Player'] = player_name
    stats['Career Goals'] = data.get('career_goals', 0)
    stats['La Liga Titles'] = data.get('total_la_liga_titles', 0)
    stats['Champions League Titles'] = data.get('total_champions_league_titles', 0)
    
    # Count Ballon d'Or Wins
    ballon_dor_wins = data.get('career_awards', []).count('Ballon d\'Or Win')
    stats['Ballon d\'Or Wins'] = ballon_dor_wins
    
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

# Create a DataFrame from the list
stats_df = pd.DataFrame(player_stats)

# Copy the DataFrame for normalization
normalized_stats = stats_df.copy()

# List of metrics to normalize
metrics = ['Career Goals', 'La Liga Titles', 'Champions League Titles',
           'Ballon d\'Or Wins', 'La Liga Golden Boots', '20+ Goal Seasons',
           '10+ Assist Seasons', 'Cup Final Wins', 'CL Top Scorer Awards']

# Normalize each metric
for metric in metrics:
    max_value = normalized_stats[metric].max()
    min_value = normalized_stats[metric].min()
    # Avoid division by zero
    if max_value > min_value:
        normalized_stats[metric] = (normalized_stats[metric] - min_value) / (max_value - min_value)
    else:
        normalized_stats[metric] = 0

# Prepare data for the radar chart
categories = metrics
N = len(categories)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]  # Close the plot

# Initialize the radar chart
plt.figure(figsize=(12, 12))
ax = plt.subplot(111, polar=True)

colors = {
    'Lionel Messi': 'yellow',
    'Cristiano Ronaldo': 'red',
    'Luis Suárez': 'green',
    'Karim Benzema': 'cyan',
    'Neymar Jr.': 'indigo',
    'Gareth Bale': 'grey',
    'Raúl González': 'magenta'
}

# Plot each player's stats
for idx, row in normalized_stats.iterrows():
    values = row[metrics].tolist()
    values += values[:1]  # Close the plot
    ax.plot(angles, values, linewidth=2, linestyle='solid', label=row['Player'], color=colors[row['Player']])
    ax.fill(angles, values, alpha=0.1, color=colors[row['Player']])

# Customize the chart
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
plt.xticks(angles[:-1], categories, size=12)
ax.tick_params(axis='x', which='major', pad=15)
ax.set_rlabel_position(0)
plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0], labels=["0.2","0.4","0.6","0.8", "1.0"], color="grey", size=10)
plt.ylim(0, 1)

# Add legend and title
plt.title('Comparison of La Liga Forwards', size=18, y=1.05)
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.15), fontsize=12)
plt.show()
