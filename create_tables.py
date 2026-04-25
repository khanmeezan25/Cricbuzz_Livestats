from db_connection import connect_db

conn = connect_db()
cursor = conn.cursor()

# Matches Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY,
    team1 TEXT,
    team2 TEXT,
    status TEXT,
    venue TEXT
)
""")

# Players Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    runs INTEGER,
    wickets INTEGER,
    team TEXT
)
""")

conn.commit()
conn.close()

