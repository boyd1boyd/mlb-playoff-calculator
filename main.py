import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_standings(url):
    """
    Fetches the standings table from the specified URL.
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Locate the standings table. Update the selector based on the actual website.
    table = soup.find("table", {"class": "standings-table"})
    if not table:
        raise Exception("Standings table not found on the page.")
    
    # Parse the HTML table into a pandas DataFrame.
    df = pd.read_html(str(table))[0]
    return df

def process_standings(df):
    """
    Processes the standings DataFrame by converting columns and calculating max wins.
    Assumes df has columns: 'Team', 'Wins', 'Losses', and 'Remaining Games'
    """
    # Convert necessary columns to numeric types.
    df['Wins'] = pd.to_numeric(df['Wins'], errors='coerce')
    df['Remaining Games'] = pd.to_numeric(df['Remaining Games'], errors='coerce')
    
    # Calculate the maximum possible wins.
    df['Max_Wins'] = df['Wins'] + df['Remaining Games']
    
    # Sort teams by current wins (you could also sort by winning percentage if available).
    sorted_df = df.sort_values(by='Wins', ascending=False).reset_index(drop=True)
    return sorted_df

def calculate_top_teams(sorted_df):
    """
    Identifies the top 3 teams based on current wins and selects two wildcard teams.
    Note: This is a simplified approach. More complex tiebreakers may be required.
    """
    # Top 3 teams based on current wins.
    top_three = sorted_df.head(3)
    
    # For wildcards, assume the next 2 teams are potential wildcards.
    wildcards = sorted_df.iloc[3:5]  
    return top_three, wildcards

def main():
    # Replace this URL with the actual page where the standings are available.
    url = "https://www.example.com/mlb/standings"
    
    try:
        df = fetch_standings(url)
        print("Raw Standings Data:")
        print(df.head())
        
        sorted_df = process_standings(df)
        top_three, wildcards = calculate_top_teams(sorted_df)
        
        print("\nTop 3 Teams:")
        print(top_three[['Team', 'Wins', 'Max_Wins']])
        
        print("\nWildcard Teams:")
        print(wildcards[['Team', 'Wins', 'Max_Wins']])
        
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
