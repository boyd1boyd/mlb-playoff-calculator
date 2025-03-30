import pandas as pd

# Sample data simulating current standings
data = {
    'Team': ['Team A', 'Team B', 'Team C', 'Team D', 'Team E', 'Team F', 'Team G'],
    'Wins': [95, 92, 90, 88, 87, 85, 80],
    'Losses': [60, 63, 65, 67, 68, 70, 75],
    'Remaining Games': [7, 7, 7, 7, 7, 7, 7]
}

df = pd.DataFrame(data)
df['Max_Wins'] = df['Wins'] + df['Remaining Games']

# Sort by Wins
df = df.sort_values(by='Wins', ascending=False).reset_index(drop=True)

# Top 3 teams
top_3 = df.head(3)

# Wildcards (next best 2 teams)
wildcards = df.iloc[3:5]

# Playoff threshold: wildcard cutoff
wildcard_cutoff = wildcards['Wins'].min()

# Determine playoff eligibility
df['Still_Alive'] = df['Max_Wins'] >= wildcard_cutoff

print("🏆 Top 3 Teams:")
print(top_3[['Team', 'Wins', 'Max_Wins']])

print("\n💥 Wildcard Contenders:")
print(wildcards[['Team', 'Wins', 'Max_Wins']])

print("\n📊 Full Table with Playoff Eligibility:")
print(df[['Team', 'Wins', 'Max_Wins', 'Still_Alive']])
