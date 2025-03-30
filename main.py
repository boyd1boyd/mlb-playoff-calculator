import requests
import pandas as pd
from datetime import datetime

def fetch_mlb_standings():
    current_year = datetime.now().year
    url = f"https://statsapi.mlb.com/api/v1/standings?leagueId=103,104&season={current_year}"
    r = requests.get(url)
    data = r.json()

    division_order = [
        ("American League", "AL East"),
        ("American League", "AL Central"),
        ("American League", "AL West"),
        ("National League", "NL East"),
        ("National League", "NL Central"),
        ("National League", "NL West")
    ]

    teams = []

    for idx, record in enumerate(data['records']):
        if idx >= len(division_order):
            continue  # Defensive: skip if more divisions than expected

        league_name, division_name = division_order[idx]

        for team_info in record['teamRecords']:
            team_data = team_info['team']

            team = {
                'Team': team_data['name'],
                'League': league_name,
                'Division': division_name,
                'Wins': team_info['wins'],
                'Losses': team_info['losses'],
                'GamesBack': team_info.get('gamesBack', '0'),
                'WinPct': float(team_info['winningPercentage']),
            }

            team['Remaining Games'] = 162 - (team['Wins'] + team['Losses'])
            team['Max_Wins'] = team['Wins'] + team['Remaining Games']

            teams.append(team)

    df = pd.DataFrame(teams)
    return df

def get_playoff_picture(df):
    output = {}

    for league in ['American League', 'National League']:
        league_df = df[df['League'] == league].copy()  # Copy to avoid SettingWithCopyWarning

        # Get 1st place team in each division
        division_winners = (
            league_df.sort_values('Wins', ascending=False)
            .groupby('Division')
            .first()
        )
        division_winner_names = division_winners['Team'].tolist()

        # Next best 3 (wildcards)
        non_div_winners = league_df[~league_df['Team'].isin(division_winner_names)]
        wildcards = non_div_winners.sort_values('Wins', ascending=False).head(3)

        # Elimination check
        win_cutoff = wildcards['Wins'].min() if not wildcards.empty else 0
        league_df.loc[:, 'Still_Alive'] = league_df['Max_Wins'] >= win_cutoff

        output[league] = {
            'Division Winners': division_winners[['Team', 'Wins']],
            'Wildcards': wildcards[['Team', 'Wins']],
            'Standings': league_df[['Team', 'Wins', 'Max_Wins', 'Still_Alive']]
                          .sort_values('Wins', ascending=False)
        }

    return output

def main():
    df = fetch_mlb_standings()
    if df.empty:
        print("🚫 No data found.")
        return

    print(f"✅ MLB Standings for {datetime.now().year}:\n")

    playoff_picture = get_playoff_picture(df)

    for league, info in playoff_picture.items():
        print(f"\n=== {league} ===")
        print("\n🏆 Division Winners:")
        print(info['Division Winners'].to_string(index=False))

        print("\n💥 Wildcard Teams:")
        print(info['Wildcards'].to_string(index=False))

        print("\n❓ Elimination Check:")
        print(info['Standings'].to_string(index=False))

if __name__ == "__main__":
    main()
