import pandas as pd
import requests
from bs4 import BeautifulSoup

def fetch_espn_standings():
    url = "https://www.espn.com/mlb/standings"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    # All tables (one per division)
    tables = soup.find_all("table", class_="Table")

    all_dfs = []
    division_names = ["AL East", "AL Central", "AL West", "NL East", "NL Central", "NL West"]

    for table, division in zip(tables, division_names):
        df = pd.read_html(str(table))[0]
        df["Division"] = division
        all_dfs.append(df)

    combined_df = pd.concat(all_dfs)
    combined_df.reset_index(drop=True, inplace=True)

    # Standardize columns
    combined_df.rename(columns={
        "W": "Wins",
        "L": "Losses",
        "PCT": "WinPct",
        "GB": "GamesBack"
    }, inplace=True)

    # Calculate Remaining Games (assume 162-game season)
    combined_df["Remaining Games"] = 162 - (combined_df["Wins"] + combined_df["Losses"])
    
    return combined_df

def main():
    standings = fetch_espn_standings()
    print("✅ Scraped Live MLB Standings:")
    print(standings.head())

if __name__ == "__main__":
    main()
