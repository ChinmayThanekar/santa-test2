import streamlit as st

def render_room_input():
    """Render room input section and return True if room selected"""
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
    
    # Show welcome message if no room selected
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
        return False
    
    return True
