import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="World Cup 2026 Live Hub",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for a sharp layout
st.markdown("""
    <style>
    .main-title { font-size: 38px; font-weight: bold; color: #1E3A8A; text-align: center; margin-bottom: 20px; }
    .metric-box { background-color: #F3F4F6; padding: 15px; border-radius: 10px; text-align: center; font-size: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏆 FIFA World Cup 2026 Tracker & Analytics</div>', unsafe_allow_html=True)
st.write("---")

# 2. Sidebar - Navigation and Ad Unit
with st.sidebar:
    st.header("🌐 Hub Navigation")
    menu = st.radio("Go To:", ["📅 Live Fixtures", "📊 Group Standings", "💵 Fan Zone & Kits"])
    
    st.write("---")
    # Native monetization placeholder frame
    st.markdown("""
        <div style="background-color: #FEF3C7; padding: 20px; border-radius: 8px; border: 1px dashed #D97706; text-align: center;">
            <p style="color: #B45309; margin: 0; font-weight: bold;">⭐ SPONSOR AD PLACE</p>
            <p style="font-size: 12px; color: #78350F; margin: 5px 0 0 0;">Earn money per 1,000 traffic views here.</p>
        </div>
    """, unsafe_allow_html=True)

# 3. Live Fixtures Menu Panel
if menu == "📅 Live Fixtures":
    st.header("⚡ Matchday Action & Live Countdown")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-box"><b>🗓️ Tournament Duration</b><br>June 11 – July 19, 2026</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-box"><b>🏟️ Co-Hosts</b><br>USA, Canada, Mexico</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-box"><b>🔥 Total Matches</b><br>104 Matches (48 Teams)</div>', unsafe_allow_html=True)
        
    st.subheader("Upcoming Opening Matchday Fixtures")
    
    fixtures_data = {
        "Date": ["June 11, 2026", "June 11, 2026", "June 12, 2026", "June 12, 2026"],
        "Matchup": ["Mexico 🇲🇽 vs 🇿🇦 South Africa", "South Korea 🇰🇷 vs 🇨🇿 Czechia", "Canada 🇨🇦 vs 🇧🇦 Bosnia and Herzegovina", "United States 🇺🇸 vs 🇵🇾 Paraguay"],
        "Stage": ["Group A (Opener)", "Group A", "Group B", "Group D"],
        "Venue": ["Mexico City Stadium", "Estadio Guadalajara", "Toronto Stadium", "Los Angeles Stadium"],
        "Status": ["Scheduled", "Scheduled", "Scheduled", "Scheduled"]
    }
    st.dataframe(pd.DataFrame(fixtures_data), use_container_width=True, hide_index=True)

# 4. Group Standings Matrix Panel (Complete 12-Group Structure)
elif menu == "📊 Group Standings":
    st.header("📈 Tournament Matrices")
    st.write("Select a group block to review official 2026 team allocations.")
    
    # Generate choices A through L smoothly
    group_list = [f"Group {chr(65+i)}" for i in range(12)]
    group_select = st.selectbox("Choose Group Matrix:", group_list)
    
    # Fully populated database using official FIFA 2026 team allocations
    world_cup_groups = {
        "Group A": ["Mexico 🇲🇽", "South Korea 🇰🇷", "South Africa 🇿🇦", "Czechia 🇨🇿"],
        "Group B": ["Canada 🇨🇦", "Bosnia and Herzegovina 🇧🇦", "Qatar 🇶🇦", "Switzerland 🇨🇭"],
        "Group C": ["Brazil 🇧🇷", "Morocco 🇲🇦", "Haiti 🇭🇹", "Scotland 🏴󠁧󠁢󠁳󠁣󠁴󠁿"],
        "Group D": ["United States 🇺🇸", "Paraguay 🇵🇾", "Australia 🇦🇺", "Türkiye 🇹🇷"],
        "Group E": ["Germany 🇩🇪", "Curaçao 🇨🇼", "Côte d'Ivoire 🇨🇮", "Ecuador 🇪🇨"],
        "Group F": ["Netherlands 🇳🇱", "Japan 🇯🇵", "Sweden 🇸🇪", "Tunisia 🇹🇳"],
        "Group G": ["Belgium 🇧🇪", "Egypt 🇪🇬", "Iran 🇮🇷", "New Zealand 🇳🇿"],
        "Group H": ["Spain 🇪🇸", "Cabo Verde 🇨🇻", "Saudi Arabia 🇸🇦", "Uruguay 🇺🇾"],
        "Group I": ["France 🇫🇷", "Senegal 🇸🇳", "Norway 🇳🇴", "Iraq 🇮🇶"],
        "Group J": ["Argentina 🇦🇷", "Algeria 🇩🇿", "Austria 🇦🇹", "Jordan 🇯🇴"],
        "Group K": ["Portugal 🇵🇹", "Uzbekistan 🇺🇿", "Colombia 🇨🇴", "DR Congo 🇨🇩"],
        "Group L": ["England 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Croatia 🇭🇷", "Ghana 🇬🇭", "Panama 🇵🇦"]
    }
    
    if group_select in world_cup_groups:
        st.subheader(f"Current Matrix Grid: {group_select}")
        
        matrix_df = pd.DataFrame({
            "Rank": [1, 2, 3, 4],
            "Country": world_cup_groups[group_select],
            "Played": [0, 0, 0, 0],
            "Won": [0, 0, 0, 0],
            "Drawn": [0, 0, 0, 0],
            "Lost": [0, 0, 0, 0],
            "Goal Diff (GD)": [0, 0, 0, 0],
            "Points (Pts)": [0, 0, 0, 0]
        })
        st.dataframe(matrix_df, use_container_width=True, hide_index=True)

# 5. Monetization Space Panel
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