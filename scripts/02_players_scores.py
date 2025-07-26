player_scores = {}
for player_name, data in players.items():
    score = calculate_player_score(data, points_system)
    player_scores[player_name] = score

# Create DataFrame
scores_df = pd.DataFrame(list(player_scores.items()), columns=['Player', 'Score'])
scores_df.sort_values(by='Score', ascending=False, inplace=True)

# Display the updated rankings
print(scores_df)
