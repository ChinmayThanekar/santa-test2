import streamlit as st
from utils.database import get_room_data, save_database
from utils.participants import find_existing_participant, normalize_name
import json

def render_status_tab(room_id):
    st.markdown('<h1 class="title">📋 Status Check</h1>', unsafe_allow_html=True)
    
    session_key = f"room_{room_id}"
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(label="👤 Name:", placeholder="Alice", key=f"status_name_{session_key}")
    with col2:
        pin = st.text_input(label="🔑 PIN:", placeholder="1234", type="password", key=f"status_pin_{session_key}")
    
    if st.button("✅ Check Status", key=f"check_status_{session_key}"):
        _handle_status_check(name, pin, room_id)

def _handle_status_check(name, pin, room_id):
    room_data = get_room_data(room_id)
    participants_data = room_data.get('participants_data', {})
    
    st.markdown("### 🔍 **DEBUG INFO**")
    st.json(participants_data)  # SHOW EXACT DB CONTENTS
    
    existing_name, participant_data = find_existing_participant(name, participants_data)
    
    if existing_name and participant_data.get('pin') == pin:
        st.success(f"✅ LOGGED IN as '{existing_name}'")
        
        # ULTRA-SIMPLE WISHLIST
        if 'wishlist' not in participant_data:
            participant_data['wishlist'] = []
        
        st.markdown("### 📝 **Your Wishlist**")
        wishlist_json = st.text_area(
            "Edit wishlist (JSON array):",
            value=json.dumps(participant_data['wishlist'], indent=2),
            height=200
        )
        
        if st.button("💾 SAVE WISHLIST", type="primary"):
            try:
                new_wishlist = json.loads(wishlist_json)
                participant_data['wishlist'] = new_wishlist
                room_data['participants_data'][existing_name] = participant_data
                save_database(room_data)
                
                st.success(f"✅ SAVED: {new_wishlist}")
                st.balloons()
                st.rerun()
            except:
                st.error("❌ Invalid JSON!")
    else:
        st.error(f"❌ No match. Name: '{name}', Found: '{existing_name}'")

# Usage instructions
st.markdown("""
<div class="status-card">
**TEST STEPS:**
1. Draw name first (Draw tab)
2. Check this debug JSON above
3. Enter EXACT name from JSON + PIN
4. Edit wishlist as JSON array: `["Coffee", "Book"]`
</div>
""", unsafe_allow_html=True)
