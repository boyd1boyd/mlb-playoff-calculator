import requests
import pandas as pd
import json

def fetch_mlb_standings():
    url = "https://statsapi.mlb.com/api/v1/standings?leagueId=103,104&season=2024&standingsTypes=regularSeason"
    r = requests.get(url)
    data = r.json()

    # Print 1 team record to inspect structure
    sample = data['records'][0]['teamRecords'][0]
    print("🔍 Sample team record:\n")
    print(json.dumps(sample, indent=2))
    return pd.DataFrame()  # Just stop here for now

def main():
    df = fetch_mlb_standings()

    if df.empty:
        print("🚫 No data yet. Debug mode.")
        return

if __name__ == "__main__":
    main()
