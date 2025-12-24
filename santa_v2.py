import streamlit as st
import random
import hashlib

# Secret Santa participants
PARTICIPANTS = [
    "Alice", "Bob", "Charlie", "Diana", "Eve", 
    "Frank", "Grace", "Henry", "Ivy", "Jack"
]

# ULTRA READABLE RED-GREEN GRADIENT with PERFECT TEXT
css = """
<style>
    /* RED to LIGHT GREEN Background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, 
            #b91c1c 0%, #dc2626 15%, #ef4444 30%, 
            #f97316 45%, #eab308 60%, #84cc16 75%, #4ade80 100%);
        background-size: 400% 400%;
        animation: gradientShift 25s ease infinite;
        min-height: 100vh;
        position: relative;
    }
    
    /* FORCE ALL Streamlit text overrides */
    *, *::before, *::after {
        color: #ffffff !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8) !important;
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
    
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=Dancing+Script:wght@700&display=swap');
    
    /* Christmas Lights */
    .light {
        position: fixed;
        border-radius: 50%;
        animation: twinkle 2s ease-in-out infinite;
        box-shadow: 0 0 40px currentColor;
        z-index: 999;
        top: var(--top);
        left: var(--left);
    }
    
    @keyframes twinkle {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.5); }
    }
    
    /* PERFECT WHITE CONTAINER */
    .santa-container {
        max-width: 800px;
        margin: 2rem auto;
        padding: 4rem;
        text-align: center;
        background: rgba(255,255,255,0.95) !important;
        backdrop-filter: blur(35px) brightness(1.2);
        border: 5px solid rgba(255,255,255,0.95);
        border-radius: 40px;
        box-shadow: 
            0 60px 150px rgba(0,0,0,0.6),
            inset 0 5px 40px rgba(255,255,255,0.9);
        position: relative;
        z-index: 1000;
    }
    
    .santa-container * {
        color: #1a1a1a !important;
        text-shadow: none !important;
    }
    
    .santa-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 15px;
        background: linear-gradient(90deg, 
            #b91c1c, #dc2626, #f97316, #eab308, #84cc16, #4ade80, #b91c1c);
        border-radius: 40px 40px 0 0;
        box-shadow: 0 5px 30px rgba(185,28,28,0.8);
    }
    
    /* BOLD WHITE TITLE */
    .title {
        font-size: 5rem !important;
        font-family: 'Dancing Script', cursive !important;
        background: linear-gradient(45deg, #ffffff, #f0f9ff, #ffffff) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin-bottom: 2rem !important;
        text-shadow: 
            0 0 50px rgba(255,255,255,1),
            3px 3px 20px rgba(0,0,0,0.5) !important;
        animation: titleGlow 3s ease-in-out infinite;
        letter-spacing: 5px !important;
        color: #ffffff !important;
    }
    
    @keyframes titleGlow {
        0%, 100% { 
            filter: drop-shadow(0 0 50px rgba(255,255,255,1));
            transform: scale(1);
        }
        50% { 
            filter: drop-shadow(0 0 80px rgba(255,255,255,1));
            transform: scale(1.05);
        }
    }
    
    /* DARK TEXT ON WHITE CONTAINER */
    .subtitle {
        font-size: 2rem !important;
        color: #1f2937 !important;
        margin-bottom: 3rem !important;
        font-weight: 700 !important;
        font-family: 'Poppins', sans-serif !important;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.3) !important;
    }
    
    /* ULTRA CLEAR INPUTS */
    .name-input, .pin-input, [data-baseweb="select"], [data-baseweb="input"] {
        width: 100% !important;
        padding: 2rem 3rem !important;
        font-size: 2rem !important;
        border: 5px solid #1f2937 !important;
        border-radius: 35px !important;
        background: #ffffff !important;
        box-shadow: 
            0 40px 90px rgba(0,0,0,0.4),
            inset 0 5px 30px rgba(255,255,255,1) !important;
        text-align: center !important;
        margin-bottom: 3rem !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        color: #1f2937 !important;
        text-shadow: none !important;
    }
    
    /* PERFECT BUTTONS */
    .reveal-btn, .status-btn, .check-btn, .stButton>button {
        background: linear-gradient(45deg, #b91c1c, #dc2626, #ef4444) !important;
        border: none !important;
        padding: 2rem 5rem !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        border-radius: 70px !important;
        color: #ffffff !important;
        cursor: pointer !important;
        box-shadow: 
            0 40px 100px rgba(185,28,28,0.8),
            inset 0 4px 25px rgba(255,255,255,0.3) !important;
        transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
        font-family: 'Poppins', sans-serif !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        margin: 1rem !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.5) !important;
    }
    
    /* ULTRA VISIBLE REVEAL BOX */
    .reveal-box {
        background: linear-gradient(145deg, #ffffff, #fafbfc, #ffffff) !important;
        padding: 6rem 5rem !important;
        border-radius: 45px !important;
        margin: 4rem 0 !important;
        min-height: 320px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 4rem !important;
        font-weight: 900 !important;
        color: #b91c1c !important;
        text-shadow: 4px 4px 20px rgba(0,0,0,0.4) !important;
        box-shadow: 
            0 80px 200px rgba(0,0,0,0.7),
            inset 0 8px 50px rgba(255,255,255,0.95) !important;
        border: 8px solid rgba(185,28,28,0.3) !important;
        opacity: 0;
        transform: scale(0.1) rotateY(180deg);
        animation: revealAnim 3.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards !important;
        position: relative;
    }
    
    .reveal-box * {
        color: #b91c1c !important;
        text-shadow: 3px 3px 15px rgba(0,0,0,0.3) !important;
        font-weight: 800 !important;
    }
    
    @keyframes revealAnim {
        0% { opacity: 0; transform: scale(0.1) rotateY(180deg); }
        50% { opacity: 0.95; transform: scale(1.15) rotateY(0deg); }
        100% { opacity: 1; transform: scale(1) rotateY(0deg); }
    }
    
    /* ERROR BOX */
    .invalid-box {
        background: linear-gradient(145deg, #b91c1c, #991b1b) !important;
        padding: 4.5rem !important;
        border-radius: 40px !important;
        margin: 3.5rem 0 !important;
        color: #fefce8 !important;
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        box-shadow: 0 50px 120px rgba(185,28,28,0.9) !important;
        animation: shake 1s ease-in-out both !important;
        text-align: center !important;
        border: 6px solid rgba(254,252,232,0.8) !important;
        text-shadow: 3px 3px 15px rgba(0,0,0,0.8) !important;
    }
    
    .valid-names {
        background: linear-gradient(145deg, #16a34a, #15803d) !important;
        padding: 3.5rem !important;
        border-radius: 35px !important;
        margin: 3.5rem 0 !important;
        color: #ffffff !important;
        font-size: 1.6rem !important;
        border: 5px solid rgba(255,255,255,0.9) !important;
        box-shadow: 0 40px 100px rgba(22,163,74,0.6) !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.7) !important;
    }
    
    .status-card {
        background: rgba(255,255,255,0.98) !important;
        padding: 4rem !important;
        border-radius: 35px !important;
        margin: 2.5rem 0 !important;
        border: 4px solid rgba(255,255,255,0.95) !important;
        color: #1f2937 !important;
        box-shadow: 0 45px 120px rgba(0,0,0,0.5) !important;
        text-shadow: none !important;
    }
    
    .status-card * {
        color: #1f2937 !important;
        text-shadow: none !important;
    }
    
    /* SNOWFLAKES */
    .snowflake {
        color: #ffffff !important;
        text-shadow: 0 0 40px rgba(255,255,255,1) !important;
        font-size: 3rem !important;
        position: fixed;
        top: -80px;
        animation: fall linear infinite;
        pointer-events: none;
        z-index: 500;
    }
    
    @keyframes fall {
        to { transform: translateY(150vh) rotate(1800deg); }
    }
</style>
"""

def generate_pin(name):
    seed = f"{name}{random.randint(1000, 9999)}"
    return str(int(hashlib.md5(seed.encode()).hexdigest(), 16) % 10000).zfill(4)

def create_christmas_effects():
    effects_html = ""
    light_positions = [
        ("3%", "3%", "#b91c1c"), ("97%", "3%", "#4ade80"),
        ("3%", "97%", "#dc2626"), ("97%", "97%", "#84cc16"),
        ("50%", "1%", "#eab308"), ("1%", "50%", "#ef4444"),
        ("99%", "50%", "#16a34a"), ("50%", "99%", "#b91c1c")
    ]
    
    for top, left, color in light_positions:
        effects_html += f"""
        <div class="light" style="
            --top: {top}; --left: {left};
            width: 50px; height: 50px;
            background: {color};
            animation-duration: {random.uniform(1.8, 4.2)}s;
        "></div>
        """
    
    for i in range(150):
        effects_html += f"""
        <div class="snowflake" style="
            left: {random.randint(0, 100)}vw;
            animation-delay: {random.uniform(0, 15)}s;
            animation-duration: {random.uniform(30, 60)}s;
            font-size: {random.choice(['2.5rem', '3rem', '3.5rem', '2.2rem'])};
        ">❄️</div>
        """
    return effects_html

def is_valid_participant(name, participants):
    return name.strip().lower() in [p.lower() for p in participants]

def main():
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(create_christmas_effects(), unsafe_allow_html=True)
    
    for key in ['revealed', 'user_name', 'secret_santa', 'invalid_shown', 'pin_generated']:
        if key not in st.session_state:
            st.session_state[key] = False if key != 'user_name' else ""
    if 'participants_data' not in st.session_state:
        st.session_state.participants_data = {}
    
    st.markdown('<div class="santa-container">', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🎅 Draw Secret Santa", "📋 Check Status"])
    
    with tab1:
        st.markdown('<h1 class="title">🎅 Secret Santa 🎁</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Ho Ho Ho! Enter your name to discover who drew YOU!</p>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="valid-names">
            <strong>🎄 Valid Participants:</strong><br>
            <span style="font-size: 1.8rem;">{', '.join(PARTICIPANTS)}</span> 🎄
        </div>
        """, unsafe_allow_html=True)
        
        name = st.text_input("", placeholder="👤 Enter your name here...", key="name_input")
        
        if st.button("🎊 REVEAL MY SECRET SANTA 🎊", key="reveal_btn"):
            if name.strip():
                if is_valid_participant(name, PARTICIPANTS):
                    if name not in st.session_state.participants_data or not st.session_state.participants_data[name].get('drawn', False):
                        st.session_state.user_name = name.strip()
                        other_names = [n for n in PARTICIPANTS if n.lower() != name.lower()]
                        secret_santa = random.choice(other_names)
                        pin = generate_pin(name)
                        
                        st.session_state.secret_santa = secret_santa
                        st.session_state.pin_generated = pin
                        st.session_state.participants_data[name] = {
                            'secret_santa': secret_santa,
                            'pin': pin,
                            'drawn': True
                        }
                        st.session_state.revealed = True
                        st.rerun()
                    else:
                        st.markdown("""
                        <div class="invalid-box">
                            ❌ You have already drawn your Secret Santa!<br>
                            Go to <strong>Check Status</strong> tab with your PIN! 🎅
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="invalid-box">
                        ❌ <strong>{name}</strong> is not a valid participant!<br>
                        🎅 Please check the list above and try again! 🎅
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("🎄 Please enter your name first!")
        
        if st.session_state.revealed:
            st.markdown(f"""
            <div class="reveal-box">
                <div style="font-size: 2.5rem; margin-bottom: 3rem; font-weight: 800;">
                    Hey <strong>{st.session_state.user_name}</strong>!
                </div>
                Your Secret Santa is...<br>
                <strong style="font-size: 6rem;">{st.session_state.secret_santa}</strong>! 🎁✨🎅
                <div style="font-size: 2rem; margin-top: 4rem;">
                    📌 <strong>Your PIN: {st.session_state.pin_generated}</strong><br>
                    Save this PIN to check status later! 🔐
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<h1 class="title">📋 Status Check</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Check your Secret Santa assignment using your PIN!</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Enter your name:", placeholder="Your name", key="status_name")
        with col2:
            pin = st.text_input("🔑 Enter your PIN:", placeholder="4-digit PIN", type="password", key="status_pin")
        
        if st.button("✅ Check Status", key="check_status"):
            if name and pin:
                participant_data = st.session_state.participants_data.get(name, {})
                if participant_data.get('drawn', False) and participant_data.get('pin') == pin:
                    st.success("✅ Valid login!")
                    st.markdown(f"""
                    <div class="status-card">
                        <h3 style="font-size: 2.5rem; margin-bottom: 2rem;">🎅 Your Assignment:</h3>
                        <strong style="font-size: 5rem; color: #b91c1c;">{participant_data['secret_santa']}</strong>
                        <p style="font-size: 2rem;">🎁 Buy a gift for {participant_data['secret_santa']}!</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="invalid-box">
                        ❌ Invalid name or PIN combination!<br>
                        Please check and try again. 🎅
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("Please enter both name and PIN!")
        
        st.markdown("""
        <div class="status-card">
            <strong style="font-size: 1.6rem;">ℹ️ How to use:</strong><br>
            • Use the name & 4-digit PIN from your first draw<br>
            • Each person can only draw <strong>ONCE</strong><br>
            • Check status anytime before Christmas! 🎄✨
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(
        page_title="🎅 Secret Santa",
        page_icon="🎁",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    main()
