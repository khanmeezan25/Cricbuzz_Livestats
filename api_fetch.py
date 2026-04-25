import requests

API_KEY = "b0cb5990d9msh9454d4b104d100ep12be1fjsnd00ec50f979c"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

# ===== For Live Matches =====

def get_live_matches():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
    response = requests.get(url, headers=headers)
    try:
        return response.json()
    except:
        return {"typeMatches": []}


# ===== For Recent/Previous Matches =====

def get_recent_matches():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"
    response = requests.get(url, headers=headers)
    try:
        return response.json()
    except:
        return {"typeMatches": []}


# ===== For Scorecard =====

def get_scorecard(match_id):
    url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{match_id}/scard"
    response = requests.get(url, headers=headers)
    return response.json()


# ===== Function for extract all live match details from API =====

def parse_live_matches(data):
    matches = []
    try:
        type_matches = data.get("typeMatches", [])
        for type_match in type_matches:
            for series_match in type_match.get("seriesMatches", []):
                series_wrapper = series_match.get("seriesAdWrapper", {})
                for match in series_wrapper.get("matches", []):
                    
                    # for basic match information
                    info = match.get("matchInfo", {})
                    score_list = match.get("matchScore", {})
                    
                    # Extracting team names
                    team1 = info.get("team1", {}).get("teamName", "N/A")
                    team2 = info.get("team2", {}).get("teamName", "N/A")
                    
                    # Match status and Venue details
                    status = info.get("status", "N/A")
                    venue = info.get("venueInfo", {}).get("ground", "N/A")
                    match_id = info.get("matchId", None)
                    series_name = series_wrapper.get("seriesName", "N/A")

                    # Live scores
                    team1_score = ""
                    team2_score = ""

                    t1s = score_list.get("team1Score", {})
                    t2s = score_list.get("team2Score", {})

                    if t1s:
                        inn = t1s.get("inngs1", {})
                        runs = inn.get("runs", "-")
                        wkts = inn.get("wickets", "-")
                        ovrs = inn.get("overs", "-")
                        team1_score = f"{runs}/{wkts} ({ovrs} ov)"

                    if t2s:
                        inn = t2s.get("inngs1", {})
                        runs = inn.get("runs", "-")
                        wkts = inn.get("wickets", "-")
                        ovrs = inn.get("overs", "-")
                        team2_score = f"{runs}/{wkts} ({ovrs} ov)"

                    matches.append({
                        "match_id": match_id,
                        "series": series_name,
                        "team1": team1,
                        "team2": team2,
                        "team1_score": team1_score,
                        "team2_score": team2_score,
                        "status": status,
                        "venue": venue,
                    })
    except Exception as e:
        print(f"Error parsing matches: {e}")
    return matches


# ===== Function for extract detailed scorecard for batting and bowling stats =====

def parse_scorecard(data):
    result = []
    try:
        innings_list = data.get("scoreCard", [])
        for innings in innings_list:
            innings_id = innings.get("inningsId", "?")
            bat_team = innings.get("batTeamDetails", {}).get("batTeamName", "?")

             # ----------- BATTING DATA ----------- 
            
            batsmen = []
            
            # Extracting data for each batsman
            for _, bat in innings.get("batTeamDetails", {}).get("batsmenData", {}).items():
                batsmen.append({
                    "name": bat.get("batName", "?"),
                    "runs": bat.get("runs", 0),
                    "balls": bat.get("balls", 0),
                    "fours": bat.get("fours", 0),
                    "sixes": bat.get("sixes", 0),
                    "strike_rate": bat.get("strikeRate", 0),
                    "out_desc": bat.get("outDesc", "batting"),
                })
            
            # ----------- BOWLING DATA -----------
            bowlers = []
            bowl_team = innings.get("bowlTeamDetails", {}).get("bowlTeamName", "?")
            
             # Extract data for each bowler
            for _, bowl in innings.get("bowlTeamDetails", {}).get("bowlersData", {}).items():
                bowlers.append({
                    "name": bowl.get("bowlName", "?"),
                    "overs": bowl.get("overs", 0),
                    "runs": bowl.get("runs", 0),
                    "wickets": bowl.get("wickets", 0),
                    "economy": bowl.get("economy", 0),
                    "maidens": bowl.get("maidens", 0),
                })

            result.append({
                "innings_id": innings_id,
                "bat_team": bat_team,
                "bowl_team": bowl_team,
                "batsmen": batsmen,
                "bowlers": bowlers,
            })
    except Exception as e:
        print(f"Error parsing scorecard: {e}")
    return result