import streamlit as st
import base64
import time
from pathlib import Path

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="HyperWalk - Move Daily!",
    page_icon="🏃",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- SESSION STATE ---
if "steps" not in st.session_state:
    st.session_state.steps = 42500
if "distance" not in st.session_state:
    st.session_state.distance = 32.0
if "stairs" not in st.session_state:
    st.session_state.stairs = 84
if "is_walking" not in st.session_state:
    st.session_state.is_walking = False

# --- UTILS ---
def get_image_as_base64(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

# --- THEME & CSS ---
def inject_custom_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Fredoka', sans-serif;
    }}

    .stButton > button {{
        font-family: 'Fredoka', sans-serif !important;
        border-radius: 20px !important;
        font-size: 1.5rem !important;
        padding: 1rem !important;
        background-color: #58cc02 !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 6px 0 #46a302 !important;
        transition: all 0.1s !important;
    }}

    .stButton > button:active {{
        transform: translateY(4px) !important;
        box-shadow: 0 2px 0 #46a302 !important;
    }}

    .stop-btn > div > button {{
        background-color: #ff4b4b !important;
        box-shadow: 0 6px 0 #d93d3d !important;
    }}

    /* Global Overrides */
    .main {{
        background-color: #f7f7f7;
    }}

    /* Top Nav */
    .top-nav {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 2px solid #e5e5e5;
        margin-bottom: 2rem;
    }}

    .nav-stats {{
        display: flex;
        gap: 1.5rem;
        font-size: 1.5rem;
        font-weight: 600;
    }}

    .stat-item {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}

    .fire {{ color: #ff9600; }}
    .gem {{ color: #1cb0f6; }}

    /* Goal Bar */
    .goal-container {{
        background: white;
        border: 2px solid #e5e5e5;
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 0 #e5e5e5;
    }}

    .progress-wrapper {{
        background: #e5e5e5;
        height: 24px;
        border-radius: 12px;
        margin-top: 1rem;
        overflow: hidden;
    }}

    .progress-fill {{
        background: #58cc02;
        height: 100%;
        width: 65%;
        transition: width 0.5s ease;
    }}

    /* Roadmap Tasks */
    .day-header {{
        font-size: 1.8rem;
        margin-top: 2.5rem;
        margin-bottom: 1rem;
        color: #afafaf;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
        border-left: 8px solid #58cc02;
        padding-left: 1rem;
    }}

    .task-card {{
        background: white;
        border: 2px solid #e5e5e5;
        border-radius: 24px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        box-shadow: 0 6px 0 #e5e5e5;
    }}

    .task-card.completed {{
        background: #d7ffb7;
        border-color: #58cc02;
        box-shadow: 0 6px 0 #58cc02;
    }}

    .task-icon {{ font-size: 2.5rem; width: 60px; text-align: center; }}
    .task-info h3 {{ margin: 0; font-size: 1.6rem; }}
    .task-info p {{ margin: 0; color: #777; font-size: 1.2rem; }}

    /* Stats Dashboard */
    .stats-footer {{
        background: #2b70c9;
        color: white;
        border-radius: 24px;
        padding: 2rem;
        margin-top: 3rem;
        box-shadow: 0 8px 0 #1c4a85;
    }}

    .stats-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 1rem;
        text-align: center;
    }}

    .big-stat {{ font-size: 2.8rem; font-weight: 600; display: block; }}
    .stat-label {{ font-size: 1.1rem; opacity: 0.9; text-transform: uppercase; }}

    .speech-bubble {{
        background: white;
        border: 2px solid #e5e5e5;
        border-radius: 20px;
        padding: 1.2rem;
        position: relative;
        display: inline-block;
        margin-left: 20px;
        font-size: 1.4rem;
        box-shadow: 0 4px 0 #e5e5e5;
        max-width: 300px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- APP LAYOUT ---
def main():
    inject_custom_css()

    # Top Nav
    st.markdown(f"""
    <div class="top-nav">
        <div style="font-size: 2.2rem; font-weight: 600; color: #58cc02;">HyperWalk</div>
        <div class="nav-stats">
            <div class="stat-item fire">🔥 7</div>
            <div class="stat-item gem">💎 142</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # LIVE WALK SIMULATION
    if st.session_state.is_walking:
        placeholder = st.empty()
        if st.button("STOP WALK 🛑", key="stop", use_container_width=True):
            st.session_state.is_walking = False
            st.success(f"Walk Finished! You added {st.session_state.steps - 42500} steps today!")
            st.balloons()
            st.rerun()
        
        # Simulation Loop
        for _ in range(20): # Simulate a few updates
            if not st.session_state.is_walking: break
            st.session_state.steps += 12
            st.session_state.distance += 0.01
            placeholder.markdown(f"""
            <div style="background: #58cc02; color: white; padding: 2rem; border-radius: 30px; text-align: center; margin-bottom: 2rem; box-shadow: 0 10px 0 #46a302;">
                <div style="font-size: 1.5rem; text-transform: uppercase;">Walking Active...</div>
                <div style="font-size: 5rem; font-weight: 600;">{st.session_state.steps:,}</div>
                <div style="font-size: 2rem;">{st.session_state.distance:.2f} km</div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.5)
        st.rerun()

    else:
        # Goal Bar
        st.markdown(f"""
        <div class="goal-container">
            <div style="display: flex; justify-content: space-between; align-items: end;">
                <div style="font-size: 1.8rem; font-weight: 600;">Daily Goal</div>
                <div style="color: #777; font-size: 1.2rem;">{st.session_state.steps % 10000:,} / 10,000 steps</div>
            </div>
            <div class="progress-wrapper">
                <div class="progress-fill" style="width: {(st.session_state.steps % 10000) / 100}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("START LIVE WALK 👣", use_container_width=True):
            st.session_state.is_walking = True
            st.rerun()

    # Mascot with Quote
    cheetah_base64 = get_image_as_base64("assets/cheetah.png")
    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: center; margin-top: 2rem; margin-bottom: 2rem;">
        <img src="data:image/png;base64,{cheetah_base64}" style="width: 140px;">
        <div class="speech-bubble">
            "{ "Keep those legs moving, friend! We're almost at the top!" if st.session_state.is_walking else "Ready for a stroll today? Your cheetah coach is waiting!" }"
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ROADMAP
    days = [
        ("Monday - Warm up", [("🏡", "Morning Stretch", "Done! +10 XP", True), ("🥦", "Grocery Run", "30 mins • 2k steps", False)]),
        ("Tuesday - The Climb", [("⛰️", "Stair Master", "12 flights", False), ("🌳", "Park Expedition", "5k steps", False)]),
        ("Wednesday - Market Sprint", [("🛒", "Market Hustle", "Quick 15 min walk", False)]),
        ("Thursday - Evening Glow", [("🌅", "Sunset Stroll", "3k steps • Relax", False)]),
        ("Friday - Power Hour", [("⚡", "Interval Walk", "Vary your speed!", False)]),
        ("Saturday - Long Trek", [("🗺️", "Exploration", "10k steps goal", False)]),
        ("Sunday - Recover", [("🧘", "Lazy Stride", "Gentle movement", False)]),
    ]

    for day_title, tasks in days:
        st.markdown(f'<div class="day-header">{day_title}</div>', unsafe_allow_html=True)
        for icon, title, desc, done in tasks:
            st.markdown(f"""
            <div class="task-card {'completed' if done else ''}">
                <div class="task-icon">{icon}</div>
                <div class="task-info">
                    <h3>{title}</h3>
                    <p>{desc}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # BIG STATS DASHBOARD
    st.markdown(f"""
    <div class="stats-footer">
        <div style="font-size: 1.8rem; margin-bottom: 1.5rem; font-weight: 600;">Your Weekly Performance</div>
        <div class="stats-grid">
            <div>
                <span class="big-stat">{st.session_state.steps // 1000}k</span>
                <span class="stat-label">Total Steps</span>
            </div>
            <div>
                <span class="big-stat">{st.session_state.distance:.1f}</span>
                <span class="stat-label">Kilometers</span>
            </div>
            <div>
                <span class="big-stat">{st.session_state.stairs}</span>
                <span class="stat-label">Stairs Climbed</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
