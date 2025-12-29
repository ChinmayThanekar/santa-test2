import streamlit as st

def init_room_session(room_id):
    """Initialize session state for specific room"""
    session_key = f"room_{room_id}"
    for key in ['revealed', 'user_name', 'pin_generated', 'secret_santa']:
        full_key = f"{session_key}_{key}"
        if full_key not in st.session_state:
            st.session_state[full_key] = False if key != 'user_name' else ""
