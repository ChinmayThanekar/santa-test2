import streamlit as st
from utils.database import get_room_data, update_room_data
from utils.participants import find_existing_participant, get_user_wishlist
from datetime import datetime

def render_status_tab(room_id):
    st.markdown('<h1 class="title">📋 Status Check</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 2rem; color: #1f2937; margin-bottom: 3rem; font-weight: 700;">Check your Secret Santa + Manage Wishlists! 🎁</p>', unsafe_allow_html=True)
    
    session_key = f"room_{room_id}"
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(label="👤 Enter your name:", placeholder="Your name", key=f"status_name_{session_key}")
    with col2:
        pin = st.text_input(label="🔑 Enter your PIN:", placeholder="4-digit PIN", type="password", key=f"status_pin_{session_key}")
    
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
    if not name or not pin:
        st.error("Please enter both name and PIN!")
        return
    
    room_data = get_room_data(room_id)
    participants_data = room_data.get('participants_data', {})
    
    existing_name, participant_data = find_existing_participant(name, participants_data)
    
    if existing_name and participant_data.get('drawn', False) and participant_data.get('pin') == pin:
        secret_santa_name = participant_data['secret_santa']
        st.success("✅ Valid login!")
        
        st.markdown(f"""
        <div class="status-card">
            <h3 style="font-size: 2.5rem; margin-bottom: 2rem;">🎅 Your Assignment:</h3>
            <strong style="font-size: 5rem; color: #b91c1c;">{secret_santa_name}</strong>
            <p style="font-size: 2rem;">🎁 Buy a gift for {secret_santa_name}!</p>
            <p style="font-size: 1.4rem; margin-top: 1rem;">(Logged in as: <strong>{existing_name}</strong>)</p>
        </div>
        """, unsafe_allow_html=True)
        
        _render_wishlist_sections(name, pin, room_id, secret_santa_name, existing_name)
    else:
        st.markdown("""
        <div class="invalid-box">
            ❌ Invalid name or PIN combination!<br>
            <strong>Names are case-insensitive:</strong> "Alice" = "alice"<br>
            Please check and try again. 🎅
        </div>
        """, unsafe_allow_html=True)

def _render_wishlist_sections(name, pin, room_id, secret_santa_name, existing_name):
    st.markdown("🎁 **WISHLIST FEATURES**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 **My Wishlist**")
        _render_my_wishlist(name, pin, room_id, existing_name)
    with col2:
        st.markdown("### 👀 **Their Wishlist**")
        _render_their_wishlist(secret_santa_name, room_id)

def _render_my_wishlist(name, pin, room_id, existing_name):
    """🆕 SIMPLIFIED: NO SESSION STATE, DIRECT DB"""
    
    # DEBUG: Show current DB state
    room_data = get_room_data(room_id)
    current_db_wishlist = room_data['participants_data'].get(existing_name, {}).get('wishlist', [])
    st.caption(f"🔍 DEBUG: DB has {len(current_db_wishlist)} items for {existing_name}")
    
    # Show current wishlist from DB
    if current_db_wishlist:
        st.markdown("**✅ Current wishlist:**")
        for i, item in enumerate(current_db_wishlist, 1):
            st.success(f"{i}. {item}")
    else:
        st.info("📭 No wishlist items yet!")
    
    # SIMPLE TEXT AREA - NO SESSION STATE
    wishlist_input = st.text_area(
        label="🎁 Add wishlist items (one per line):",
        height=120,
        placeholder="Coffee mug\nBook\nChocolate\nScarf",
        key=f"wl_input_{room_id}_{existing_name}_{hash(name+pin)}"  # Unique key
    )
    
    # 🆕 SAVE BUTTON - IMMEDIATE DB UPDATE
    if st.button(f"💾 **SAVE {len(wishlist_input.strip().splitlines())} items**", type="primary"):
        # Parse new wishlist
        new_items = [item.strip() for item in wishlist_input.strip().splitlines() if item.strip()]
        
        # 🆕 DIRECT DB WRITE - NO COPIES
        room_data = get_room_data(room_id)
        room_data['participants_data'][existing_name]['wishlist'] = new_items
        
        # 🆕 FORCE SAVE
        from utils.database import save_database
        save_database(room_data)
        
        st.balloons()
        st.success(f"✅ SAVED {len(new_items)} items to DATABASE!")
        
        # 🆕 RELOAD TO SHOW UPDATE
        room_data = get_room_data(room_id)
        updated_wishlist = room_data['participants_data'][existing_name]['wishlist']
        st.markdown(f"**🔥 UPDATED DB:** {len(updated_wishlist)} items")
        for i, item in enumerate(updated_wishlist, 1):
            st.success(f"{i}. {item}")

def _render_their_wishlist(secret_santa_name, room_id):
    room_data = get_room_data(room_id)
    participants_data = room_data['participants_data']
    
    # Find their data (case-insensitive)
    for stored_name, data in participants_data.items():
        if stored_name.lower() == secret_santa_name.lower():
            their_wishlist = data.get('wishlist', [])
            break
    else:
        their_wishlist = []
    
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
        st.markdown(f"**{secret_santa_name}** has no wishlist yet")
