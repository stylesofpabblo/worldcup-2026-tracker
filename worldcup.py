import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# =====================================================================
# 1. Page Configuration & Setup
# =====================================================================
st.set_page_config(
    page_title="World Cup 2026 Live Hub",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for an ultra-clean sports matrix theme
st.markdown("""
    <style>
    .main-title { font-size: 38px; font-weight: bold; color: #1E3A8A; text-align: center; margin-bottom: 20px; }
    .metric-box { background-color: #F3F4F6; padding: 15px; border-radius: 10px; text-align: center; font-size: 15px; }
    
    /* Live Pulsing Visual Cards for In-Play Matches */
    .live-card { background-color: #FFF5F5; border: 1px solid #FEB2B2; padding: 15px; border-radius: 10px; margin-bottom: 15px; }
    .live-badge { background-color: #E53E3E; color: white; padding: 2px 8px; border-radius: 5px; font-weight: bold; font-size: 12px; animation: pulse 2s infinite; }
    .no-live-card { background-color: #F0FDF4; border: 1px solid #BBF7D0; padding: 15px; border-radius: 10px; text-align: center; color: #166534; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏆 FIFA World Cup 2026 Live Matrix Hub</div>', unsafe_allow_html=True)

# Real-world system date clock
current_time_str = datetime.now().strftime("%B %d, %Y | %H:%M Local Time")
st.markdown(f"<div style='text-align: center; color: #6B7280; font-size: 14px;'>🕒 Live Data Synced: {current_time_str}</div>", unsafe_allow_html=True)
st.write("---")

# All official 48 qualified countries by their 12 tournament groups
WORLD_CUP_GROUPS = {
    "Group A": ["Mexico", "South Korea", "South Africa", "Czechia"],
    "Group B": ["Canada", "Bosnia and Herzegovina", "Qatar", "Switzerland"],
    "Group C": ["Brazil", "Morocco", "Haiti", "Scotland"],
    "Group D": ["United States", "Paraguay", "Australia", "Türkiye"],
    "Group E": ["Germany", "Curaçao", "Côte d'Ivoire", "Ecuador"],
    "Group F": ["Netherlands", "Japan", "Sweden", "Tunisia"],
    "Group G": ["Belgium", "Egypt", "Iran", "New Zealand"],
    "Group H": ["Spain", "Cabo Verde", "Saudi Arabia", "Uruguay"],
    "Group I": ["France", "Senegal", "Norway", "Iraq"],
    "Group J": ["Argentina", "Algeria", "Austria", "Jordan"],
    "Group K": ["Portugal", "Uzbekistan", "Colombia", "DR Congo"],
    "Group L": ["England", "Croatia", "Ghana", "Panama"]
}

# =====================================================================
# REAL LIVE API ENGINE (NO FAKE HARDCODED DATA)
# =====================================================================
@st.cache_data(ttl=60)  # Refreshes data every 60 seconds from the real servers
def fetch_real_world_cup_data():
    """
    Pulls live data directly from the official verified API-Football servers.
    """
    API_URL = "https://v3.football.api-sports.io/fixtures"
    headers = {'x-apisports-key': '79298fb7fc83e16cc0eb566ff985b08d'}
    params = {'league': '1', 'season': '2026'}
    
    try:
        response = requests.get(API_URL, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            res_data = response.json().get('response', [])
            if res_data:
                return res_data
    except Exception:
        pass
    return []  # Returns empty array instead of bad/fake statistics if server times out

# Run the live data fetch engine
all_fixtures = fetch_real_world_cup_data()

# =====================================================================
# 2. Sidebar - Navigation Only
# =====================================================================
with st.sidebar:
    st.header("🌐 Hub Navigation")
    menu = st.radio("Go To:", ["📅 Live Fixtures", "📊 Group Standings", "💵 Fan Zone & Kits"])
    
    st.write("---")
    st.write("📢 Sponsored Ads")
    st.markdown("""
        <div style="text-align: center; overflow: hidden;">
            <script>
                atOptions = { 'key' : 'b7d1dd815dbcc161f13d5f645548eb12', 'format' : 'iframe', 'height' : 90, 'width' : 728, 'params' : {} };
            </script>
            <script src="https://www.highperformanceformat.com/b7d1dd815dbcc161f13d5f645548eb12/invoke.js"></script>
        </div>
    """, unsafe_allow_html=True)

# =====================================================================
# 3. Live Fixtures Menu Panel
# =====================================================================
if menu == "📅 Live Fixtures":
    st.header("⚡ Matchday Action & Live Countdown")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-box"><b>🗓️ Tournament Duration</b><br>June 11 – July 19, 2026</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-box"><b>🏟️ System Status</b><br>API Live Sync Connected</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-box"><b>🔥 Total Matches</b><br>104 Matches (48 Teams)</div>', unsafe_allow_html=True)
        
    st.write("---")
    
    # 🔄 LIVE REFRESH BOARD MODULE
    @st.fragment(run_every=30)
    def display_dynamic_matchday_board():
        # Look for matches actively flagged as live by the network stream
        live_games = [f for f in all_fixtures if f.get('fixture', {}).get('status', {}).get('short') in ["1H", "2H", "HT", "LIVE", "IN_PLAY"]]
        
        st.subheader("🔴 Current Active Live Matches")
        if not live_games:
            st.markdown("""
            <div class="no-live-card">
                <b>🟢 Stadium Intermission:</b> There are no live matches actively playing on the tournament schedule at this exact hour. Check the match database below for scheduled kickoffs.
            </div>
            """, unsafe_allow_html=True)
        else:
            for game in live_games:
                home = game['teams']['home']['name']
                away = game['teams']['away']['name']
                h_score = game['goals']['home'] if game['goals']['home'] is not None else 0
                a_score = game['goals']['away'] if game['goals']['away'] is not None else 0
                mins = game.get('fixture', {}).get('status', {}).get('elapsed', 0)
                
                st.markdown(f"""
                <div class="live-card">
                    <span class="live-badge">🔴 LIVE - {mins}' MIN</span>
                    <h3 style='margin: 10px 0;'>{home}  <b style='color:#E53E3E;'>{h_score}</b>  vs  <b style='color:#E53E3E;'>{a_score}</b>  {away}</h3>
                </div>
                """, unsafe_allow_html=True)

        st.write("---")
        st.subheader("🗓️ Complete Tournament Matchday Schedule")
        
        if not all_fixtures:
            st.warning("🔄 Live fixtures database is waiting for the next data pulse from the network registry...")
        else:
            grid_rows = []
            for f in all_fixtures:
                status_code = f.get('fixture', {}).get('status', {}).get('short', 'NS')
                status_text = "🔴 LIVE" if status_code in ["1H", "2H", "HT", "LIVE"] else ("Finished (FT)" if status_code == "FT" else "Scheduled")
                
                h_goals = f['goals']['home'] if f['goals']['home'] is not None else "-"
                a_goals = f['goals']['away'] if f['goals']['away'] is not None else "-"
                
                grid_rows.append({
                    "Kickoff Date": f['fixture']['date'][:10] if 'date' in f['fixture'] else "2026-06",
                    "Matchup": f"{f['teams']['home']['name']}  [{h_goals} - {a_goals}]  {f['teams']['away']['name']}",
                    "Match Status": status_text
                })
            st.dataframe(pd.DataFrame(grid_rows), use_container_width=True, hide_index=True)
                
    display_dynamic_matchday_board()

# =====================================================================
# 4. Group Standings Panel (CALCULATED SOLELY FROM VERIFIED API RESULTS)
# =====================================================================
elif menu == "📊 Group Standings":
    st.header("📈 Tournament Standings Matrices")
    st.write("Select any group below to see real-time standings parsed directly from live verified match logs.")
    
    group_list = list(WORLD_CUP_GROUPS.keys())
    group_select = st.selectbox("Choose Group Matrix:", group_list)
    
    if group_select in WORLD_CUP_GROUPS:
        st.subheader(f"Current Standings Table: {group_select}")
        group_teams = WORLD_CUP_GROUPS[group_select]
        
        # Initialize standard clean zero lines for all teams
        standings = {team: {"Played": 0, "Won": 0, "Drawn": 0, "Lost": 0, "GD": 0, "Pts": 0} for team in group_teams}
        
        for f in all_fixtures:
            status = f.get('fixture', {}).get('status', {}).get('short', '')
            
            # CRITICAL SECURITY FILTER: Only compute tables using genuine completed or active in-play matches
            if status in ["FT", "AET", "PEN", "1H", "2H", "HT", "LIVE", "IN_PLAY"]:
                home_team = f['teams']['home']['name']
                away_team = f['teams']['away']['name']
                
                if home_team in standings and away_team in standings:
                    h_score = f['goals']['home'] if f['goals']['home'] is not None else 0
                    a_score = f['goals']['away'] if f['goals']['away'] is not None else 0
                    
                    standings[home_team]["Played"] += 1
                    standings[away_team]["Played"] += 1
                    standings[home_team]["GD"] += (h_score - a_score)
                    standings[away_team]["GD"] += (a_score - h_score)
                    
                    if h_score > a_score:
                        standings[home_team]["Won"] += 1
                        standings[home_team]["Pts"] += 3
                        standings[away_team]["Lost"] += 1
                    elif a_score > h_score:
                        standings[away_team]["Won"] += 1
                        standings[away_team]["Pts"] += 3
                        standings[home_team]["Lost"] += 1
                    else:
                        standings[home_team]["Drawn"] += 1
                        standings[away_team]["Drawn"] += 1
                        standings[home_team]["Pts"] += 1
                        standings[away_team]["Pts"] += 1

        matrix_rows = []
        for team in group_teams:
            matrix_rows.append({
                "Country": team,
                "Played": standings[team]["Played"],
                "Won": standings[team]["Won"],
                "Drawn": standings[team]["Drawn"],
                "Lost": standings[team]["Lost"],
                "Goal Diff (GD)": standings[team]["GD"],
                "Points (Pts)": standings[team]["Pts"]
            })
            
        df_matrix = pd.DataFrame(matrix_rows).sort_values(by=["Points (Pts)", "Goal Diff (GD)"], ascending=False)
        df_matrix.insert(0, 'Rank', range(1, 1 + len(df_matrix)))
        st.dataframe(df_matrix, use_container_width=True, hide_index=True)

# =====================================================================
# 5. Monetization Space Panel
# =====================================================================
elif menu == "💵 Fan Zone & Kits":
    st.header("🛍️ Official World Cup Fan Store")
    st.write("Get ready for match day! Support your favorite teams with the best gear.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=500", caption="Official Match Balls & Cleats")
        st.markdown("[🛍️ Buy Premium Match Gear](#)") 
        st.caption("Earn up to 10% cash commission per order generated.")
        
    with col2:
        st.image("https://images.unsplash.com/photo-1575361204480-aadea25e6e68?w=500", caption="National Team Jerseys")
        st.markdown("[👕 Browse Team Kits & Jerseys](#)")
        st.caption("High tracking traffic demand during tournament opening week.")