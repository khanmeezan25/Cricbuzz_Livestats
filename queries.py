# 1. ----- All matches ----- 

def get_all_matches(conn):
    return conn.execute("SELECT * FROM matches").fetchall()

# 2. -----  Match by ID ----- 

def get_match_by_id(conn, match_id):
    return conn.execute(
        "SELECT * FROM matches WHERE match_id = ?", 
        (match_id,)
    ).fetchone()

# 3. -----  Matches by team ----- 

def get_matches_by_team(conn, team):
    return conn.execute("""
    SELECT * FROM matches 
    WHERE team1 = ? OR team2 = ?
    """, (team, team)).fetchall()

# 4. -----  Recent matches  ----- 

def recent_matches(conn):
    return conn.execute("""
    SELECT * FROM matches 
    ORDER BY match_id DESC 
    LIMIT 5
    """).fetchall()

# 5. -----  Matches at specific venue ----- 

def matches_by_venue(conn, venue):
    return conn.execute("""
    SELECT * FROM matches 
    WHERE venue = ?
    """, (venue,)).fetchall()

# 6. -----  Count total matches ----- 

def total_matches(conn):
    return conn.execute("""
    SELECT COUNT(*) FROM matches
    """).fetchone()

# 7. -----  Distinct teams ----- 

def distinct_teams(conn):
    return conn.execute("""
    SELECT DISTINCT team1 FROM matches
    """).fetchall()

# 8. -----  Match status filter ----- 

def matches_by_status(conn, status):
    return conn.execute("""
    SELECT * FROM matches 
    WHERE status LIKE ?
    """, ('%' + status + '%',)).fetchall()

# 9. -----  Matches per team ----- 

def matches_per_team(conn):
    return conn.execute("""
    SELECT team1, COUNT(*) 
    FROM matches 
    GROUP BY team1
    """).fetchall()

# 10. -----  Most active teams ----- 

def top_teams(conn):
    return conn.execute("""
    SELECT team1, COUNT(*) as total
    FROM matches
    GROUP BY team1
    ORDER BY total DESC
    LIMIT 5
    """).fetchall()

# 11. -----  Venue match count ----- 

def matches_per_venue(conn):
    return conn.execute("""
    SELECT venue, COUNT(*) 
    FROM matches 
    GROUP BY venue
    ORDER BY COUNT(*) DESC
    """).fetchall()

# 12. -----  Player total runs ----- 

def total_runs_by_player(conn):
    return conn.execute("""
    SELECT name, SUM(runs)
    FROM players
    GROUP BY name
    """).fetchall()

# 13. -----  Player total wickets ----- 

def total_wickets_by_player(conn):
    return conn.execute("""
    SELECT name, SUM(wickets)
    FROM players
    GROUP BY name
    """).fetchall()

# 14. -----  Top run scorers ----- 

def top_run_scorers(conn):
    return conn.execute("""
    SELECT name, runs 
    FROM players
    ORDER BY runs DESC
    LIMIT 10
    """).fetchall()

# 15. -----  Top wicket takers ----- 

def top_wicket_takers(conn):
    return conn.execute("""
    SELECT name, wickets
    FROM players
    ORDER BY wickets DESC
    LIMIT 10
    """).fetchall()

# 16. -----  Team-wise players ----- 

def team_wise_players(conn):
    return conn.execute("""
    SELECT team, COUNT(*) 
    FROM players
    GROUP BY team
    """).fetchall()

# 17. -----  Players with above average runs ----- 

def above_avg_players(conn):
    return conn.execute("""
    SELECT name, runs 
    FROM players
    WHERE runs > (SELECT AVG(runs) FROM players)
    """).fetchall()

# 18. -----  Highest run scorer ----- 

def highest_run_scorer(conn):
    return conn.execute("""
    SELECT name, MAX(runs) FROM players
    """).fetchone()

# 19. -----  Highest wicket taker ----- 

def highest_wicket_taker(conn):
    return conn.execute("""
    SELECT name, MAX(wickets) FROM players
    """).fetchone()

# 20. -----  Rank players by runs (WINDOW FUNCTION) ----- 

def rank_players(conn):
    return conn.execute("""
    SELECT name, runs,
    RANK() OVER (ORDER BY runs DESC) as rank
    FROM players
    """).fetchall()

# 21. -----  Matches with same venue count > 1 ----- 

def repeated_venues(conn):
    return conn.execute("""
    SELECT venue, COUNT(*) 
    FROM matches
    GROUP BY venue
    HAVING COUNT(*) > 1
    """).fetchall()

# 22. -----  Players with zero wickets ----- 

def zero_wickets(conn):
    return conn.execute("""
    SELECT name FROM players
    WHERE wickets = 0
    """).fetchall()

# 23. -----  Teams appearing in both columns ----- 

def all_teams(conn):
    return conn.execute("""
    SELECT team1 FROM matches
    UNION
    SELECT team2 FROM matches
    """).fetchall()

# 24. -----  Matches count using subquery ----- 

def match_count_subquery(conn):
    return conn.execute("""
    SELECT * FROM matches
    WHERE match_id IN (
        SELECT match_id FROM matches LIMIT 5
    )
    """).fetchall()

# 25. -----  Running total of runs ----- 

def running_total_runs(conn):
    return conn.execute("""
    SELECT name, runs,
    SUM(runs) OVER (ORDER BY runs) as cumulative_runs
    FROM players
    """).fetchall()