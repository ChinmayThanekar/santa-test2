import streamlit as st
from components.room_input import render_room_input
from components.draw_santa import render_draw_tab
from components.check_status import render_status_tab
from components.stats_display import render_stats_tab
from utils.session import init_room_session
from config.settings import DATA_DIR
from assets.styles import load_css, create_effects

def main():
    st.set_page_config(
        page_title="🎅 Multi-Room Secret Santa",
        page_icon="🎁",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Load styles and effects
    st.markdown(load_css(), unsafe_allow_html=True)
    st.markdown(create_effects(), unsafe_allow_html=True)
    
    # Room selection
    if not render_room_input():
        st.stop()
    
    # Initialize session for selected room
    room_id = st.session_state.selected_room
    init_room_session(room_id)
    
    # Main container
    st.markdown('<div class="santa-container">', unsafe_allow_html=True)
    st.markdown(f'<h3 style="color: #b91c1c; margin-bottom: 2rem;">📍 Room: <strong>{room_id}</strong></h3>', unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🎅 Draw Secret Santa", "📋 Check Status", "📊 Room Stats"])
    with tab1:
        render_draw_tab(room_id)
    with tab2:
        render_status_tab(room_id)
    with tab3:
        render_stats_tab(room_id)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
