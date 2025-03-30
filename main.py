import requests
import pandas as pd

def fetch_mlb_standings():
    url = "https://statsapi.mlb.com/api/v1/standings?leagueId=103,104&season=2024&standingsTypes=regularSeason"
    r = requests.get(url)
    data = r.json()

    teams = []

    for record in data['records']:
        division_info = record.get('division', {})
        league_info = record.get('league', {})

        division_name = division_info.get('name', 'Unknown Division')
        league_name = league_info.get('name', 'Unknown League')

        for team_info in record['teamRecords']:
            team = {
                'Team': team_info['team']['name'],
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

    print("✅ Live MLB Standings via MLB API:")
    print(df[['League', 'Division', 'Team', 'Wins', 'Losses', 'WinPct', 'Remaining Games']].head(12))

if __name__ == "__main__":
    main()
