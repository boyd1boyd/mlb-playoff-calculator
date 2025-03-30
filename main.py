import requests
import pandas as pd

def fetch_mlb_standings():
    url = "https://statsapi.mlb.com/api/v1/standings?leagueId=103,104&season=2023&date=2023-10-01"
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
                'Remaining Games': 162 - (team_info['wins'] + team_info['losses'])
            }
            teams.append(team)

    df = pd.DataFrame(teams)
    return df

def main():
    df = fetch_mlb_standings()

    if df.empty:
        print("🚫 No data found.")
        return

    print("✅ Final 2023 MLB Standings via MLB API:")
    print(df[['League', 'Division', 'Team', 'Wins', 'Losses', 'WinPct', 'Remaining Games']].head(12))

if __name__ == "__main__":
    main()
