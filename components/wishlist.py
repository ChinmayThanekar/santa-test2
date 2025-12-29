import streamlit as st
from utils.database import get_room_data, update_room_data
from utils.participants import get_user_wishlist, update_user_wishlist, find_existing_participant

def render_wishlist_section(name, pin, room_id, secret_santa_name):
    """Render wishlist add/view sections"""
    st.markdown("🎁 **WISHLIST FEATURES**", unsafe_allow_html=True)
    
    # Create 2-column layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 **My Wishlist**")
        _render_my_wishlist(name, pin, room_id)
    
    with col2:
        st.markdown("### 👀 **Their Wishlist**")
        _render_their_wishlist(secret_santa_name, room_id)
    
    st.markdown("---")

def _render_my_wishlist(name, pin, room_id):
    """Render form to add/edit my wishlist"""
    room_data = get_room_data(room_id)
    participants_data = room_data.get('participants_data', {})
    
    # Check if user is authenticated
    existing_name, participant_data = find_existing_participant(name, participants_data)
    if not (existing_name and participant_data.get('pin') == pin):
        st.warning("🔐 Login first to edit your wishlist!")
        return
    
    current_wishlist = get_user_wishlist(name, participants_data)
     
    # Wishlist input
    wishlist_input = st.text_area(
        "Add your gift wishlist (one item per line):",
        value="\n".join(current_wishlist),
        height=150,
        help="e.g., Coffee mug, Book, Chocolate, Scarf"
    )
    
    if st.button("💾 **Update My Wishlist**", use_container_width=True):
        new_wishlist = [item.strip() for item in wishlist_input.strip().split("\n") if item.strip()]
        if update_user_wishlist(name, new_wishlist, participants_data):
            update_room_data(room_id, {'participants_data': participants_data})
            st.success("✅ Wishlist updated!")
            st.rerun()
        else:
            st.error("❌ Failed to update wishlist!")
    
    # Display current wishlist
    if current_wishlist:
        st.markdown("**Your current wishlist:**")
        for i, item in enumerate(current_wishlist, 1):
            st.write(f"{i}. {item}")
    else:
        st.info("📭 No wishlist items yet!")
def _render_their_wishlist(secret_santa_name, room_id):
    """Render secret santa's wishlist"""
    room_data = get_room_data(room_id)
    participants_data = room_data.get('participants_data', {})
    
    their_wishlist = get_user_wishlist(secret_santa_name, participants_data)
    
    if their_wishlist:
        st.markdown(f"**{secret_santa_name}'s wishlist:** 🎁")
        for i, item in enumerate(their_wishlist, 1):
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #fef3c7, #fde68a); 
                padding: 1rem; 
                border-radius: 15px; 
                margin: 0.5rem 0; 
                border-left: 5px solid #f59e0b;
            '>
                <strong>{i}.</strong> {item}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"**{secret_santa_name}** has no wishlist yet 😅")
        st.info("They need to login and add items first!")
