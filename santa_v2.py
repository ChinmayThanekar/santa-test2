import streamlit as st
import random
from streamlit.components.v1 import html

# Secret Santa participants (you can customize this list)
PARTICIPANTS = [
    "Alice", "Bob", "Charlie", "Diana", "Eve", 
    "Frank", "Grace", "Henry", "Ivy", "Jack"
]

# Christmas Santa Theme CSS with animated background
css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&display=swap');
    
    /* Santa Christmas Background */
    .main {
        background: 
            radial-gradient(circle at 20% 80%, rgba(255,107,107,0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255,202,87,0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(72,219,251,0.2) 0%, transparent 50%),
            linear-gradient(135deg, #2c3e50 0%, #1a252f 50%, #34495e 100%);
        min-height: 100vh;
        font-family: 'Poppins', sans-serif;
        position: relative;
        overflow: hidden;
    }
    
    /* Santa Hat Pattern Background */
    .santa-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0.05;
        z-index: 1;
        pointer-events: none;
    }
    
    /* Christmas Lights Animation */
    .light {
        position: fixed;
        border-radius: 50%;
        animation: twinkle 2s ease-in-out infinite;
        box-shadow: 0 0 20px currentColor;
        z-index: 2;
    }
    
    .light:nth-child(odd) { animation-delay: 0s; }
    .light:nth-child(even) { animation-delay: 1s; }
    
    @keyframes twinkle {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.2); }
    }
    
    .santa-container {
        max-width: 600px;
        margin: 0 auto;
        padding: 2rem;
        text-align: center;
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(15px);
        border: 2px solid rgba(255,255,255,0.2);
        border-radius: 25px;
        box-shadow: 
            0 25px 50px rgba(0,0,0,0.3),
            inset 0 1px 0 rgba(255,255,255,0.4);
        position: relative;
        z-index: 10;
        overflow: hidden;
    }
    
    .santa-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, 
            #ff6b6b, #feca57, #48dbfb, #ff9ff3, #ff6b6b);
        border-radius: 25px 25px 0 0;
    }
    
    .title {
        font-size: 3.5rem;
        font-family: 'Dancing Script', cursive;
        background: linear-gradient(45deg, #ff6b6b, #feca57, #ff9ff3, #48dbfb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        text-shadow: 0 0 30px rgba(255,255,255,0.5);
        animation: titleBounce 3s ease-in-out infinite;
    }
    
    @keyframes titleBounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    .subtitle {
        font-size: 1.4rem;
        color: #f8f9fa;
        margin-bottom: 2rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }
    
    .name-input {
        width: 100%;
        padding: 1.2rem;
        font-size: 1.6rem;
        border: 3px solid rgba(255,255,255,0.3);
        border-radius: 20px;
        background: rgba(255,255,255,0.95);
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.2),
            inset 0 1px 0 rgba(255,255,255,0.8);
        text-align: center;
        margin-bottom: 2rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .name-input:focus {
        border-color: #ff6b6b;
        box-shadow: 
            0 20px 45px rgba(255,107,107,0.3),
            inset 0 1px 0 rgba(255,255,255,0.9);
        transform: scale(1.02);
    }
    
    .reveal-btn {
        background: linear-gradient(45deg, #ff4757, #ff6b6b, #ff8e8e);
        border: none;
        padding: 1.4rem 3.5rem;
        font-size: 1.4rem;
        font-weight: 700;
        border-radius: 50px;
        color: white;
        cursor: pointer;
        box-shadow: 
            0 20px 40px rgba(255,71,87,0.4),
            inset 0 1px 0 rgba(255,255,255,0.3);
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        font-family: 'Poppins', sans-serif;
        position: relative;
        overflow: hidden;
    }
    
    .reveal-btn:hover {
        transform: translateY(-8px);
        box-shadow: 
            0 30px 60px rgba(255,71,87,0.6),
            inset 0 1px 0 rgba(255,255,255,0.4);
    }
    
    /* Reveal Animation */
    .reveal-box {
        background: linear-gradient(45deg, #ff9ff3, #feca57, #54a0ff);
        padding: 3.5rem 2rem;
        border-radius: 30px;
        margin: 2.5rem 0;
        min-height: 220px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 2.8rem;
        font-weight: 700;
        color: #1a1a2e;
        text-shadow: 2px 2px 4px rgba(255,255,255,0.5);
        box-shadow: 
            0 30px 60px rgba(0,0,0,0.3),
            inset 0 1px 0 rgba(255,255,255,0.6);
        opacity: 0;
        transform: scale(0.3) rotateX(90deg);
        animation: revealAnim 2.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
        position: relative;
        overflow: hidden;
    }
    
    .reveal-box::before {
        content: '🎁✨';
        position: absolute;
        font-size: 4rem;
        top: 10px;
        left: 50%;
        transform: translateX(-50%);
        animation: giftBounce 1s ease-in-out 1s both;
    }
    
    @keyframes giftBounce {
        0%, 60%, 100% { transform: translateX(-50%) translateY(0); }
        30%, 70% { transform: translateX(-50%) translateY(-20px); }
    }
    
    @keyframes revealAnim {
        0% { opacity: 0; transform: scale(0.3) rotateX(90deg); }
        50% { opacity: 0.8; transform: scale(1.05) rotateX(0deg); }
        100% { opacity: 1; transform: scale(1) rotateX(0deg); }
    }
    
    /* Invalid Participant Styling */
    .invalid-box {
        background: linear-gradient(45deg, #ff3838, #ff4757);
        padding: 2.5rem;
        border-radius: 25px;
        margin: 2rem 0;
        color: white;
        font-size: 1.6rem;
        font-weight: 700;
        box-shadow: 0 20px 45px rgba(255,56,56,0.4);
        animation: shake 0.6s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
        text-align: center;
        border: 3px solid rgba(255,255,255,0.3);
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0) rotate(0deg); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-12px) rotate(-2deg); }
        20%, 40%, 60%, 80% { transform: translateX(12px) rotate(2deg); }
    }
    
    .valid-names {
        background: rgba(76,175,80,0.2);
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        color: #e8f5e8;
        font-size: 1rem;
        border: 1px solid rgba(76,175,80,0.4);
    }
    
    /* Enhanced Snowflakes */
    .snowflake {
        color: #fff;
        font-size: 1.8rem;
        position: fixed;
        top: -30px;
        animation: fall linear infinite;
        pointer-events: none;
        z-index: 5;
        text-shadow: 0 0 10px rgba(255,255,255,0.8);
    }
    
    @keyframes fall {
        to {
            transform: translateY(110vh) rotate(720deg);
        }
    }
</style>
"""

def create_christmas_effects():
    """Create Christmas lights and snowflakes"""
    effects_html = ""
    
    # Christmas lights around the screen
    light_positions = [
        ("10%", "10%", "#ff6b6b"), ("90%", "10%", "#feca57"),
        ("10%", "90%", "#48dbfb"), ("90%", "90%", "#ff9ff3"),
        ("50%", "5%", "#ff4757"), ("5%", "50%", "#54a0ff"),
        ("95%", "50%", "#00d2d3"), ("50%", "95%", "#ff3838")
    ]
    
    for i, (top, left, color) in enumerate(light_positions):
        size = "25px" if i < 4 else "20px"
        effects_html += f"""
        <div class="light" style="
            width: {size}; height: {size};
            top: {top}; left: {left};
            background: {color};
            animation-duration: {random.uniform(1.5, 3)}s;
        "></div>
        """
    
    # Snowflakes
    for i in range(60):
        left = f"{random.randint(0, 100)}vw"
        delay = f"{random.randint(0, 30)}s"
        duration = f"{random.uniform(12, 25)}s"
        size = random.choice(["1.2rem", "1.8rem", "2.2rem"])
        rotation = random.choice(["rotate(0deg)", "rotate(45deg)", "rotate(90deg)"])
        effects_html += f"""
        <div class="snowflake" style="
            left: {left};
            animation-delay: {delay};
            animation-duration: {duration};
            font-size: {size};
            animation-timing-function: {rotation};
        ">❄️</div>
        """
    
    return effects_html

def is_valid_participant(name, participants):
    """Check if name exists in participants list (case-insensitive)"""
    return name.strip().lower() in [p.lower() for p in participants]

def main():
    st.markdown(css, unsafe_allow_html=True)
    
    # Add Christmas effects
    st.markdown(create_christmas_effects(), unsafe_allow_html=True)
    
    # Session state initialization
    if 'revealed' not in st.session_state:
        st.session_state.revealed = False
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    if 'invalid_shown' not in st.session_state:
        st.session_state.invalid_shown = False
    
    container = st.container()
    
    with container:
        st.markdown('<div class="santa-container">', unsafe_allow_html=True)
        
        if not st.session_state.revealed:
            st.markdown('<h1 class="title">🎅 Secret Santa 🎁</h1>', unsafe_allow_html=True)
            st.markdown('<p class="subtitle">Ho Ho Ho! Enter your name to discover your Secret Santa!</p>', unsafe_allow_html=True)
            
            # Show valid participants
            st.markdown("""
            <div class="valid-names">
                <strong>🎄 Valid Participants:</strong> """ + ", ".join(PARTICIPANTS) + """ 🎄
            </div>
            """, unsafe_allow_html=True)
            
            name = st.text_input("", 
                               placeholder="👤 Enter your name here...",
                               key="name_input",
                               help="Type your name exactly as listed above!")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if st.button("🎊 REVEAL MY SECRET SANTA 🎊", key="reveal_btn"):
                    if name.strip():
                        if is_valid_participant(name, PARTICIPANTS):
                            st.session_state.user_name = name.strip()
                            st.session_state.invalid_shown = False
                            
                            # Find secret santa
                            other_names = [n for n in PARTICIPANTS if n.lower() != name.lower()]
                            secret_santa = random.choice(other_names)
                            st.session_state.secret_santa = secret_santa
                            st.session_state.revealed = True
                            st.rerun()
                        else:
                            st.session_state.invalid_shown = True
                            st.session_state.user_name = name.strip()
                            st.rerun()
                    else:
                        st.error("Please enter your name first! 🎄")
            
            # Show invalid participant message
            if st.session_state.invalid_shown and st.session_state.user_name:
                st.markdown(f"""
                <div class="invalid-box">
                    ❌ <strong>{st.session_state.user_name}</strong> is not a valid participant! <br>
                    🎅 Please check the list above and try again! 🎅
                </div>
                """, unsafe_allow_html=True)
                
        else:
            # Reveal animation
            st.markdown(f"""
            <div class="reveal-box">
                <div style="font-size: 1.2rem; margin-bottom: 1rem;">Hey <strong>{st.session_state.user_name}</strong>,</div>
                Your Secret Santa is... <br><strong style="color: #1a1a2e; font-size: 3rem;">{st.session_state.secret_santa}</strong>! 🎁✨
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<p class="subtitle" style="margin-top: 2rem;">Spread some holiday magic! 🎅❄️</p>', unsafe_allow_html=True)
            
            if st.button("🔄 Try Another Name", key="reset_btn"):
                st.session_state.revealed = False
                st.session_state.user_name = ""
                st.session_state.secret_santa = None
                st.session_state.invalid_shown = False
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Secret Santa 🎅",
        page_icon="🎅",
        layout="wide"
    )
    main()
