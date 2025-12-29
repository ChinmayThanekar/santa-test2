import streamlit as st
from utils.database import get_room_data
from utils.participants import find_existing_participant
from components.wishlist import render_wishlist_section
from datetime import datetime

def render_status_tab(room_id):
    """Render Check Status tab with Wishlist features"""
    st.markdown('<h1 class="title">📋 Status Check</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 2rem; color: #1f2937; margin-bottom: 3rem; font-weight: 700;">Check your Secret Santa + Manage Wishlists! 🎁</p>', unsafe_allow_html=True)
    
    session_key = f"room_{room_id}"
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("👤 Enter your name:", placeholder="Your name", key=f"status_name_{session_key}")
    with col2:
        pin = st.text_input("🔑 Enter your PIN:", placeholder="4-digit PIN", type="password", key=f"status_pin_{session_key}")
    
    if st.button("✅ **Check Status & Wishlist**", key=f"check_status_{session_key}"):
        _handle_status_check(name, pin, room_id)
    
    st.markdown("""
    <div class="status-card">
        <strong style="font-size: 1.6rem;">ℹ️ How to use:</strong><br>
        • Use name & PIN from your draw<br>
        • Add your wishlist for your Secret Santa<br>
        • See your giftee's wishlist instantly! 🎄✨
    </div>
    """, unsafe_allow_html=True)

def _handle_status_check(name, pin, room_id):
    """Handle status check + show wishlists"""
    if not name or not pin:
        st.error("Please enter both name and PIN!")
        return
    
    room_data = get_room_data(room_id)
    participants_data = room_data.get('participants_data', {})
    
    # Case-insensitive search
    existing_name, participant_data = find_existing_participant(name, participants_data)
    
    if existing_name and participant_data.get('drawn', False) and participant_data.get('pin') == pin:
        secret_santa_name = participant_data['secret_santa']
        st.success("✅ Valid login!")
        
        # Show assignment
        st.markdown(f"""
        <div class="status-card">
            <h3 style="font-size: 2.5rem; margin-bottom: 2rem;">🎅 Your Assignment:</h3>
            <strong style="font-size: 5rem; color: #b91c1c;">{secret_santa_name}</strong>
            <p style="font-size: 2rem;">🎁 Buy a gift for {secret_santa_name}!</p>
            <p style="font-size: 1.4rem; margin-top: 1rem;">(Logged in as: <strong>{existing_name}</strong>)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 🎁 NEW: Show wishlist sections
        render_wishlist_section(name, pin, room_id, secret_santa_name)
        
    else:
        st.markdown("""
        <div class="invalid-box">
            ❌ Invalid name or PIN combination!<br>
            <strong>Names are case-insensitive:</strong> "Alice" = "alice"<br>
            Please check and try again. 🎅
        </div>
        """, unsafe_allow_html=True)
