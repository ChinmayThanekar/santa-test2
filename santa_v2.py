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

# Database file - stores room data
DB_FILE = "secret_santa_rooms.json"

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

# [Rest of CSS remains exactly the same - omitted for brevity]
css = """
# [Previous CSS code - no changes needed]
"""

def generate_pin(name):
    seed = f"{name}{random.randint(1000, 9999)}"
    return str(int(hashlib.md5(seed.encode()).hexdigest(), 16) % 10000).zfill(4)

def create_christmas_effects():
    # [Previous function - no changes]
    effects_html = ""
    light_positions = [
        ("3%", "3%", "#b91c1c"), ("97%", "3%", "#4ade80"),
        ("3%", "97%", "#dc2626"), ("97%", "97%", "#84cc16"),
        ("50%", "1%", "#eab308"), ("1%", "50%", "#ef4444"),
        ("99%", "50%", "#16a34a"), ("50%", "99%", "#b91c1c")
    ]
    
    for top, left, color in light_positions:
        effects_html += f"""
        <div class="light" style="
            --top: {top}; --left: {left};
            width: 50px; height: 50px;
            background: {color};
            animation-duration: {random.uniform(1.8, 4.2)}s;
        "></div>
        """
    
    for i in range(150):
        effects_html += f"""
        <div class="snowflake" style="
            left: {random.randint(0, 100)}vw;
            animation-delay: {random.uniform(0, 15)}s;
            animation-duration: {random.uniform(30, 60)}s;
            font-size: {random.choice(['2.5rem', '3rem', '3.5rem', '2.2rem'])};
        ">❄️</div>
        """
    return effects_html

def is_valid_participant(name, participants):
    return name.strip().lower() in [p.lower() for p in participants]

def main():
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(create_christmas_effects(), unsafe_allow_html=True)
    
    # Room selection/input
    st.markdown('<div class="santa-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        room_id = st.text_input("🏠 Enter Room/Event ID:", placeholder="e.g., office2025, family-xmas", key="room_id")
    with col2:
        create_room = st.button("➕ Create New Room", key="create_room")
    
    if create_room:
        if room_id.strip():
            room_data = get_room_data(room_id.strip())
            st.success(f"✅ Room '{room_id}' created/loaded!")
            st.rerun()
        else:
            st.error("Please enter a room ID!")
    
    if not room_id.strip():
        st.markdown("""
        <div class="status-card">
            <h3>🎅 Welcome to Multi-Room Secret Santa! 🎁</h3>
            <p>Enter a unique Room ID for your event (office party, family gathering, etc.)</p>
            <p><strong>Room data persists across sessions!</strong></p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()
    
    room_data = get_room_data(room_id.strip())
    
    # Initialize session state for current room
    session_key = f"room_{room_id.strip()}"
    for key in ['revealed', 'user_name', 'invalid_shown']:
        if session_key not in st.session_state:
            st.session_state[session_key] = False if key != 'user_name' else ""
    
    tab1, tab2, tab3 = st.tabs(["🎅 Draw Secret Santa", "📋 Check Status", "📊 Room Stats"])
    
    with tab1:
        st.markdown('<h1 class="title">🎅 Secret Santa</h1>', unsafe_allow_html=True)
        st.markdown(f'<p class="subtitle">Room: <strong>{room_id}</strong> | {room_data.get("event_name", "Secret Santa")}</p>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="valid-names">
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
                        
                        update_room_data(room_id.strip(), {'participants_data': participants_data})
                        
                        st.session_state[f'{session_key}_user_name'] = name.strip()
                        st.session_state[f'{session_key}_revealed'] = True
                        st.session_state[f'{session_key}_pin_generated'] = pin
                        st.session_state[f'{session_key}_secret_santa'] = secret_santa
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
        st.markdown(f'<p class="subtitle">Room: <strong>{room_id}</strong></p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Enter your name:", placeholder="Your name", key=f"status_name_{session_key}")
        with col2:
            pin = st.text_input("🔑 Enter your PIN:", placeholder="4-digit PIN", type="password", key=f"status_pin_{session_key}")
        
        if st.button("✅ Check Status", key=f"check_status_{session_key}"):
            if name and pin:
                room_data = get_room_data(room_id.strip())
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
    
    with tab3:
        st.markdown('<h1 class="title">📊 Room Statistics</h1>', unsafe_allow_html=True)
        st.markdown(f'<p class="subtitle">Room: <strong>{room_id}</strong> | Created: {room_data.get("created", "Unknown")[:10]}</p>', unsafe_allow_html=True)
        
        participants_data = room_data.get('participants_data', {})
        drawn_count = sum(1 for data in participants_data.values() if data.get('drawn', False))
        total_participants = len(participants_data)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("🎅 Drawn", f"{drawn_count}/{len(PARTICIPANTS)}")
        col2.metric("📋 Total Joins", total_participants)
        col3.metric("🎁 Ready", f"{drawn_count}/{len(PARTICIPANTS)}")
        
        if participants_data:
            st.markdown("### Recent Activity")
            recent = sorted(participants_data.items(), 
                          key=lambda x: x[1].get('drawn_at', ''), 
                          reverse=True)[:5]
            for name, data in recent:
                status = "✅ Drawn" if data.get('drawn') else "⏳ Pending"
                st.write(f"**{name}** - {status} ({data.get('pin', 'N/A')[:2]}***)")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(
        page_title="🎅 Multi-Room Secret Santa",
        page_icon="🎁",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    main()
