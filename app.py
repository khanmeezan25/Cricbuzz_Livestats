import streamlit as st
import pandas as pd

# ================ PAGE CONFIG ================
st.set_page_config(page_title="Cricbuzz LiveStats", layout="wide")
 
# ============ HEADER =============
st.markdown("<style>.block-container {padding-top: 1rem;}</style>", unsafe_allow_html=True) 
st.markdown("""
    <div style="display:flex; align-items:center; justify-content:center; gap:10px;">
        <img src="https://img.icons8.com/color/96/cricket.png" width="65">
        <h1 style="color: green; font-size: 60px; margin:0;">
            Cricbuzz LiveStats
        </h1>
    </div>
""", unsafe_allow_html=True)


# ================ BACKGROUND COLOR ================
st.markdown("""
    <style>
        .stApp {
            background-color: #F0FFF0;
        }
        header[data-testid="stHeader"] {
            background-color: #F0FFF0;
        }
        div[data-testid="stToolbar"] {
            background-color: #F0FFF0;
        }
        section[data-testid="stSidebar"] {
            background-color: #e0f2e9;
        }
    </style>
""", unsafe_allow_html=True)


# ========== SIDEBAR ==========

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            background-color: #0e1117;
        }

        section[data-testid="stSidebar"] * {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)


st.sidebar.markdown("""
    <h2 style='text-align: center; margin-top: 0px; color:white;'>
        ㊂ Menu
    </h2>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        div[role="radiogroup"] > label {
            margin-bottom: 70px;
        }

        div[role="radiogroup"] label span {
            font-size: 25px;
        }

        section[data-testid="stSidebar"] hr {
            border: 1px solid white
        }                        
    </style>
""", unsafe_allow_html=True)


page = st.sidebar.radio(
    "------------",
    ["📡 Live Match", "🏆 Top Player Stats", "📊 SQL Analytics", "🛠 CRUD Operations", "🏠 Home"]
)

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Cricbuzz LiveStats")



# ==============================================================
# PAGE 5 — HOME
# ==============================================================

if page == "🏠 Home":
    st.title("🏏 Cricbuzz LiveStats Dashboard")
    st.divider()

    st.markdown("""
    Welcome to **Cricbuzz LiveStats** — a full-stack cricket analytics project that combines
    live API data, SQL databases, and an interactive dashboard into one powerful application.
    """)

    st.divider()

    # --- Tools Used ---
    st.subheader("🛠️ Tools & Technologies Used")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🐍 **Python**\nBackend logic, API calls, data parsing")
    with col2:
        st.info("🗄️ **SQLite**\nStructured data storage & SQL analytics")
    with col3:
        st.info("📊 **Streamlit**\nInteractive web dashboard")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.info("🌐 **Cricbuzz API**\nReal-time cricket data via RapidAPI")
    with col5:
        st.info("🐼 **Pandas**\nData manipulation & table display")
    with col6:
        st.info("📈 **Plotly / Charts**\nVisualizations & graphs")

    st.divider()

    # --- Project Workflow ---
    st.subheader("⚙️ Project Workflow")
    steps = {
        "Step 1️⃣ — Fetch API Data": "Connect to Cricbuzz via RapidAPI. Get live scores, player stats, match info.",
        "Step 2️⃣ — Store in SQLite DB": "Parse API response and insert into `matches` and `players` tables.",
        "Step 3️⃣ — SQL Analytics": "Run 25 SQL queries from beginner to advanced (Window Functions, CTEs, Subqueries).",
        "Step 4️⃣ — Streamlit Dashboard": "Visualize everything: live scores, player rankings, analytics results.",
        "Step 5️⃣ — CRUD Operations": "Manually add, update, delete, and view records in the database.",
    }
    for title, desc in steps.items():
        with st.expander(title):
            st.write(desc)

    st.divider()

        # --- Navigation Buttons ---
    st.subheader("🚀 Quick Navigation")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("📡 Live Match", use_container_width=True):
            st.session_state["page"] = "📡 Live Match"
            st.rerun()
    with c2:
        if st.button("🏆 Top Player Stats", use_container_width=True):
            st.session_state["page"] = "🏆 Top Player Stats"
            st.rerun()
    with c3:
        if st.button("📊 SQL Analytics", use_container_width=True):
            st.session_state["page"] = "📊 SQL Analytics"
            st.rerun()
    with c4:
        if st.button("🛠 CRUD Operations", use_container_width=True):
            st.session_state["page"] = "🛠 CRUD Operations"
            st.rerun()

    st.divider()
    st.success("👈 Use the sidebar to navigate between pages!")

# ==============================================================
# PAGE 1 — LIVE MATCH
# ==============================================================

elif page == "📡 Live Match":

    from api_fetch import get_live_matches, get_recent_matches, get_scorecard

    def _parse_matches(data):
        live, completed = [], []
        for match_type in data.get("typeMatches", []):
            for series in match_type.get("seriesMatches", []):
                wrapper = series.get("seriesAdWrapper")
                if wrapper:
                    for m in wrapper.get("matches", []):
                        info = m.get("matchInfo", {})
                        match_score = m.get("matchScore", {})
                        match_id = info.get("matchId")
                        team1 = info.get("team1", {}).get("teamName", "TBA")
                        team2 = info.get("team2", {}).get("teamName", "TBA")
                        state = info.get("state", "").lower()
                        status = info.get("status", "").lower()
                        match_entry = {
                            "id": match_id,
                            "name": f"{team1} vs {team2}",
                            "info": info,
                            "matchScore": match_score
                        }
                        if ("complete" in state or "won" in status or
                                "draw" in status or "tied" in status or
                                "abandoned" in status or "no result" in status):
                            completed.append(match_entry)
                        else:
                            live.append(match_entry)
        return live, completed

    st.title("📡 Live Match Page")
    st.caption("Select a match to view live scores and detailed player stats")
    st.divider()

    if st.button("🔄 Refresh Matches", use_container_width=False):
        st.session_state["live_data"] = get_live_matches()
        st.session_state.pop("recent_data", None)
        st.toast("Matches refreshed!", icon="✅")

    if "live_data" not in st.session_state:
        with st.spinner("Fetching live matches..."):
            st.session_state["live_data"] = get_live_matches()

    live_matches, completed_matches = _parse_matches(st.session_state["live_data"])

    # Agar live API se kuch nahi aaya to recent API call karo
    if not live_matches and not completed_matches:
        if "recent_data" not in st.session_state:
            with st.spinner("Koi live match nahi... Recent matches fetch ho rahe hain..."):
                st.session_state["recent_data"] = get_recent_matches()
        _, completed_matches = _parse_matches(st.session_state["recent_data"])

    selected_data = None

    if live_matches:
        st.subheader("🔴 Live Matches")
        live_names = [m["name"] for m in live_matches]
        selected_live = st.selectbox("Select a live match", live_names, key="live_select")
        selected_data = next(m for m in live_matches if m["name"] == selected_live)
    elif completed_matches:
        st.info("🏏 Abhi koi live match nahi chal raha — yahan recent matches hain:")
        st.divider()
        st.subheader("🕐 Recent / Completed Matches")
        completed_names = [m["name"] for m in completed_matches]
        selected_completed = st.selectbox("Match select karo scorecard dekhne ke liye", completed_names, key="completed_select")
        selected_data = next(m for m in completed_matches if m["name"] == selected_completed)
    else:
        st.warning("⚠️ Koi bhi match nahi mila. Thodi der baad Refresh karein.")
        st.stop()

    if selected_data is None:
        st.stop()

    info = selected_data["info"]
    match_id = selected_data["id"]
    match_score = selected_data["matchScore"]
    team1_name = info.get("team1", {}).get("teamName", "Team 1")
    team2_name = info.get("team2", {}).get("teamName", "Team 2")
    status_text = info.get("status", "N/A")
    venue_text = info.get("venueInfo", {}).get("ground", "N/A")
    series_text = info.get("seriesName", "N/A")

    st.divider()
    st.subheader("🏟️ Match Details")

    st.markdown("""
        <style>
            [data-testid="stMetricLabel"] p {
                font-size: 15px !important;
                color: #555;
            }
            [data-testid="stMetricValue"] {
                font-size: 22px !important;
                white-space: normal !important;
                word-break: break-word !important;
                line-height: 1.3 !important;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Team 1", team1_name)
    with col2:
        st.metric("Team 2", team2_name)
    with col3:
        st.metric("Status", status_text)

    col_v, col_s = st.columns(2)
    with col_v:
        st.info(f"📍 **Venue:** {venue_text}")
    with col_s:
        st.info(f"🏆 **Series:** {series_text}")

    st.divider()
    st.subheader("🏏 Live Score")

    team1_score_data = match_score.get("team1Score", {})
    team2_score_data = match_score.get("team2Score", {})

    score_found = False
    for inn_key in ["inngs1", "inngs2"]:
        t1 = team1_score_data.get(inn_key)
        t2 = team2_score_data.get(inn_key)
        if t1 or t2:
            score_found = True
            col_t1, col_t2 = st.columns(2)
            if t1:
                with col_t1:
                    st.metric(f"🏏 {team1_name}", f"{t1.get('runs', 0)}/{t1.get('wickets', '-')}", delta=f"{t1.get('overs', 0)} overs")
            if t2:
                with col_t2:
                    st.metric(f"🏏 {team2_name}", f"{t2.get('runs', 0)}/{t2.get('wickets', '-')}", delta=f"{t2.get('overs', 0)} overs")

    if not score_found:
        st.info("Score not available yet.")

    st.divider()

    with st.spinner("Loading scorecard..."):
        scorecard_data = get_scorecard(match_id)
    innings_data = scorecard_data.get("scoreCard", scorecard_data.get("scorecard", []))

    if not innings_data:
        st.warning("⚠️ Scorecard not available yet for this match.")
    else:
        def get_bat_bowl_labels(innings_id):
            if innings_id % 2 == 1:
                return team1_name, team2_name
            else:
                return team2_name, team1_name

        st.subheader("🏏 Batting Stats")
        for innings in innings_data:
            innings_id = innings.get("inningsid", 1)
            bat_label, bowl_label = get_bat_bowl_labels(innings_id)
            batsmen = innings.get("batsman", [])
            if batsmen:
                with st.expander(f"📋 Innings {innings_id} — {bat_label} Batting", expanded=True):
                    rows = [{
                        "Name": b.get("name", "-"), "Runs": b.get("runs", 0),
                        "Balls": b.get("balls", 0), "4s": b.get("fours", 0),
                        "6s": b.get("sixes", 0), "SR": b.get("strkrate", 0),
                        "Dismissal": b.get("outdec", "batting")
                    } for b in batsmen]
                    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("🎯 Bowling Stats")
        for innings in innings_data:
            innings_id = innings.get("inningsid", 1)
            bat_label, bowl_label = get_bat_bowl_labels(innings_id)
            bowlers = innings.get("bowler", [])
            if bowlers:
                with st.expander(f"📋 Innings {innings_id} — {bowl_label} Bowling", expanded=True):
                    rows = [{
                        "Name": b.get("name", "-"), "Overs": b.get("overs", 0),
                        "Runs": b.get("runs", 0), "Wickets": b.get("wickets", 0),
                        "Economy": b.get("econrate", 0), "Maidens": b.get("maidens", 0)
                    } for b in bowlers]
                    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ==============================================================
# PAGE 2 — TOP PLAYER STATS
# ==============================================================

elif page == "🏆 Top Player Stats":
    from db_connection import connect_db

    st.title("🏆 Top Player Stats")
    st.caption("Rankings based on data stored in the local SQLite database")
    st.divider()

    # Option to sync DB from latest API data
    if st.button("🔄 Sync Latest Data from API", use_container_width=False):
        with st.spinner("Fetching and inserting data..."):
            from insert_data import insert_matches, insert_all_players
            insert_matches()
            insert_all_players()
        st.success("Database updated! ✅")

    conn = connect_db()

    # ---------- Top Run Scorers ----------
    st.subheader("🏏 Top Run Scorers")
    run_data = conn.execute("""
        SELECT name, team, runs 
        FROM players 
        ORDER BY runs DESC 
        LIMIT 10
    """).fetchall()

    if run_data:
        df_runs = pd.DataFrame(run_data, columns=["Player", "Team", "Runs"])
        df_runs.index = df_runs.index + 1
        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(df_runs, use_container_width=True)
        with col2:
            st.bar_chart(df_runs.set_index("Player")["Runs"])
    else:
        st.info("No player data yet. Click 'Sync Latest Data' above.")

    st.divider()

    # ---------- Top Wicket Takers ----------
    st.subheader("🎯 Top Wicket Takers")
    wkt_data = conn.execute("""
        SELECT name, team, wickets 
        FROM players 
        ORDER BY wickets DESC 
        LIMIT 10
    """).fetchall()

    if wkt_data:
        df_wkt = pd.DataFrame(wkt_data, columns=["Player", "Team", "Wickets"])
        df_wkt.index = df_wkt.index + 1
        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(df_wkt, use_container_width=True)
        with col2:
            st.bar_chart(df_wkt.set_index("Player")["Wickets"])
    else:
        st.info("No wicket data yet.")

    st.divider()

    # ---------- All Rounders (Runs + Wickets both > 0) ----------
    st.subheader("⭐ All Rounders (Runs + Wickets both > 0)")
    ar_data = conn.execute("""
        SELECT name, team, runs, wickets
        FROM players
        WHERE runs > 0 AND wickets > 0
        ORDER BY runs DESC
        LIMIT 10
    """).fetchall()

    if ar_data:
        df_ar = pd.DataFrame(ar_data, columns=["Player", "Team", "Runs", "Wickets"])
        df_ar.index = df_ar.index + 1
        st.dataframe(df_ar, use_container_width=True)
    else:
        st.info("No all-rounder data yet.")

    st.divider()

    # ---------- Team-wise Player Count ----------
    st.subheader("🌍 Team-wise Player Count")
    team_data = conn.execute("""
        SELECT team, COUNT(*) as total_players
        FROM players
        GROUP BY team
        ORDER BY total_players DESC
    """).fetchall()

    if team_data:
        df_team = pd.DataFrame(team_data, columns=["Team", "Total Players"])
        df_team.index = df_team.index + 1
        st.dataframe(df_team, use_container_width=True)
    else:
        st.info("No team data yet.")

    conn.close()


# ==============================================================
# PAGE 3 — SQL ANALYTICS
# ==============================================================

elif page == "📊 SQL Analytics":
    from db_connection import connect_db

    st.title("📊 SQL Analytics")
    st.caption("25 SQL queries — Beginner to Advanced | SELECT → Window Functions")
    st.divider()

    conn = connect_db()

    # Helper to render query result
    def show_query(title, sql, conn, params=None):
        with st.expander(title):
            st.code(sql.strip(), language="sql")
            try:
                if params:
                    rows = conn.execute(sql, params).fetchall()
                else:
                    rows = conn.execute(sql).fetchall()
                if rows:
                    cols = [desc[0] for desc in conn.execute(sql, params or []).description] if params else [desc[0] for desc in conn.execute(sql).description]
                    st.dataframe(pd.DataFrame(rows, columns=cols), use_container_width=True, hide_index=True)
                else:
                    st.info("No data found for this query.")
            except Exception as e:
                st.error(f"Query error: {e}")

    st.subheader("🟢 Beginner Queries (1–8)")

    show_query("Q1. All Matches", "SELECT * FROM matches", conn)
    show_query("Q2. Recent 5 Matches", "SELECT * FROM matches ORDER BY match_id DESC LIMIT 5", conn)
    show_query("Q3. Total Match Count", "SELECT COUNT(*) AS total_matches FROM matches", conn)
    show_query("Q4. All Distinct Teams", "SELECT team1 FROM matches UNION SELECT team2 FROM matches", conn)
    show_query("Q5. All Players", "SELECT * FROM players", conn)
    show_query("Q6. Top 10 Run Scorers", "SELECT name, team, runs FROM players ORDER BY runs DESC LIMIT 10", conn)
    show_query("Q7. Top 10 Wicket Takers", "SELECT name, team, wickets FROM players ORDER BY wickets DESC LIMIT 10", conn)
    show_query("Q8. Players With Zero Wickets", "SELECT name, team FROM players WHERE wickets = 0", conn)

    st.divider()
    st.subheader("🟡 Intermediate Queries (9–17)")

    show_query("Q9. Matches Per Team (GROUP BY)", """
        SELECT team1 AS team, COUNT(*) AS matches_played
        FROM matches GROUP BY team1
        ORDER BY matches_played DESC
    """, conn)

    show_query("Q10. Matches Per Venue", """
        SELECT venue, COUNT(*) AS total
        FROM matches GROUP BY venue
        ORDER BY total DESC
    """, conn)

    show_query("Q11. Matches by Status Filter (LIKE)", """
        SELECT * FROM matches WHERE status LIKE '%won%'
    """, conn)

    show_query("Q12. Repeated Venues (HAVING)", """
        SELECT venue, COUNT(*) AS cnt
        FROM matches GROUP BY venue
        HAVING COUNT(*) > 1
    """, conn)

    show_query("Q13. Players Above Average Runs (Subquery)", """
        SELECT name, team, runs FROM players
        WHERE runs > (SELECT AVG(runs) FROM players)
        ORDER BY runs DESC
    """, conn)

    show_query("Q14. Highest Run Scorer", """
        SELECT name, team, MAX(runs) AS highest_runs FROM players
    """, conn)

    show_query("Q15. Highest Wicket Taker", """
        SELECT name, team, MAX(wickets) AS most_wickets FROM players
    """, conn)

    show_query("Q16. Team-wise Player Count", """
        SELECT team, COUNT(*) AS total_players
        FROM players GROUP BY team ORDER BY total_players DESC
    """, conn)

    show_query("Q17. Total Runs Per Team (JOIN-like GROUP)", """
        SELECT team, SUM(runs) AS total_runs
        FROM players GROUP BY team ORDER BY total_runs DESC
    """, conn)

    st.divider()
    st.subheader("🔴 Advanced Queries (18–25)")

    show_query("Q18. Rank Players by Runs (WINDOW FUNCTION)", """
        SELECT name, team, runs,
        RANK() OVER (ORDER BY runs DESC) AS run_rank
        FROM players
    """, conn)

    show_query("Q19. Running Total of Runs (SUM OVER)", """
        SELECT name, runs,
        SUM(runs) OVER (ORDER BY runs DESC) AS cumulative_runs
        FROM players
    """, conn)

    show_query("Q20. Dense Rank by Wickets", """
        SELECT name, team, wickets,
        DENSE_RANK() OVER (ORDER BY wickets DESC) AS wicket_rank
        FROM players
    """, conn)

    show_query("Q21. Row Number per Player", """
        SELECT ROW_NUMBER() OVER (ORDER BY runs DESC) AS row_num,
        name, team, runs FROM players
    """, conn)

    show_query("Q22. Top 5 Matches Using Subquery", """
        SELECT * FROM matches
        WHERE match_id IN (SELECT match_id FROM matches ORDER BY match_id DESC LIMIT 5)
    """, conn)

    show_query("Q23. CTE — Top Run Scorers", """
        WITH top_runs AS (
            SELECT name, team, runs FROM players ORDER BY runs DESC LIMIT 5
        )
        SELECT * FROM top_runs
    """, conn)

    show_query("Q24. CTE — Players With Both Runs and Wickets", """
        WITH all_rounders AS (
            SELECT name, team, runs, wickets
            FROM players WHERE runs > 0 AND wickets > 0
        )
        SELECT *, (runs + wickets * 20) AS performance_score
        FROM all_rounders ORDER BY performance_score DESC
    """, conn)

    show_query("Q25. NTILE — Divide Players into 4 Performance Groups", """
        SELECT name, runs,
        NTILE(4) OVER (ORDER BY runs DESC) AS performance_group
        FROM players
    """, conn)

    conn.close()


# ==============================================================
# PAGE 4 — CRUD OPERATIONS
# ==============================================================

elif page == "🛠 CRUD Operations":
    from db_connection import connect_db

    st.title("🛠️ CRUD Operations")
    st.caption("Create · Read · Update · Delete — Manage your Cricket Database")
    st.divider()

    conn = connect_db()

    crud_tab = st.tabs(["➕ Create", "📖 Read", "✏️ Update", "🗑️ Delete"])

    # ==================== CREATE ====================
    with crud_tab[0]:
        st.subheader("➕ Add New Record")
        entity = st.radio("Choose table", ["Player", "Match"], horizontal=True)

        if entity == "Player":
            st.markdown("**Add a Player**")
            p_name = st.text_input("Player Name")
            p_team = st.text_input("Team")
            p_runs = st.number_input("Runs", min_value=0, step=1)
            p_wkts = st.number_input("Wickets", min_value=0, step=1)

            if st.button("➕ Insert Player"):
                if p_name and p_team:
                    conn.execute(
                        "INSERT INTO players (name, team, runs, wickets) VALUES (?, ?, ?, ?)",
                        (p_name, p_team, int(p_runs), int(p_wkts))
                    )
                    conn.commit()
                    st.success(f"Player **{p_name}** added successfully! ✅")
                else:
                    st.warning("Please fill in Name and Team.")

        else:
            st.markdown("**Add a Match**")
            m_id   = st.number_input("Match ID", min_value=1, step=1)
            m_t1   = st.text_input("Team 1")
            m_t2   = st.text_input("Team 2")
            m_stat = st.text_input("Status")
            m_ven  = st.text_input("Venue")

            if st.button("➕ Insert Match"):
                if m_t1 and m_t2:
                    try:
                        conn.execute(
                            "INSERT OR IGNORE INTO matches (match_id, team1, team2, status, venue) VALUES (?, ?, ?, ?, ?)",
                            (int(m_id), m_t1, m_t2, m_stat, m_ven)
                        )
                        conn.commit()
                        st.success(f"Match **{m_t1} vs {m_t2}** added! ✅")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Please fill in both team names.")

    # ==================== READ ====================
    with crud_tab[1]:
        st.subheader("📖 View Records")
        view_tab = st.tabs(["🏏 Players", "📋 Matches"])

        with view_tab[0]:
            search_name = st.text_input("🔍 Search by Player Name (optional)")
            if search_name:
                rows = conn.execute(
                    "SELECT * FROM players WHERE name LIKE ?", (f"%{search_name}%",)
                ).fetchall()
            else:
                rows = conn.execute("SELECT * FROM players ORDER BY runs DESC").fetchall()

            if rows:
                df = pd.DataFrame(rows, columns=["ID", "Name", "Runs", "Wickets", "Team"])
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.caption(f"Total records: {len(df)}")
            else:
                st.info("No player records found.")

        with view_tab[1]:
            rows = conn.execute("SELECT * FROM matches ORDER BY match_id DESC").fetchall()
            if rows:
                df = pd.DataFrame(rows, columns=["Match ID", "Team 1", "Team 2", "Status", "Venue"])
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.caption(f"Total matches: {len(df)}")
            else:
                st.info("No match records found.")

    # ==================== UPDATE ====================
    with crud_tab[2]:
        st.subheader("✏️ Update Record")
        update_entity = st.radio("Update table", ["Player", "Match"], horizontal=True, key="upd_entity")

        if update_entity == "Player":
            players_list = conn.execute("SELECT player_id, name, team FROM players").fetchall()
            if players_list:
                options = {f"{p[1]} ({p[2]}) [ID:{p[0]}]": p[0] for p in players_list}
                selected = st.selectbox("Select Player to Update", list(options.keys()))
                pid = options[selected]

                current = conn.execute("SELECT * FROM players WHERE player_id = ?", (pid,)).fetchone()
                new_runs = st.number_input("New Runs", value=int(current[2]), min_value=0, step=1)
                new_wkts = st.number_input("New Wickets", value=int(current[3]), min_value=0, step=1)
                new_team = st.text_input("New Team", value=current[4])

                if st.button("💾 Update Player"):
                    conn.execute(
                        "UPDATE players SET runs = ?, wickets = ?, team = ? WHERE player_id = ?",
                        (int(new_runs), int(new_wkts), new_team, pid)
                    )
                    conn.commit()
                    st.success("Player updated successfully! ✅")
            else:
                st.info("No players in database yet.")

        else:
            matches_list = conn.execute("SELECT match_id, team1, team2 FROM matches").fetchall()
            if matches_list:
                options = {f"{m[1]} vs {m[2]} [ID:{m[0]}]": m[0] for m in matches_list}
                selected = st.selectbox("Select Match to Update", list(options.keys()))
                mid = options[selected]

                current = conn.execute("SELECT * FROM matches WHERE match_id = ?", (mid,)).fetchone()
                new_status = st.text_input("New Status", value=current[3] or "")
                new_venue  = st.text_input("New Venue", value=current[4] or "")

                if st.button("💾 Update Match"):
                    conn.execute(
                        "UPDATE matches SET status = ?, venue = ? WHERE match_id = ?",
                        (new_status, new_venue, mid)
                    )
                    conn.commit()
                    st.success("Match updated successfully! ✅")
            else:
                st.info("No matches in database yet.")

    # ==================== DELETE ====================
    with crud_tab[3]:
        st.subheader("🗑️ Delete Record")
        del_entity = st.radio("Delete from table", ["Player", "Match"], horizontal=True, key="del_entity")

        if del_entity == "Player":
            players_list = conn.execute("SELECT player_id, name, team FROM players").fetchall()
            if players_list:
                options = {f"{p[1]} ({p[2]}) [ID:{p[0]}]": p[0] for p in players_list}
                selected = st.selectbox("Select Player to Delete", list(options.keys()))
                pid = options[selected]

                st.warning(f"⚠️ Are you sure you want to delete **{selected}**?")
                if st.button("🗑️ Confirm Delete Player"):
                    conn.execute("DELETE FROM players WHERE player_id = ?", (pid,))
                    conn.commit()
                    st.success("Player deleted! ✅")
                    st.rerun()
            else:
                st.info("No players to delete.")

        else:
            matches_list = conn.execute("SELECT match_id, team1, team2 FROM matches").fetchall()
            if matches_list:
                options = {f"{m[1]} vs {m[2]} [ID:{m[0]}]": m[0] for m in matches_list}
                selected = st.selectbox("Select Match to Delete", list(options.keys()))
                mid = options[selected]

                st.warning(f"⚠️ Are you sure you want to delete match **{selected}**?")
                if st.button("🗑️ Confirm Delete Match"):
                    conn.execute("DELETE FROM matches WHERE match_id = ?", (mid,))
                    conn.commit()
                    st.success("Match deleted! ✅")
                    st.rerun()
            else:
                st.info("No matches to delete.")

    conn.close()