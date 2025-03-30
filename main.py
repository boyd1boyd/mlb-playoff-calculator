def main():
    df = fetch_mlb_standings()
    if df.empty:
        print("🚫 No data found.")
        return

    playoff_picture = get_playoff_picture(df)

    html_output = f"<h1>MLB Playoff Picture – {datetime.now().strftime('%Y-%m-%d %H:%M')}</h1>"

    for league, info in playoff_picture.items():
        html_output += f"<h2>{league}</h2>"
        html_output += "<h3>🏆 Division Winners</h3>"
        html_output += info['Division Winners'].to_html(index=False, border=1)

        html_output += "<h3>💥 Wildcard Teams</h3>"
        html_output += info['Wildcards'].to_html(index=False, border=1)

        html_output += "<h3>❓ Elimination Check</h3>"
        html_output += info['Standings'].to_html(index=False, border=1)

    # Save to docs/index.html
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html_output)

    print("✅ Webpage updated at docs/index.html")
