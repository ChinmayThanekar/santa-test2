import streamlit as st
import random
import hashlib
import json
import os
from datetime import datetime

PARTICIPANTS = [
    "Alice", "Bob", "Charlie", "Diana", "Eve", 
    "Frank", "Grace", "Henry", "Ivy", "Jack"
]

# ✅ GIT-SAFE: Data folder (add to .gitignore)
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
DB_FILE = os.path.join(DATA_DIR, "secret_santa_rooms.json")

# [CSS and all functions EXACTLY SAME as before]
css = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, 
        #b91c1c 0%, #dc2626 15%, #ef4444 30%, 
        #f97316 45%, #eab308 60%, #84cc16 75%, #4ade80 100%);
    background-size: 400% 400%;
    animation: gradientShift 25s ease infinite;
    min-height: 100vh;
}

.room-input-section {
    background: rgba(255,255,255,0.98) !important;
    padding: 3rem !important;
    border-radius: 30px !important;
    margin: 2rem auto !important;
    max-width: 900px !important;
    box-shadow: 0 40px 120px rgba(0,0,0,0.5) !important;
    border: 4px solid rgba(255,255,255,0.9) !important;
}
/* [Rest of CSS unchanged] */
</style>
"""

# [All functions unchanged - load_database, save_database, etc.]
def load_database():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_database(database):
    with open(DB_FILE, 'w') as f:
        json.dump(database, f, indent=2)

def get_room_data(room_id):
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
    db = load_database()
    if room_id in db:
        db[room_id].update(data)
        save_database(db)
    return get_room_data(room_id)

# [generate_pin, create_christmas_effects, is_valid_participant - SAME]

def main():
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(create_christmas_effects(), unsafe_allow_html=True)
    
    # ✅ Room Input Section
    st.markdown('<div class="room-input-section">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #b91c1c; text-align: center; margin-bottom: 2rem;">🏠 Enter Room ID</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        room_id = st.text_input("Event/Room ID", placeholder="office2025, family-xmas", key="room_id")
    with col2:
        if st.button("➕ Join Room", key="join_room", use_container_width=True):
            if room_id.strip():
                st.session_state.selected_room = room_id.strip()
                st.rerun()
            else:
                st.error("Enter a room ID first!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
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
    
    # Load room & continue with tabs [SAME AS BEFORE]
    room_id = st.session_state.selected_room
    room_data = get_room_data(room_id)
    
    st.markdown('<div class="santa-container">', unsafe_allow_html=True)
    st.markdown(f'<h3 style="color: #b91c1c;">📍 Room: <strong>{room_id}</strong></h3>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🎅 Draw Secret Santa", "📋 Check Status", "📊 Room Stats"])
    
    # [Tab contents SAME as previous versions]
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(page_title="🎅 Secret Santa", page_icon="🎁", layout="wide")
    main()
