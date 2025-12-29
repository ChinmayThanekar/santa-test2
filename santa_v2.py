import streamlit as st
import random
import hashlib
import json
import os
from datetime import datetime

# Secret Santa participants
PARTICIPANTS = [
    "Alice", "Bob", "Charlie", "Diana", "Eve", 
    "Frank", "Grace", "Henry", "Ivy", "Jack"
]

# ✅ GIT-SAFE: Data folder (add data/ to .gitignore)
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
DB_FILE = os.path.join(DATA_DIR, "secret_santa_rooms.json")

# COMPLETE CSS with FIXED room input visibility
css = """
<style>
    /* RED to LIGHT GREEN Background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, 
            #b91c1c 0%, #dc2626 15%, #ef4444 30%, 
            #f97316 45%, #eab308 60%, #84cc16 75%, #4ade80 100%);
        background-size: 400% 400%;
        animation: gradientShift 25s ease infinite;
        min-height: 100vh;
        position: relative;
    }
    
    /* FIXED: Room input visibility at TOP */
    .room-input-section {
        background: rgba(255,255,255,0.98) !important;
        padding: 3rem !important;
        border-radius: 30px !important;
        margin: 2rem auto !important;
        max-width: 900px !important;
        box-shadow: 0 40px 120px rgba(0,0,0,0.5) !important;
        border: 4px solid rgba(255,255,255,0.9) !important;
        text-align: center;
    }
    
    .room-input-section * {
        color: #1f2937 !important;
        text-shadow: none !important;
    }
    
    .room-input-section [data-baseweb="input"] {
        padding: 1.5rem 2rem !important;
        font-size: 1.6rem !important;
        border: 3px solid #b91c1c !important;
        border-radius: 25px !important;
        background: #ffffff !important;
        margin-bottom: 1rem !important;
        font-weight: 600 !important;
    }
    
    .room-input-section .stButton > button {
        background: linear-gradient(45deg, #b91c1c, #dc2626) !important;
        padding: 1.5rem 4rem !important;
        font-size: 1.4rem !important;
        border-radius: 30px !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
    }
    
    /* ✅ REPLACE the universal selector with these SPECIFIC overrides */
[data-testid="stAppViewContainer"], 
.main .block-container,
.stApp > header {
    color: #ffffff !important;
}

[data-testid="stMarkdownContainer"] p, 
h1, h2, h3, .stMarkdown {
    color: #ffffff !important;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.8) !important;
}


    
    [data-testid="stAppViewContainer"] > div > div > div {
        background: transparent !important;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 100%;
        background: transparent !important;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=Dancing+Script:wght@700&display=swap');
    
    /* Christmas Lights */
    .light {
        position: fixed;
        border-radius: 50%;
        animation: twinkle 2s ease-in-out infinite;
        box-shadow: 0 0 40px currentColor;
        z-index: 999;
        top: var(--top);
        left: var(--left);
    }
    
    @keyframes twinkle {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.5); }
    }
    
    /* PERFECT WHITE CONTAINER */
    .santa-container {
        max-width: 800px;
        margin: 2rem auto;
        padding: 4rem;
        text-align: center;
        background: rgba(255,255,255,0.95) !important;
        backdrop-filter: blur(35px) brightness(1.2);
        border: 5px solid rgba(255,255,255,0.95);
        border-radius: 40px;
        box-shadow: 
            0 60px 150px rgba(0,0,0,0.6),
            inset 0 5px 40px rgba(255,255,255,0.9);
        position: relative;
        z-index: 1000;
    }
    
    .santa-container * {
        color: #1a1a1a !important;
        text-shadow: none !important;
    }
    
    /* [Rest of CSS classes - title, buttons, reveal-box, etc. - SAME as original] */
    .title {
        font-size: 5rem !important;
        font-family: 'Dancing Script', cursive !important;
        background: linear-gradient(45deg, #ffffff, #f0f9ff, #ffffff) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin-bottom: 2rem !important;
        text-shadow: 
            0 0 50px rgba(255,255,255,1),
            3px 3px 20px rgba(0,0,0,0.5) !important;
        animation: titleGlow 3s ease-in-out infinite;
        letter-spacing: 5px !important;
    }
    
    @keyframes titleGlow {
        0%, 100% { 
            filter: drop-shadow(0 0 50px rgba(255,255,255,1));
            transform: scale(1);
        }
        50% { 
            filter: drop-shadow(0 0 80px rgba(255,255,255,1));
            transform: scale(1.05);
        }
    }
    
    .reveal-btn, .status-btn, .check-btn, .stButton>button {
        background: linear-gradient(45deg, #b91c1c, #dc2626, #ef4444) !important;
        border: none !important;
        padding: 2rem 5rem !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        border-radius: 70px !important;
        color: #ffffff !important;
        cursor: pointer !important;
        box-shadow: 
            0 40px 100px rgba(185,28,28,0.8),
            inset 0 4px 25px rgba(255,255,255,0.3) !important;
        transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
        font-family: 'Poppins', sans-serif !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        margin: 1rem !important;
    }
    
    .reveal-box {
        background: linear-gradient(145deg, #ffffff, #fafbfc, #ffffff) !important;
        padding: 6rem 5rem !important;
        border-radius: 45px !important;
        margin: 4rem 0 !important;
        min-height: 320px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 4rem !important;
        font-weight: 900 !important;
        color: #b91c1c !important;
        box-shadow: 
            0 80px 200px rgba(0,0,0,0.7),
            inset 0 8px 50px rgba(255,255,255,0.95) !important;
        border: 8px solid rgba(185,28,28,0.3) !important;
        animation: revealAnim 3.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards !important;
    }
    
    @keyframes revealAnim {
        0% { opacity: 0; transform: scale(0.1) rotateY(180deg); }
        50% { opacity: 0.95; transform: scale(1.15) rotateY(0deg); }
        100% { opacity: 1; transform: scale(1) rotateY(0deg); }
    }
    
    .invalid-box {
        background: linear-gradient(145deg, #b91c1c, #991b1b) !important;
        padding: 4.5rem !important;
        border-radius: 40px !important;
        margin: 3.5rem 0 !important;
        color: #fefce8 !important;
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        box-shadow: 0 50px 120px rgba(185,28,28,0.9) !important;
        animation: shake 1s ease-in-out both !important;
        text-align: center !important;
        border: 6px solid rgba(254,252,232,0.8) !important;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    
    .status-card {
        background: rgba(255,255,255,0.98) !important;
        padding: 4rem !important;
        border-radius: 35px !important;
        margin: 2.5rem 0 !important;
        border: 4px solid rgba(255,255,255,0.95) !important;
        color: #1f2937 !important;
        box-shadow: 0 45px 120px rgba(0,0,0,0.5) !important;
    }
    
    .snowflake {
    color: #ffffff !important;              /* Pure white */
    text-shadow: none !important;           /* No glow */
    position: fixed;
    top: -50px;                             /* Start higher */
    animation: fall linear infinite;
    pointer-events: none;
    z-index: 200;                           /* Lower z-index */
    opacity: 0.8 !important;
}

@keyframes fall {
    to { 
        transform: translateY(120vh) rotate(720deg);  /* Gentler spin */
    }
}
"""

def load_database():
    """Load room database from JSON file"""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_database(database):
    """Save room database to JSON file"""
    with open(DB_FILE, 'w') as f:
        json.dump(database, f, indent=2)

def get_room_data(room_id):
    """Get or initialize room data"""
    db = load_database()
    if room_id not in db:
        db[room_id] = {
            'created': datetime.now().isoformat(),
            'participants_data': {},
            'event_name': f"Secret Santa Room {room_id}",
            'status': 'active'
        }
        save_database(db)
    return db[room_id]

def update_room_data(room_id, data):
    """Update room data in database"""
    db = load_database()
    if room_id in db:
        db[room_id].update(data)
        save_database(db)
    return get_room_data(room_id)

def generate_pin(name):
    seed = f"{name}{random.randint(1000, 9999)}"
    return str(int(hashlib.md5(seed.encode()).hexdigest(), 16) % 10000).zfill(4)

def create_christmas_effects():
    effects_html = ""
    light_positions = [
        ("3%", "3%", "#b91c1c"), ("97%", "3%", "#4ade80"),
        ("3%", "97%", "#dc2626"), ("97%", "97%", "#84cc16"),
        ("50%", "1%", "#eab308"), ("1%", "50%", "#ef4444"),
        ("99%", "50%", "#16a34a"), ("50%", "99%", "#b91c1c")
    ]
    
    # Christmas Lights (unchanged)
    for top, left, color in light_positions:
        effects_html += f"""
        <div class="light" style="
            --top: {top}; --left: {left};
            width: 50px; height: 50px;
            background: {color};
            animation-duration: {random.uniform(1.8, 4.2)}s;
        "></div>
        """
    
    # ✅ OPTIMIZED SNOWFLAKES: 40 (was 150), smaller (1-1.8rem), pure white
    for i in range(40):  # Reduced density: 40 snowflakes
        effects_html += f"""
        <div class="snowflake" style="
            left: {random.randint(0, 100)}vw;
            animation-delay: {random.uniform(0, 20)}s;
            animation-duration: {random.uniform(25, 50)}s;
            font-size: {random.choice(['1rem', '1.2rem', '1.5rem', '1.8rem'])};
            opacity: {random.uniform(0.6, 0.9)};
        ">❄</div>
        """
    return effects_html

def is_valid_participant(name, participants):
    return name.strip().lower() in [p.lower() for p in participants]

def main():
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(create_christmas_effects(), unsafe_allow_html=True)
    
    # ✅ ROOM INPUT - PROMINENTLY VISIBLE
    st.markdown('<div class="room-input-section">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #b91c1c; text-align: center; margin-bottom: 2rem;">🏠 Enter Room ID</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        room_id = st.text_input("Event/Room ID", placeholder="office2025, family-xmas, etc.", key="room_id")
    with col2:
        if st.button("➕ Join Room", key="join_room", use_container_width=True):
            if room_id.strip():
                st.session_state.selected_room = room_id.strip()
                st.rerun()
            else:
                st.error("Enter a room ID first!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Stop if no room selected
    if 'selected_room' not in st.session_state or not st.session_state.selected_room:
        st.markdown("""
        <div style='text-align: center; padding: 4rem; background: rgba(255,255,255,0.9); 
                    border-radius: 25px; margin: 2rem auto; max-width: 600px;'>
            <h2 style='color: #b91c1c;'>🎅 Welcome to Secret Santa! 🎁</h2>
            <p style='font-size: 1.4rem; color: #1f2937;'>
                Enter your <strong>Room/Event ID</strong> above to join!<br>
                Examples: <code>office2025</code>, <code>family-xmas</code>
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()
    
    # Load room data
    room_id = st.session_state.selected_room
    room_data = get_room_data(room_id)
    
    # Main app container
    st.markdown('<div class="santa-container">', unsafe_allow_html=True)
    
    st.markdown(f'<h3 style="color: #b91c1c; margin-bottom: 2rem;">📍 Room: <strong>{room_id}</strong></h3>', unsafe_allow_html=True)
    
    # Session state for current room
    session_key = f"room_{room_id}"
    for key in ['revealed', 'user_name', 'pin_generated', 'secret_santa']:
        if f"{session_key}_{key}" not in st.session_state:
            st.session_state[f"{session_key}_{key}"] = False if key != 'user_name' else ""
    
    tab1, tab2, tab3 = st.tabs(["🎅 Draw Secret Santa", "📋 Check Status", "📊 Room Stats"])
    
    with tab1:
        st.markdown('<h1 class="title">🎅 Secret Santa 🎁</h1>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 2rem; color: #1f2937; margin-bottom: 3rem; font-weight: 700;">Ho Ho Ho! Enter your name to discover who drew YOU!</p>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #16a34a, #15803d); padding: 3.5rem; border-radius: 35px; margin: 3.5rem 0; color: #ffffff; font-size: 1.6rem; border: 5px solid rgba(255,255,255,0.9); box-shadow: 0 40px 100px rgba(22,163,74,0.6); font-weight: 700;">
            <strong>🎄 Valid Participants:</strong><br>
            <span style="font-size: 1.8rem;">{', '.join(PARTICIPANTS)}</span> 🎄
        </div>
        """, unsafe_allow_html=True)
        
        name = st.text_input("", placeholder="👤 Enter your name here...", key=f"name_input_{session_key}")
        
        if st.button("🎊 REVEAL MY SECRET SANTA 🎊", key=f"reveal_btn_{session_key}"):
            if name.strip():
                if is_valid_participant(name, PARTICIPANTS):
                    participants_data = room_data.get('participants_data', {})
                    if name not in participants_data or not participants_data[name].get('drawn', False):
                        other_names = [n for n in PARTICIPANTS if n.lower() != name.lower()]
                        secret_santa = random.choice(other_names)
                        pin = generate_pin(name)
                        
                        participants_data[name] = {
                            'secret_santa': secret_santa,
                            'pin': pin,
                            'drawn': True,
                            'drawn_at': datetime.now().isoformat()
                        }
                        
                        update_room_data(room_id, {'participants_data': participants_data})
                        
                        st.session_state[f'{session_key}_user_name'] = name.strip()
                        st.session_state[f'{session_key}_secret_santa'] = secret_santa
                        st.session_state[f'{session_key}_pin_generated'] = pin
                        st.session_state[f'{session_key}_revealed'] = True
                        st.rerun()
                    else:
                        st.markdown("""
                        <div class="invalid-box">
                            ❌ You have already drawn your Secret Santa!<br>
                            Go to <strong>Check Status</strong> tab with your PIN! 🎅
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="invalid-box">
                        ❌ <strong>{name}</strong> is not a valid participant!<br>
                        🎅 Please check the list above and try again! 🎅
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("🎄 Please enter your name first!")
        
        if st.session_state.get(f'{session_key}_revealed', False):
            st.markdown(f"""
            <div class="reveal-box">
                <div style="font-size: 2.5rem; margin-bottom: 3rem; font-weight: 800;">
                    Hey <strong>{st.session_state[f'{session_key}_user_name']}</strong>!
                </div>
                Your Secret Santa is...<br>
                <strong style="font-size: 6rem;">{st.session_state[f'{session_key}_secret_santa']}</strong>! 🎁✨🎅
                <div style="font-size: 2rem; margin-top: 4rem;">
                    📌 <strong>Your PIN: {st.session_state[f'{session_key}_pin_generated']}</strong><br>
                    Save this PIN to check status later! 🔐
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<h1 class="title">📋 Status Check</h1>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 2rem; color: #1f2937; margin-bottom: 3rem; font-weight: 700;">Check your Secret Santa assignment using your PIN!</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Enter your name:", placeholder="Your name", key=f"status_name_{session_key}")
        with col2:
            pin = st.text_input("🔑 Enter your PIN:", placeholder="4-digit PIN", type="password", key=f"status_pin_{session_key}")
        
        if st.button("✅ Check Status", key=f"check_status_{session_key}"):
            if name and pin:
                room_data = get_room_data(room_id)
                participant_data = room_data.get('participants_data', {}).get(name, {})
                if participant_data.get('drawn', False) and participant_data.get('pin') == pin:
                    st.success("✅ Valid login!")
                    st.markdown(f"""
                    <div class="status-card">
                        <h3 style="font-size: 2.5rem; margin-bottom: 2rem;">🎅 Your Assignment:</h3>
                        <strong style="font-size: 5rem; color: #b91c1c;">{participant_data['secret_santa']}</strong>
                        <p style="font-size: 2rem;">🎁 Buy a gift for {participant_data['secret_santa']}!</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="invalid-box">
                        ❌ Invalid name or PIN combination!<br>
                        Please check and try again. 🎅
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("Please enter both name and PIN!")
        
        st.markdown("""
        <div class="status-card">
            <strong style="font-size: 1.6rem;">ℹ️ How to use:</strong><br>
            • Use the name & 4-digit PIN from your first draw<br>
            • Each person can only draw <strong>ONCE</strong><br>
            • Check status anytime before Christmas! 🎄✨
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<h1 class="title">📊 Room Statistics</h1>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size: 2rem; color: #1f2937; margin-bottom: 2rem; font-weight: 700;">Room: <strong>{room_id}</strong> | Created: {room_data.get("created", "Unknown")[:10]}</p>', unsafe_allow_html=True)
        
        participants_data = room_data.get('participants_data', {})
        drawn_count = sum(1 for data in participants_data.values() if data.get('drawn', False))
        
        col1, col2, col3 = st.columns(3)
        col1.metric("🎅 Drawn", f"{drawn_count}/{len(PARTICIPANTS)}")
        col2.metric("📋 Total Joins", len(participants_data))
        col3.metric("🎁 Progress", f"{drawn_count/len(PARTICIPANTS)*100:.0f}%")
        
        if participants_data:
            st.markdown("### Recent Activity")
            recent = sorted(participants_data.items(), 
                          key=lambda x: x[1].get('drawn_at', ''), 
                          reverse=True)[:5]
            for name, data in recent:
                status = "✅ Drawn" if data.get('drawn') else "⏳ Pending"
                pin_preview = data.get('pin', 'N/A')[:2] + "***" if data.get('pin') else "N/A"
                st.write(f"**{name}** - {status} ({pin_preview})")
        else:
            st.info("👥 No participants have joined this room yet!")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(
        page_title="🎅 Multi-Room Secret Santa",
        page_icon="🎁",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    main()
