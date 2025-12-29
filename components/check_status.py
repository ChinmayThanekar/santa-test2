import streamlit as st
from utils.database import get_room_data
from utils.participants import is_valid_participant
from datetime import datetime

def render_status_tab(room_id):
    """Render Check Status tab"""
    st.markdown('<h1 class="title">📋 Status Check</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 2rem; color: #1f2937; margin-bottom: 3rem; font-weight: 700;">Check your Secret Santa assignment using your PIN!</p>', unsafe_allow_html=True)
    
    session_key = f"room_{room_id}"
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("👤 Enter your name:", placeholder="Your name", key=f"status_name_{session_key}")
    with col2:
        pin = st.text_input("🔑 Enter your PIN:", placeholder="4-digit PIN", type="password", key=f"status_pin_{session_key}")
    
    if st.button("✅ Check Status", key=f"check_status_{session_key}"):
        _handle_status_check(name, pin, room_id)
    
    st.markdown("""
    <div class="status-card">
        <strong style="font-size: 1.6rem;">ℹ️ How to use:</strong><br>
        • Use the name & 4-digit PIN from your first draw<br>
        • Each person can only draw <strong>ONCE</strong><br>
        • Check status anytime before Christmas! 🎄✨
    </div>
    """, unsafe_allow_html=True)

def _handle_status_check(name, pin, room_id):
    """Handle status check logic"""
    if not name or not pin:
        st.error("Please enter both name and PIN!")
        return
    
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
