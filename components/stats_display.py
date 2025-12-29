import streamlit as st
from utils.database import get_room_data
from config.participants import PARTICIPANTS

def render_stats_tab(room_id):
    """Render Room Statistics tab"""
    st.markdown('<h1 class="title">📊 Room Statistics</h1>', unsafe_allow_html=True)
    room_data = get_room_data(room_id)
    st.markdown(f'<p style="font-size: 2rem; color: #1f2937; margin-bottom: 2rem; font-weight: 700;">Room: <strong>{room_id}</strong> | Created: {room_data.get("created", "Unknown")[:10]}</p>', unsafe_allow_html=True)
    
    participants_data = room_data.get('participants_data', {})
    drawn_count = sum(1 for data in participants_data.values() if data.get('drawn', False))
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🎅 Drawn", f"{drawn_count}/{len(PARTICIPANTS)}")
    col2.metric("📋 Total Joins", len(participants_data))
    col3.metric("🎁 Progress", f"{drawn_count/len(PARTICIPANTS)*100:.0f}%")
    
    if participants_data:
        st.markdown("### Recent Activity")
        recent = sorted(participants_data.items(), 
                      key=lambda x: x[1].get('drawn_at', ''), 
                      reverse=True)[:5]
        for name, data in recent:
            status = "✅ Drawn" if data.get('drawn') else "⏳ Pending"
            pin_preview = data.get('pin', 'N/A')[:2] + "***" if data.get('pin') else "N/A"
            st.write(f"**{name}** - {status} ({pin_preview})")
    else:
        st.info("👥 No participants have joined this room yet!")
