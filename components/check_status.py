import streamlit as st
from utils.database import get_room_data, save_database
from utils.participants import find_existing_participant, get_user_wishlist, normalize_name
from datetime import datetime

def render_status_tab(room_id):
    """Render Check Status tab with Wishlist features"""
    st.markdown('<h1 class="title">📋 Status Check</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 2rem; color: #1f2937; margin-bottom: 3rem; font-weight: 700;">Check your Secret Santa + Manage Wishlists! 🎁</p>', unsafe_allow_html=True)
    
    session_key = f"room_{room_id}"
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(
            label="👤 Enter your name:", 
            placeholder="Your name", 
            key=f"status_name_{session_key}"
        )
    with col2:
        pin = st.text_input(
            label="🔑 Enter your PIN:", 
            placeholder="4-digit PIN", 
            type="password", 
            key=f"status_pin_{session_key}"
        )
    
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
        
        # 🎁 FIXED: Inline wishlist sections with persistence
        _render_wishlist_sections(existing_name, pin, room_id, secret_santa_name)
        
    else:
        st.markdown("""
        <div class="invalid-box">
            ❌ Invalid name or PIN combination!<br>
            <strong>Names are case-insensitive:</strong> "Alice" = "alice"<br>
            Please check and try again. 🎅
        </div>
        """, unsafe_allow_html=True)

def _render_wishlist_sections(existing_name, pin, room_id, secret_santa_name):
    """🆕 INLINE WISHLIST - NO EXTERNAL MODULE NEEDED"""
    st.markdown("🎁 **WISHLIST FEATURES**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 **My Wishlist**")
        _render_my_wishlist(existing_name, pin, room_id)
    
    with col2:
        st.markdown("### 👀 **Their Wishlist**")
        _render_their_wishlist(secret_santa_name, room_id)

def _render_my_wishlist(existing_name, pin, room_id):
    """🆕 FIXED PERSISTENT WISHLIST"""
    room_data = get_room_data(room_id)
    current_wishlist = room_data['participants_data'].get(existing_name, {}).get('wishlist', [])
    
    st.markdown(f"**Current: {len(current_wishlist)} items**")
    if current_wishlist:
        for i, item in enumerate(current_wishlist, 1):
            st.success(f"{i}. {item}")
    else:
        st.info("📭 No items yet!")
    
    wishlist_input = st.text_area(
        label="Add wishlist (one per line):",
        value="\n".join(current_wishlist),
        height=120,
        placeholder="Coffee mug\nBook\nChocolates"
    )
    
    if st.button("💾 **SAVE WISHLIST**", type="primary", use_container_width=True):
        new_items = [item.strip() for item in wishlist_input.strip().split("\n") if item.strip()]
        
        # 🆕 DIRECT DB UPDATE
        room_data = get_room_data(room_id)
        room_data['participants_data'][existing_name]['wishlist'] = new_items
        save_database(room_data)
        
        st.success(f"✅ SAVED {len(new_items)} items!")
        st.balloons()
        st.rerun()

def _render_their_wishlist(secret_santa_name, room_id):
    """Show Secret Santa's wishlist"""
    room_data = get_room_data(room_id)
    participants_data = room_data['participants_data']
    
    their_wishlist = get_user_wishlist(secret_santa_name, participants_data)
    
    if their_wishlist:
        st.markdown(f"**{secret_santa_name}'s wishlist:** 🎁")
        for i, item in enumerate(their_wishlist, 1):
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #fef3c7, #fde68a); 
                padding: 1.2rem; border-radius: 15px; margin: 0.5rem 0; 
                border-left: 5px solid #f59e0b;
            '>
                <strong style='color: #b45309;'>{i}.</strong> {item}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info(f"{secret_santa_name} has no wishlist yet!")
