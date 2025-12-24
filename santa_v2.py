import streamlit as st
import random
from streamlit.components.v1 import html

# Secret Santa participants (you can customize this list)
PARTICIPANTS = [
    "Alice", "Bob", "Charlie", "Diana", "Eve", 
    "Frank", "Grace", "Henry", "Ivy", "Jack"
]

# Fixed Christmas Theme CSS - Forces proper background & readability
css = """
<style>
    /* Force full override of Streamlit default styles */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, 
            #1a1a2e 0%, 
            #16213e 25%, 
            #0f0f23 50%, 
            #1a1a2e 75%, 
            #2d1b69 100%);
        background-size: 300% 300%;
        animation: gradientShift 20s ease infinite;
        min-height: 100vh;
        position: relative;
    }
    
    [data-testid="stAppViewContainer"] > div > div > div {
        background: transparent !important;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 100%;
        background: transparent !important;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Dancing+Script:wght@700&display=swap');
    
    /* Christmas Lights */
    .light {
        position: fixed;
        border-radius: 50%;
        animation: twinkle 2s ease-in-out infinite;
        box-shadow: 0 0 30px currentColor;
        z-index: 999;
        top: var(--top);
        left: var(--left);
    }
    
    @keyframes twinkle {
        0%, 100% { opacity: 0.4; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.4); }
    }
    
    /* Main Santa Container */
    .santa-container {
        max-width: 700px;
        margin: 2rem auto;
        padding: 3rem;
        text-align: center;
        background: linear-gradient(145deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));
        backdrop-filter: blur(25px);
        border: 2px solid rgba(255,255,255,0.2);
        border-radius: 30px;
        box-shadow: 
            0 35px 80px rgba(0,0,0,0.5),
            inset 0 1px 0 rgba(255,255,255,0.3);
        position: relative;
        z-index: 1000;
    }
    
    .santa-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 8px;
        background: linear-gradient(90deg, 
            #dc2626, #ff6b35, #ffd23f, #51cf66, #16a34a, #dc2626);
        border-radius: 30px 30px 0 0;
        box-shadow: 0 2px 15px rgba(220,38,38,0.5);
    }
    
    /* Title */
    .title {
        font-size: 4rem;
        font-family: 'Dancing Script', cursive;
        background: linear-gradient(45deg, #ffffff, #f8fafc, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.5rem;
        text-shadow: 0 0 40px rgba(255,255,255,0.8);
        animation: titleGlow 4s ease-in-out infinite;
        letter-spacing: 2px;
    }
    
    @keyframes titleGlow {
        0%, 100% { text-shadow: 0 0 40px rgba(255,255,255,0.8), 0 0 60px rgba(255,255,255,0.4); }
        50% { text-shadow: 0 0 60px rgba(255,255,255,1), 0 0 100px rgba(255,255,255,0.6); }
    }
    
    .subtitle {
        font-size: 1.6rem;
        color: #f8fafc;
        margin-bottom: 2.5rem;
        text-shadow: 0 3px 15px rgba(0,0,0,0.7);
        font-weight: 500;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Name Input */
    .name-input {
        width: 100%;
        padding: 1.5rem 2rem;
        font-size: 1.8rem;
        border: 3px solid rgba(255,255,255,0.4);
        border-radius: 25px;
        background: rgba(255,255,255,0.95) !important;
        box-shadow: 
            0 25px 50px rgba(0,0,0,0.3),
            inset 0 2px 10px rgba(255,255,255,0.8);
        text-align: center;
        margin-bottom: 3rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        transition: all 0.4s ease;
        color: #1e293b;
    }
    
    .name-input:focus {
        border-color: #fefce8 !important;
        box-shadow: 
            0 30px 60px rgba(254,252,232,0.4),
            inset 0 2px 15px rgba(255,255,255,1);
        transform: scale(1.02);
    }
    
    /* Reveal Button */
    .reveal-btn {
        background: linear-gradient(45deg, #dc2626, #ff6b35, #ffd23f);
        border: none;
        padding: 1.6rem 4rem;
        font-size: 1.6rem;
        font-weight: 800;
        border-radius: 50px;
        color: #1e293b;
        cursor: pointer;
        box-shadow: 
            0 30px 60px rgba(220,38,38,0.6),
            inset 0 2px 10px rgba(255,255,255,0.4);
        transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        font-family: 'Poppins', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        position: relative;
        overflow: hidden;
    }
    
    .reveal-btn:hover {
        transform: translateY(-12px);
        box-shadow: 
            0 40px 80px rgba(220,38,38,0.8),
            inset 0 2px 15px rgba(255,255,255,0.5);
        color: #1e293b;
    }
    
    /* Reveal Box */
    .reveal-box {
        background: linear-gradient(145deg, #fefce8, #ffffff, #fefce8);
        padding: 4rem 3rem;
        border-radius: 35px;
        margin: 3rem 0;
        min-height: 260px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 3.2rem;
        font-weight: 900;
        color: #1e293b !important;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        box-shadow: 
            0 40px 90px rgba(0,0,0,0.5),
            inset 0 2px 20px rgba(255,255,255,0.9);
        opacity: 0;
        transform: scale(0.1) rotateY(180deg);
        animation: revealAnim 3s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
        position: relative;
        border: 4px solid rgba(255,255,255,0.6);
    }
    
    @keyframes revealAnim {
        0% { opacity: 0; transform: scale(0.1) rotateY(180deg); }
        50% { opacity: 0.9; transform: scale(1.1) rotateY(0deg); }
        100% { opacity: 1; transform: scale(1) rotateY(0deg); }
    }
    
    /* Invalid Box */
    .invalid-box {
        background: linear-gradient(145deg, #dc2626, #b91c1c);
        padding: 3rem;
        border-radius: 30px;
        margin: 2.5rem 0;
        color: #fefce8 !important;
        font-size: 1.9rem;
        font-weight: 800;
        box-shadow: 0 30px 70px rgba(220,38,38,0.7);
        animation: shake 0.8s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
        text-align: center;
        border: 4px solid rgba(255,255,255,0.4);
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0) rotate(0deg); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-20px) rotate(-3deg); }
        20%, 40%, 60%, 80% { transform: translateX(20px) rotate(3deg); }
    }
    
    /* Valid Names List */
    .valid-names {
        background: linear-gradient(145deg, rgba(34,197,94,0.3), rgba(34,197,94,0.1));
        padding: 2rem;
        border-radius: 25px;
        margin: 2rem 0;
        color: #f8fafc !important;
        font-size: 1.2rem;
        border: 2px solid rgba(34,197,94,0.6);
        box-shadow: 0 15px 40px rgba(34,197,94,0.4);
    }
    
    /* Snowflakes */
    .snowflake {
        color: #ffffff;
        text-shadow: 0 0 20px rgba(255,255,255,0.9);
        font-size: 2.2rem;
        position: fixed;
        top: -50px;
        animation: fall linear infinite;
        pointer-events: none;
        z-index: 500;
        filter: drop-shadow(0 0 10px rgba(255,255,255,0.8));
    }
    
    @keyframes fall {
        to { transform: translateY(120vh) rotate(1080deg); }
    }
    
    /* Hide Streamlit metrics */
    [data-testid="stMetric"] { display: none !important; }
</style>
"""

def create_christmas_effects():
    """Create enhanced Christmas effects"""
    effects_html = ""
    
    # Red-Green Christmas lights in fixed positions
    light_positions = [
        ("5%", "5%", "#dc2626"), ("95%", "5%", "#22c55e"),
        ("5%", "95%", "#ff6b35"), ("95%", "95%", "#16a34a"),
        ("50%", "2%", "#ffd23f"), ("2%", "50%", "#ef4444"),
        ("98%", "50%", "#059669"), ("50%", "98%", "#dc2626"),
        ("20%", "20%", "#f97316"), ("80%", "80%", "#51cf66")
    ]
    
    for top, left, color in light_positions:
        effects_html += f"""
        <div class="light" style="
            --top: {top};
            --left: {left};
            width: 35px; height: 35px;
            background: {color};
            animation-duration: {random.uniform(1.5, 3.5)}s;
        "></div>
        """
    
    # Enhanced snowflakes
    for i in range(80):
        left = f"{random.randint(0, 100)}vw"
        delay = f"{random.uniform(0, 8)}s"
        duration = f"{random.uniform(15, 35)}s"
        size = random.choice(["1.8rem", "2.2rem", "2.8rem", "1.5rem"])
        effects_html += f"""
        <div class="snowflake" style="
            left: {left};
            animation-delay: {delay};
            animation-duration: {duration};
            font-size: {size};
        ">❄️</div>
        """
    
    return effects_html

def is_valid_participant(name, participants):
    return name.strip().lower() in [p.lower() for p in participants]

def main():
    # Apply CSS first
    st.markdown(css, unsafe_allow_html=True)
    
    # Add Christmas effects
    st.markdown(create_christmas_effects(), unsafe_allow_html=True)
    
    # Session state
    for key in ['revealed', 'user_name', 'invalid_shown']:
        if key not in st.session_state:
            st.session_state[key] = False if key != 'user_name' else ""
    
    # Main content container
    st.markdown('<div class="santa-container">', unsafe_allow_html=True)
    
    if not st.session_state.revealed:
        st.markdown('<h1 class="title">🎅 Secret Santa 🎁</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Ho Ho Ho! Enter your name to discover who drew YOU! ✨</p>', unsafe_allow_html=True)
        
        # Valid participants list
        st.markdown(f"""
        <div class="valid-names">
            <strong>🎄 Valid Participants:</strong><br>
            <span style="font-size: 1.4rem;">{', '.join(PARTICIPANTS)}</span> 🎄
        </div>
        """, unsafe_allow_html=True)
        
        name = st.text_input("", 
                           placeholder="👤 Enter your name here...",
                           key="name_input",
                           help="Type your name exactly as listed above!")
        
        if st.button("🎊 REVEAL MY SECRET SANTA 🎊", key="reveal_btn", help="Click to discover!"):
            if name.strip():
                if is_valid_participant(name, PARTICIPANTS):
                    st.session_state.user_name = name.strip()
                    st.session_state.invalid_shown = False
                    
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
                st.error("🎄 Please enter your name first!")
        
        if st.session_state.invalid_shown and st.session_state.user_name:
            st.markdown(f"""
            <div class="invalid-box">
                ❌ <strong>{st.session_state.user_name}</strong> is not a valid participant!<br>
                🎅 Please check the list above and try again! 🎅
            </div>
            """, unsafe_allow_html=True)
            
    else:
        st.markdown(f"""
        <div class="reveal-box">
            <div style="font-size: 1.6rem; margin-bottom: 1.5rem; font-weight: 600;">
                Hey <strong>{st.session_state.user_name}</strong>!
            </div>
            Your Secret Santa is...<br>
            <strong style="font-size: 4rem; color: #dc2626;">{st.session_state.secret_santa}</strong>! 🎁✨🎅
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<p class="subtitle" style="margin-top: 3rem;">Spread some holiday magic! Merry Christmas! 🎄❄️</p>', unsafe_allow_html=True)
        
        if st.button("🔄 Try Another Name", key="reset_btn"):
            for key in ['revealed', 'user_name', 'secret_santa', 'invalid_shown']:
                st.session_state[key] = False if key != 'user_name' else ""
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(
        page_title="🎅 Secret Santa",
        page_icon="🎁",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    main()
