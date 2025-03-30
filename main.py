import pandas as pd

def fetch_espn_standings():
    url = "https://www.espn.com/mlb/standings"
    
    try:
        # Read all HTML tables on the page
        dfs = pd.read_html(url)
        print(f"✅ Loaded {len(dfs)} tables from ESPN")

        # ESPN returns division tables in this order
        division_names = ["AL East", "AL Central", "AL West", "NL East", "NL Central", "NL West"]
        
        # Use only the first 6 tables (one per division)
        all_dfs = []

        for df, division in zip(dfs[:6], division_names):
            df["Division"] = division
            all_dfs.append(df)

        combined_df = pd.concat(all_dfs)
        combined_df.reset_index(drop=True, inplace=True)

        # Rename columns for clarity
        combined_df.rename(columns={
            "W": "Wins",
            "L": "Losses",
            "PCT": "WinPct",
            "GB": "GamesBack"
        }, inplace=True)

        # Calculate Remaining Games (assume 162-game season)
        combined_df["Remaining Games"] = 162 - (combined_df["Wins"] + combined_df["Losses"])

        return combined_df
    
    except Exception as e:
        print("❌ Error fetching standings:", e)
        return pd.DataFrame()  # Return empty if there's an error

def main():
    standings = fetch_espn_standings()

    if standings.empty:
        print("🚫 No standings data available.")
        return

    print("✅ Live MLB Standings Preview:")
    print(standings[['Division', 'Team', 'Wins', 'Losses', 'Remaining Games']].head())

if __name__ == "__main__":
    main()
