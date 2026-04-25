from db_connection import connect_db
from api_fetch import get_live_matches, get_scorecard, parse_live_matches


# ===== Insert Matches into DB =====

def insert_matches():
    data = get_live_matches()

    conn = connect_db()
    cursor = conn.cursor()

    for match_type in data.get("typeMatches", []):
        for series in match_type.get("seriesMatches", []):
            wrapper = series.get("seriesAdWrapper")

            if wrapper:
                for m in wrapper.get("matches", []):
                    info = m.get("matchInfo", {})

                    cursor.execute("""
                    INSERT OR IGNORE INTO matches 
                    (match_id, team1, team2, status, venue)
                    VALUES (?, ?, ?, ?, ?)
                    """, (
                        info.get("matchId"),
                        info.get("team1", {}).get("teamName"),
                        info.get("team2", {}).get("teamName"),
                        info.get("status"),
                        info.get("venueInfo", {}).get("ground")
                    ))

    conn.commit()
    conn.close()
    print("Matches inserted ✅")


# ===== Insert Players (Batsmen + Bowlers) from Scorecard =====

def insert_players(match_id):
    """
    Given a match_id, fetches scorecard from API and inserts
    batting + bowling stats into the players table.
    """
    from api_fetch import get_scorecard

    data = get_scorecard(match_id)
    innings_list = data.get("scoreCard", [])

    conn = connect_db()
    cursor = conn.cursor()

    for innings in innings_list:
        bat_team = innings.get("batTeamDetails", {}).get("batTeamName", "Unknown")
        bowl_team = innings.get("bowlTeamDetails", {}).get("bowlTeamName", "Unknown")

        # ---------- Insert Batsmen ----------
        for _, bat in innings.get("batTeamDetails", {}).get("batsmenData", {}).items():
            name    = bat.get("batName", "Unknown")
            runs    = bat.get("runs", 0)
            team    = bat_team

            # Check if player already exists for this team; update runs if higher
            existing = cursor.execute(
                "SELECT player_id, runs FROM players WHERE name = ? AND team = ?",
                (name, team)
            ).fetchone()

            if existing:
                if runs > existing[1]:
                    cursor.execute(
                        "UPDATE players SET runs = ? WHERE player_id = ?",
                        (runs, existing[0])
                    )
            else:
                cursor.execute("""
                    INSERT INTO players (name, runs, wickets, team)
                    VALUES (?, ?, 0, ?)
                """, (name, runs, team))

        # ---------- Insert Bowlers ----------
        for _, bowl in innings.get("bowlTeamDetails", {}).get("bowlersData", {}).items():
            name    = bowl.get("bowlName", "Unknown")
            wickets = bowl.get("wickets", 0)
            team    = bowl_team

            existing = cursor.execute(
                "SELECT player_id, wickets FROM players WHERE name = ? AND team = ?",
                (name, team)
            ).fetchone()

            if existing:
                # Accumulate wickets across innings
                cursor.execute(
                    "UPDATE players SET wickets = wickets + ? WHERE player_id = ?",
                    (wickets, existing[0])
                )
            else:
                cursor.execute("""
                    INSERT INTO players (name, runs, wickets, team)
                    VALUES (?, 0, ?, ?)
                """, (name, wickets, team))

    conn.commit()
    conn.close()
    print(f"Players inserted for match {match_id} ✅")


# ===== Insert Players from ALL Live Matches =====

def insert_all_players():
    """
    Fetches all live/recent matches and inserts player data for each.
    """
    data = get_live_matches()
    matches = parse_live_matches(data)

    for match in matches:
        mid = match.get("match_id")
        if mid:
            try:
                insert_players(mid)
            except Exception as e:
                print(f"Skipping match {mid}: {e}")

    print("All players inserted ✅")


# ===== Run both if executed directly =====

if __name__ == "__main__":
    insert_matches()
    insert_all_players()