import random  # Add this
from datetime import datetime  # Add this
import streamlit as st
from utils.database import get_room_data, update_room_data
from utils.participants import is_valid_participant, generate_pin, get_other_participants,find_existing_participant
from config.participants import PARTICIPANTS
 
def render_draw_tab(room_id):
    """Render Draw Secret Santa tab"""
    st.markdown('<h1 class="title">🎅 Secret Santa 🎁</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 2rem; color: #1f2937; margin-bottom: 3rem; font-weight: 700;">Ho Ho Ho! Enter your name to discover who drew YOU!</p>', unsafe_allow_html=True)
    
    # Valid participants list
    st.markdown(f"""
    <div style="background: linear-gradient(145deg, #16a34a, #15803d); padding: 3.5rem; border-radius: 35px; margin: 3.5rem 0; color: #ffffff; font-size: 1.6rem; border: 5px solid rgba(255,255,255,0.9); box-shadow: 0 40px 100px rgba(22,163,74,0.6); font-weight: 700;">
        <strong>🎄 Valid Participants:</strong><br>
        <span style="font-size: 1.8rem;">{', '.join(PARTICIPANTS)}</span> 🎄
    </div>
    """, unsafe_allow_html=True)
    
    session_key = f"room_{room_id}"
    name = st.text_input("", placeholder="👤 Enter your name here...", key=f"name_input_{session_key}")
    
    if st.button("🎊 REVEAL MY SECRET SANTA 🎊", key=f"reveal_btn_{session_key}"):
        _handle_draw(name, room_id, session_key)
    
    if st.session_state.get(f'{session_key}_revealed', False):
        _show_reveal(session_key)

def _handle_draw(name, room_id, session_key):
    """Handle secret santa draw logic (CASE-INSENSITIVE)"""
    if not name.strip():
        st.error("🎄 Please enter your name first!")
        return
    
    if not is_valid_participant(name):
        st.markdown(f"""
        <div class="invalid-box">
            ❌ <strong>{name}</strong> is not a valid participant!<br>
            🎅 Please check the list above and try again! 🎅
        </div>
        """, unsafe_allow_html=True)
        return
    
    room_data = get_room_data(room_id)
    participants_data = room_data.get('participants_data', {})
    
    # 🔍 CASE-INSENSITIVE CHECK: Find existing participant
    existing_name, existing_data = find_existing_participant(name, participants_data)
    
    if existing_name and existing_data.get('drawn', False):
        st.markdown(f"""
        <div class="invalid-box">
            ❌ <strong>{name}</strong> (aka <strong>{existing_name}</strong>) has already drawn!<br>
            Go to <strong>Check Status</strong> tab with your PIN! 🎅
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Draw secret santa (use original casing for display)
    other_names = get_other_participants(name)
    secret_santa = random.choice(other_names)
    pin = generate_pin(name)
    
    # Store with ORIGINAL casing but check case-insensitively
    display_name = name.strip()  # Keep user's original casing
    participants_data[display_name] = {
    'secret_santa': secret_santa,
    'pin': pin,
    'drawn': True,
    'drawn_at': datetime.now().isoformat(),
    'wishlist': []  # 🆕 WISHLIST INITIALIZED!
}
    
    update_room_data(room_id, {'participants_data': participants_data})
    
    # Update session state
    st.session_state[f'{session_key}_user_name'] = display_name
    st.session_state[f'{session_key}_secret_santa'] = secret_santa
    st.session_state[f'{session_key}_pin_generated'] = pin
    st.session_state[f'{session_key}_revealed'] = True
    st.rerun()

def _show_reveal(session_key):
    """Show secret santa reveal animation"""
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
