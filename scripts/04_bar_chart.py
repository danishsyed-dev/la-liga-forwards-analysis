import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.bar(scores_df['Player'], scores_df['Score'], color='teal')
plt.xlabel('Player')
plt.ylabel('Total Points')
plt.title('All-Time Greatest Forwards of La Liga')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
