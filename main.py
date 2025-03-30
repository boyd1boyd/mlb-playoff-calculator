import pandas as pd

def fetch_espn_standings():
    url = "https://www.espn.com/mlb/standings"
    
    try:
        dfs = pd.read_html(url)
        print(f"✅ Loaded {len(dfs)} tables from ESPN")

        division_names = ["AL East", "AL Central", "NL East", "NL Central"]
        all_dfs = []

        for df, division in zip(dfs[:4], division_names):
            df["Division"] = division
            all_dfs.append(df)

        combined_df = pd.concat(all_dfs, ignore_index=True)

        # Rename ESPN-style columns to standard names
        if "W" in combined_df.columns and "L" in combined_df.columns:
            combined_df.rename(columns={
                "W": "Wins",
                "L": "Losses",
                "PCT": "WinPct",
                "GB": "GamesBack"
            }, inplace=True)
        else:
            print("❌ Expected columns 'W' and 'L' not found.")
            return pd.DataFrame()

        combined_df["Remaining Games"] = 162 - (combined_df["Wins"] + combined_df["Losses"])
        return combined_df

    except Exception as e:
        print("❌ Error fetching standings:", e)
        return pd.DataFrame()

def main():
    standings = fetch_espn_standings()

    if standings.empty:
        print("🚫 No standings data available.")
        return

    print("✅ Live MLB Standings Preview:")
    print(standings[['Division', 'Team', 'Wins', 'Losses', 'Remaining Games']].head())

if __name__ == "__main__":
    main()
