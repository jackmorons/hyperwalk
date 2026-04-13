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
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&family=Outfit:wght@400;600&display=swap');

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
        background: linear-gradient(135deg, #f0f2f5 0%, #e8ecf1 100%) !important;
    }}

    /* PREMIUM BUTTONS */
    .stButton > button {{
        font-family: 'Outfit', sans-serif !important;
        border-radius: 24px !important;
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        padding: 0.8rem 1.5rem !important;
        background: linear-gradient(135deg, #58cc02 0%, #46a302 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 8px 15px rgba(88, 204, 2, 0.2) !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        margin-bottom: 0.5rem !important;
    }}

    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 20px rgba(88, 204, 2, 0.3) !important;
    }}

    .stButton > button:active {{
        transform: translateY(2px) !important;
        box-shadow: 0 4px 10px rgba(88, 204, 2, 0.2) !important;
    }}

    /* TOP NAV NAVIGATION */
    .nav-btn > div > button {{
        background: rgba(255, 255, 255, 0.7) !important;
        color: #3c3c3c !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
        font-size: 1.2rem !important;
        border-radius: 18px !important;
        padding: 0.4rem 0.8rem !important;
        width: auto !important;
        min-width: 80px !important;
    }}
    .nav-btn-active > div > button {{
        border: 2px solid #58cc02 !important;
        background: white !important;
    }}

    /* CALENDAR BUTTONS */
    .calendar-btn > div > button {{
        background: white !important;
        color: #3c3c3c !important;
        border: 1px solid #eee !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03) !important;
        border-radius: 16px !important;
        font-size: 1.1rem !important;
        aspect-ratio: 1 !important;
        width: 100% !important;
        height: auto !important;
        min-height: 48px !important;
    }}
    .calendar-btn-active > div > button {{
        background: linear-gradient(135deg, #ff9600 0%, #ff7e00 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 8px 15px rgba(255, 150, 0, 0.2) !important;
    }}
    .calendar-btn-future > div > button {{
        opacity: 0.4 !important;
        background: #f9f9f9 !important;
        box-shadow: none !important;
    }}

    /* TOP NAV CONTAINER */
    .top-nav-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        margin-bottom: 1.5rem;
    }}

    /* SLICK CARDS */
    .slick-card {{
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.9);
        border-radius: 32px;
        padding: 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.05);
    }}

    .goal-value {{
        font-size: 4.5rem;
        font-weight: 600;
        background: linear-gradient(135deg, #3c3c3c 0%, #1a1a1a 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
    }}

    .progress-wrapper {{
        background: #edf0f3;
        height: 16px;
        border-radius: 20px;
        margin-top: 1.5rem;
        overflow: hidden;
    }}

    .progress-fill {{
        background: linear-gradient(90deg, #58cc02 0%, #83e031 100%);
        height: 100%;
        border-radius: 20px;
        transition: width 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}

    /* SPEECH BUBBLE */
    .speech-bubble {{
        background: white;
        border-radius: 24px;
        padding: 1.2rem;
        margin-left: 15px;
        font-size: 1.2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        max-width: 260px;
        color: #4b4b4b;
        position: relative;
    }}

    /* SHOP ITEMS */
    .shop-item {{
        background: white;
        border-radius: 24px;
        padding: 1.4rem;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.04);
        border: 1px solid #f8f8f8;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- VIEW FUNCTIONS ---

def draw_top_nav():
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f'<div style="font-size: 2.2rem; font-weight: 600; color: #58cc02; cursor: pointer;" onclick="window.location.reload()">HyperWalk</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<div class="{"nav-btn-active" if st.session_state.current_page == "streak" else "nav-btn"}">', unsafe_allow_html=True)
        if st.button(f"🔥 {7}"):
            st.session_state.current_page = "streak"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown(f'<div class="{"nav-btn-active" if st.session_state.current_page == "shop" else "nav-btn"}">', unsafe_allow_html=True)
        if st.button(f"💎 {142}"):
            st.session_state.current_page = "shop"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def draw_mascot(text):
    cheetah_base64 = get_image_as_base64("assets/cheetah.png")
    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: center; margin-top: 1rem; margin-bottom: 2rem;">
        <img src="data:image/png;base64,{cheetah_base64}" style="width: 130px; filter: drop-shadow(0 10px 15px rgba(0,0,0,0.08));">
        <div class="speech-bubble">"{text}"</div>
    </div>
    """, unsafe_allow_html=True)

def draw_home():
    draw_top_nav()
    draw_mascot("Unlocking new speeds today! Let's chase that goal, Giacomo!")

    # Daily Goal Progress Card
    st.markdown(f"""
    <div class="slick-card">
        <div style="font-size: 1rem; text-transform: uppercase; color: #8e9aaf; font-weight: 600; letter-spacing: 1.5px; margin-bottom: 0.5rem;">Daily Progress</div>
        <div class="goal-value">{st.session_state.steps:,}</div>
        <div style="font-size: 1.4rem; color: #5c677d; font-weight: 400;">/ 10,000 steps</div>
        <div class="progress-wrapper">
            <div class="progress-fill" style="width: {min((st.session_state.steps / 10000) * 100, 100)}%"></div>
        </div>
        <div style="display: flex; justify-content: space-around; margin-top: 2rem;">
            <div style="text-align: center;">
                <div style="font-size: 1.8rem; font-weight: 600; color: #1a1a1a;">{st.session_state.distance:.1f}</div>
                <div style="font-size: 0.8rem; color: #8e9aaf; text-transform: uppercase;">Kilometers</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.8rem; font-weight: 600; color: #1a1a1a;">{st.session_state.stairs}</div>
                <div style="font-size: 0.8rem; color: #8e9aaf; text-transform: uppercase;">Stairs</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("START LIVE WALK 👣", use_container_width=True):
        st.session_state.is_walking = True
        st.rerun()

def draw_shop():
    draw_top_nav()
    # BACK BUTTON integrated into header/nav logic, but adding a "Home" trigger
    if st.button("⬅️ BACK TO DASHBOARD", use_container_width=True):
        st.session_state.current_page = "home"
        st.rerun()
    
    st.markdown("<h2 style='text-align: center; margin-top: 1.5rem; color: #1cb0f6;'>HyperShop 💎</h2>", unsafe_allow_html=True)

    items = [
        ("Prime Sneakers", "✨ 500", "👟", "#fff9e5"),
        ("Nitro XP", "💎 100", "🧪", "#e5f6ff"),
        ("Cheetah Aura", "🔥 50", "💨", "#fff0e5"),
        ("Energy Burst", "💎 25", "⚡", "#f2e5ff"),
    ]

    for name, price, icon, bg in items:
        st.markdown(f"""
        <div class="shop-item">
            <div style="display: flex; align-items: center; gap: 1.2rem;">
                <div style="font-size: 2.8rem; background: {bg}; width: 64px; height: 64px; border-radius: 20px; display: flex; align-items: center; justify-content: center;">{icon}</div>
                <div>
                    <h3 style="margin:0; font-size: 1.4rem;">{name}</h3>
                    <p style="margin:0; color:#8e9aaf; font-size: 0.9rem;">Exclusive Upgrade</p>
                </div>
            </div>
            <div style="font-size: 1.4rem; font-weight: 600; color: #1cb0f6;">{price}</div>
        </div>
        """, unsafe_allow_html=True)

def draw_streak():
    draw_top_nav()
    if st.button("⬅️ BACK TO DASHBOARD", use_container_width=True):
        st.session_state.current_page = "home"
        st.rerun()
    
    st.markdown("<h2 style='text-align: center; margin-top: 1.5rem; color: #ff9600;'>Streak History 🔥</h2>", unsafe_allow_html=True)

    # INTERACTIVE CALENDAR
    st.markdown("<div style='background: white; border-radius: 28px; padding: 1.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.03);'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-bottom:1.5rem; font-size: 1.3rem; color: #3c3c3c;'>April 2026</h3>", unsafe_allow_html=True)
    
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
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Selected History Card
    sel = st.session_state.selected_calendar_day
    if sel and sel <= 13:
        mock_steps = [8500, 9200, 10500, 7800, 10200, 11000, 9500, 12000, 8000, 10000, 9800, 10500, 7320][sel-1]
        st.markdown(f"""
        <div class="slick-card" style="margin-top: 1.5rem; border-left: 8px solid #ff9600;">
            <div style="font-size: 1rem; font-weight: 600; color: #8e9aaf; margin-bottom: 0.5rem;">HISTORY: APRIL {sel}</div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 2.8rem; font-weight: 600; color: #1a1a1a;">{mock_steps:,}</div>
                    <div style="color: #5c677d;">Steps Cleared</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.2rem; color: #58cc02; font-weight: 600;">{'WINNER' if mock_steps >= 10000 else 'STARTED'}</div>
                    <div style="font-size: 0.9rem; color: #8e9aaf;">+50 Gems</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- SIMULATION ---

def draw_active_walk():
    placeholder = st.empty()
    if st.button("STOP AND RECOVER 🧘", key="stop", use_container_width=True):
        st.session_state.is_walking = False
        st.balloons()
        st.rerun()
    
    # Simulation Loop
    for _ in range(20):
        if not st.session_state.is_walking: break
        st.session_state.steps += 18 # Faster cheetah speed!
        st.session_state.distance += 0.015
        placeholder.markdown(f"""
        <div style="background: linear-gradient(135deg, #58cc02 0%, #46a302 100%); color: white; padding: 2.5rem; border-radius: 40px; text-align: center; margin-bottom: 2rem; box-shadow: 0 20px 40px rgba(88, 204, 2, 0.3);">
            <div style="font-size: 1.2rem; text-transform: uppercase; letter-spacing: 2px; opacity: 0.9;">Sprint Mode Active</div>
            <div style="font-size: 6rem; font-weight: 600; margin: 0.5rem 0; line-height: 1;">{st.session_state.steps:,}</div>
            <div style="font-size: 2rem; opacity: 0.9;">{st.session_state.distance:.2f} km traversed</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.4)
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
