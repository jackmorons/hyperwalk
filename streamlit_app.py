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
    st.session_state.steps = 7320
if "distance" not in st.session_state:
    st.session_state.distance = 5.2
if "stairs" not in st.session_state:
    st.session_state.stairs = 3
if "is_walking" not in st.session_state:
    st.session_state.is_walking = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "selected_calendar_day" not in st.session_state:
    st.session_state.selected_calendar_day = 13

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

    /* HIDE STREAMLIT BRANDING */
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display:none;}}

    /* IPHONE 17 PRO OPTIMIZATION */
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 450px !important;
        margin: 0 auto !important;
    }}

    .stApp {{
        background-color: #f7f7f7 !important;
    }}

    /* BUTTONS */
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
        width: 100% !important;
        margin-bottom: 0.5rem !important;
    }}

    .stButton > button:active {{
        transform: translateY(4px) !important;
        box-shadow: 0 2px 0 #46a302 !important;
    }}

    /* Secondary Buttons (Shop/Streak) */
    .shop-btn > div > button {{
        background-color: #1cb0f6 !important;
        box-shadow: 0 6px 0 #1899d6 !important;
    }}
    .streak-btn > div > button {{
        background-color: #ff9600 !important;
        box-shadow: 0 6px 0 #d97f00 !important;
    }}
    .back-btn > div > button {{
        background-color: #afafaf !important;
        box-shadow: 0 6px 0 #8c8c8c !important;
        font-size: 1.1rem !important;
        padding: 0.5rem !important;
    }}

    /* CALENDAR BUTTONS */
    .calendar-btn > div > button {{
        background-color: white !important;
        color: #3c3c3c !important;
        border: 2px solid #e5e5e5 !important;
        box-shadow: 0 4px 0 #e5e5e5 !important;
        font-size: 1.2rem !important;
        padding: 0 !important;
        aspect-ratio: 1 !important;
        width: 100% !important;
        height: auto !important;
        min-height: 48px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    .calendar-btn-active > div > button {{
        background-color: #fff4e5 !important;
        border-color: #ff9600 !important;
        color: #ff9600 !important;
        box-shadow: 0 4px 0 #ff9600 !important;
    }}
    .calendar-btn-future > div > button {{
        opacity: 0.3 !important;
        cursor: not-allowed !important;
        background-color: #f7f7f7 !important;
        box-shadow: none !important;
    }}

    /* TOP NAV */
    .top-nav {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 2px solid #e5e5e5;
        margin-bottom: 1.5rem;
    }}

    .nav-stats {{
        display: flex;
        gap: 1rem;
        font-size: 1.4rem;
        font-weight: 600;
    }}

    .stat-item {{
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }}

    .fire {{ color: #ff9600; }}
    .gem {{ color: #1cb0f6; }}

    /* GOAL CONTAINER */
    .goal-container {{
        background: white;
        border: 2px solid #e5e5e5;
        border-radius: 30px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 0 #e5e5e5;
        text-align: center;
    }}

    .progress-wrapper {{
        background: #e5e5e5;
        height: 24px;
        border-radius: 12px;
        margin-top: 1.5rem;
        overflow: hidden;
    }}

    .progress-fill {{
        background: #58cc02;
        height: 100%;
        transition: width 0.5s ease;
    }}

    /* SPEECH BUBBLE */
    .speech-bubble {{
        background: white;
        border: 2px solid #e5e5e5;
        border-radius: 20px;
        padding: 1rem;
        position: relative;
        display: inline-block;
        margin-left: 15px;
        font-size: 1.2rem;
        box-shadow: 0 4px 0 #e5e5e5;
        max-width: 250px;
        color: #3c3c3c;
    }}

    /* SHOP ITEMS */
    .shop-item {{
        background: white;
        border: 2px solid #e5e5e5;
        border-radius: 24px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 5px 0 #e5e5e5;
    }}

    /* HISTORY CARD */
    .history-card {{
        background: white;
        border: 2px solid #e5e5e5;
        border-radius: 24px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        box-shadow: 0 8px 0 #e5e5e5;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- VIEW FUNCTIONS ---

def draw_top_nav():
    st.markdown(f"""
    <div class="top-nav">
        <div style="font-size: 2.2rem; font-weight: 600; color: #58cc02;">HyperWalk</div>
        <div class="nav-stats">
            <div class="stat-item fire">🔥 7</div>
            <div class="stat-item gem">💎 142</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def draw_mascot(text):
    cheetah_base64 = get_image_as_base64("assets/cheetah.png")
    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: center; margin-top: 1rem; margin-bottom: 2rem;">
        <img src="data:image/png;base64,{cheetah_base64}" style="width: 120px;">
        <div class="speech-bubble">"{text}"</div>
    </div>
    """, unsafe_allow_html=True)

def draw_home():
    draw_top_nav()
    draw_mascot("Looking fast today, Giacomo! Let's hit that daily goal!")

    # Daily Goal Progress
    st.markdown(f"""
    <div class="goal-container">
        <div style="font-size: 1.2rem; text-transform: uppercase; color: #afafaf; letter-spacing: 1px;">Daily Stride</div>
        <div style="font-size: 4rem; font-weight: 600; margin: 0.5rem 0;">{st.session_state.steps % 10000:,}</div>
        <div style="font-size: 1.5rem; color: #777;">steps out of 10,000</div>
        <div class="progress-wrapper">
            <div class="progress-fill" style="width: {(st.session_state.steps % 10000) / 100}%"></div>
        </div>
        <div style="display: flex; justify-content: space-around; margin-top: 1.5rem;">
            <div><b style="font-size: 1.4rem;">{st.session_state.distance:.1f}</b><br><small>KMS</small></div>
            <div><b style="font-size: 1.4rem;">{st.session_state.stairs}</b><br><small>STAIRS</small></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("START LIVE WALK 👣", use_container_width=True):
        st.session_state.is_walking = True
        st.rerun()

    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="shop-btn">', unsafe_allow_html=True)
        if st.button("SHOP 💎"):
            st.session_state.current_page = "shop"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="streak-btn">', unsafe_allow_html=True)
        if st.button("STREAK 🔥"):
            st.session_state.current_page = "streak"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def draw_shop():
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅️ HOME"):
        st.session_state.current_page = "home"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center;'>HyperShop 💎</h1>", unsafe_allow_html=True)
    # MASCOT REMOVED FROM SHOP PER REQUEST

    items = [
        ("Golden Sneakers", "✨ 500", "👟"),
        ("Double XP Potion", "💎 100", "🧪"),
        ("Cheetah Cape", "🔥 50", "🦸"),
        ("Heart Refill", "💎 25", "❤️"),
    ]

    for name, price, icon in items:
        st.markdown(f"""
        <div class="shop-item">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="font-size: 2.5rem;">{icon}</div>
                <div>
                    <h3 style="margin:0;">{name}</h3>
                    <p style="margin:0; color:#777;">Limited Edition</p>
                </div>
            </div>
            <div style="font-size: 1.5rem; font-weight: 600;">{price}</div>
        </div>
        """, unsafe_allow_html=True)

def draw_streak():
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅️ HOME"):
        st.session_state.current_page = "home"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center;'>Streak 7 🔥</h1>", unsafe_allow_html=True)
    # MASCOT REMOVED FROM STREAK PER REQUEST

    st.markdown("<h3 style='margin-bottom:1rem;'>April 2026</h3>", unsafe_allow_html=True)
    
    # INTERACTIVE CALENDAR
    for week in range(5):
        cols = st.columns(7)
        for d in range(7):
            day_num = week * 7 + d + 1
            if day_num <= 30:
                with cols[d]:
                    is_past = day_num <= 13
                    is_active = st.session_state.selected_calendar_day == day_num
                    is_streak = 7 <= day_num <= 13
                    
                    btn_class = "calendar-btn"
                    if is_active: btn_class += " calendar-btn-active"
                    if not is_past: btn_class += " calendar-btn-future"
                    
                    st.markdown(f'<div class="{btn_class}">', unsafe_allow_html=True)
                    label = "🔥" if is_streak else str(day_num)
                    
                    if st.button(label, key=f"cal_{day_num}", disabled=not is_past):
                        st.session_state.selected_calendar_day = day_num
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

    # HISTORY CARD
    sel = st.session_state.selected_calendar_day
    if sel and sel <= 13:
        mock_steps = [8500, 9200, 10500, 7800, 10200, 11000, 9500, 12000, 8000, 10000, 9800, 10500, 7320][sel-1]
        st.markdown(f"""
        <div class="history-card">
            <div style="font-size: 1.2rem; font-weight: 600; color: #ff9600; margin-bottom: 0.5rem;">
                📅 APRIL {sel}, 2026 DETAILS
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 2rem; font-weight: 600;">{mock_steps:,}</div>
                    <div style="color: #777;">steps completed</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.2rem; color: #58cc02;">{'✅ GOAL REACHED' if mock_steps >= 10000 else '🚶 KEEP WALKING'}</div>
                    <div style="font-size: 1rem; color: #777;">+50 Gems Earned</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.info("Tap a past day to view your specific task performance. Future days are locked for now!")

# --- SIMULATION ---

def draw_active_walk():
    placeholder = st.empty()
    st.markdown('<div class="stop-btn">', unsafe_allow_html=True)
    if st.button("STOP WALK 🛑", key="stop", use_container_width=True):
        st.session_state.is_walking = False
        st.success(f"Walk Finished! Well done!")
        st.balloons()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Simulation Loop
    for _ in range(20):
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

# --- MAIN ---

def main():
    inject_custom_css()

    if st.session_state.is_walking:
        draw_active_walk()
    else:
        if st.session_state.current_page == "home":
            draw_home()
        elif st.session_state.current_page == "shop":
            draw_shop()
        elif st.session_state.current_page == "streak":
            draw_streak()

if __name__ == "__main__":
    main()
