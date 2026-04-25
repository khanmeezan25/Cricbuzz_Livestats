🏏 Cricbuzz LiveStats
A full-stack cricket analytics dashboard built with Python and Streamlit. It fetches real-time match data from the Cricbuzz API, stores it in a local SQLite database, and provides an interactive interface for live scores, player stats, SQL analytics, and full CRUD operations.


📁 Project Structure

cricbuzz_livestats/
│
├── app.py                 # Main Streamlit application (all 4 pages)
├── api_fetch.py           # Cricbuzz API functions (live, recent, scorecard)
├── db_connection.py       # SQLite database connection
├── create_tables.py       # Creates matches & players tables
├── insert_data.py         # Fetches API data and inserts into DB
├── queries.py             # 25  SQL query functions
├── requirements.txt       # Python dependencies
├── cricket.db             # SQLite database (auto-created on first run)
└── README.md              # Project documentation


⚙️ Setup Instructions

1. Download the Project
 git clone <https://github.com/khanmeezan25/Cricbuzz_Livestats>
 cd cricbuzz_livestats

2. Install Dependencies
   pip install -r requirements.txt

3. Configure API Key
   Open api_fetch.py and replace the API key with your own:
   API_KEY = "YOUR_RAPIDAPI_KEY_HERE"

4. Create Database Tables
   python create_tables.py

5. Run the Application
   streamlit run app.py


📊 Pages & Features

📡 Live Match
Fetches real-time live matches from Cricbuzz API
If no live match is running, automatically shows recent/completed matches
Displays match details: teams, venue, series name, status
Shows live scores (runs/wickets/overs) for each innings
Full batting and bowling scorecard with detailed stats

🏆 Top Player Stats
Sync latest player data from API into local database
Top 10 run scorers with bar chart
Top 10 wicket takers with bar chart
All-rounders list (players with both runs and wickets)
Team-wise player count table

📊 SQL Analytics
25 SQL queries across 3 difficulty levels
Each query shows the SQL code + live result from database
Easy (Q1–Q8): SELECT, COUNT, DISTINCT, LIMIT
Medium (Q9–Q17): GROUP BY, HAVING, LIKE, Subqueries, JOIN-style
Advanced (Q18–Q25): RANK(), DENSE_RANK(), ROW_NUMBER(), NTILE(), CTEs, SUM OVER()

🛠 CRUD Operations
Create: Add new players or matches manually
Read: Search and view all records with filters
Update: Edit player stats or match status
Delete: Remove players or matches with confirmation   


📦 Dependencies
streamlit
pandas
requests


🔄 Data Flow
Cricbuzz API (RapidAPI)
        ↓
   api_fetch.py          ← fetches live/recent matches & scorecards
        ↓
   insert_data.py        ← parses and inserts into SQLite
        ↓
   cricket.db            ← local database (matches + players tables)
        ↓
   app.py (Streamlit)    ← displays everything on the dashboard


   👨‍💻 Tech Stack
   Python - Core language
   Streamlit - Web dashboard
   SQLite - Local database
   Pandas - Data manipulation
   Requests - HTTP API calls
   Cricbuzz API (RapidAPI) - Real-time cricket data

           
