import streamlit as st
import random
import hashlib

# Secret Santa participants
PARTICIPANTS = [
    "Alice", "Bob", "Charlie", "Diana", "Eve", 
    "Frank", "Grace", "Henry", "Ivy", "Jack"
]

# FIXED RED to LIGHT GREEN with PERFECT READABILITY
css = """
<style>
    /* Force full override - RED to LIGHT GREEN gradient */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, 
            #dc2626 0%,      
            #ef4444 15%,     
            #f97316 30%,     
            #eab308 45%,     
            #84cc16 60%,     
            #a3e635 75%,     
            #4ade80 100%     
        );
        background-size: 400% 400%;
        animation: gradientShift 25s ease infinite;
        min-height: 100vh;
        position: relative;
    }
    
    [data-testid="stAppViewContainer"] > div > div > div {
        background: transparent !important;
    }
    
    /* FORCE ALL STREAMLIT TEXT TO WHITE */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown p,
    .stText, .st-emotion-cache-1f5gtxj p,
    div[data-testid="stMarkdownContainer"] * {
        color: #ffffff !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5) !important;
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
    
    /* PERFECT WHITE CONTAINER */
    .santa-container {
        max-width: 750px;
        margin: 2rem auto;
        padding: 3.5rem;
        text-align: center;
        background: rgba(255,255,255,0.98) !important;
        backdrop-filter: blur(30px) brightness(1.15);
        border: 4px solid rgba(255,255,255,0.9);
        border-radius: 35px;
        box-shadow: 
            0 50px 120px rgba(0,0,0,0.5),
            inset 0 4px 30px rgba(255,255,255,0.8);
        position: relative;
        z-index: 1000;
    }
    
    .santa-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 12px;
        background: linear-gradient(90deg, 
            #dc2626, #f97316, #eab308, #84cc16, #4ade80, #dc2626);
        border-radius: 35px 35px 0 0;
        box-shadow: 0 4px 25px rgba(220,38,38,0.7);
    }
    
    /* WHITE GLOWING TITLE */
    .title {
        font-size: 4.5rem !important;
        font-family: 'Dancing Script', cursive !important;
        background: linear-gradient(45deg, #ffffff, #f0f9ff, #ffffff) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin-bottom: 2rem !important;
        text-shadow: 
            0 0 40px rgba(255,255,255,0.9),
            2px 2px 10px rgba(0,0,0,0.3) !important;
        animation: titleGlow 4s ease-in-out infinite;
        letter-spacing: 4px;
        color: #ffffff !important;
    }
    
    @keyframes titleGlow {
        0%, 100% { text-shadow: 0 0 40px rgba(255,255,255,0.9), 2px 2px 10px rgba(0,0,0,0.3); }
        50% { text-shadow: 0 0 70px rgba(255,255,255,1), 0 0 100px rgba(255,255,255,0.7), 2px 2px 10px rgba(0,0,0,0.3); }
    }
    
    .subtitle {
        font-size: 1.8rem !important;
        color: #1e293b !important;
        margin-bottom: 3rem !important;
        text-shadow: 1px 1px 5px rgba(0,0,0,0.3) !important;
        font-weight: 600 !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* PERFECT INPUTS */
    .name-input, .pin-input, [data-baseweb="select"] {
        width: 100% !important;
        padding: 1.8rem 2.5rem !important;
        font-size: 1.9rem !important;
        border: 4px solid #1e293b !important;
        border-radius: 30px !important;
        background: #ffffff !important;
        box-shadow: 
            0 35px 70px rgba(0,0,0,0.4),
            inset 0 4px 20px rgba(255,255,255,1) !important;
        text-align: center !important;
        margin-bottom: 2.5rem !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        color: #1e293b !important;
    }
    
    /* BUTTONS */
    .reveal-btn, .status-btn, .check-btn, .stButton>button {
        background: linear-gradient(45deg, #1e293b, #334155, #475569) !important;
        border: none !important;
        padding: 1.8rem 4.5rem !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        border-radius: 60px !important;
        color: #ffffff !important;
        cursor: pointer !important;
        box-shadow: 
            0 35px 80px rgba(30,41,59,0.8),
            inset 0 3px 20px rgba(255,255,255,0.4) !important;
        transition: all 0.5s ease !important;
        font-family: 'Poppins', sans-serif !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        margin: 0.8rem !important;
    }
    
    /* REVEAL BOX - WHITE TEXT GUARANTEED */
    .reveal-box {
        background: linear-gradient(145deg, #ffffff, #f8fafc, #ffffff) !important;
        padding: 5rem 4rem !important;
        border-radius: 40px !important;
        margin: 4rem 0 !important;
        min-height: 280px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        color: #1e293b !important;
        text-shadow: 3px 3px 15px rgba(0,0,0,0.3) !important;
        box-shadow: 
            0 60px 140px rgba(0,0,0,0.6),
            inset 0 5px 40px rgba(255,255,255,0.9) !important;
        border: 6px solid rgba(30,41,59,0.2) !important;
        opacity: 0;
        transform: scale(0.1) rotateY(180deg);
        animation: revealAnim 3s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards !important;
    }
    
    .reveal-box * {
        color: #1e293b !important;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.2) !important;
    }
    
    @keyframes revealAnim {
        0% { opacity: 0; transform: scale(0.1) rotateY(180deg); }
        50% { opacity: 0.9; transform: scale(1.1) rotateY(0deg); }
        100% { opacity: 1; transform: scale(1) rotateY(0deg); }
    }
    
    .invalid-box {
        background: linear-gradient(145deg, #dc2626, #b91c1c) !important;
        padding: 4rem !important;
        border-radius: 35px !important;
        margin: 3rem 0 !important;
        color: #fefce8 !important;
        font-size: 2.2rem !important;
        font-weight: 900 !important;
        box-shadow: 0 40px 100px rgba(220,38,38,0.9) !important;
        animation: shake 0.8s ease-in-out both !important;
        text-align: center !important;
        border: 5px solid rgba(255,255,255,0.6) !important;
    }
    
    .invalid-box * {
        color: #fefce8 !important;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-25px); }
        20%, 40%, 60%, 80% { transform: translateX(25px); }
    }
    
    .valid-names {
        background: linear-gradient(145deg, rgba(74,222,128,0.9), rgba(34,197,94,0.7)) !important;
        padding: 3rem !important;
        border-radius: 30px !important;
        margin: 3rem 0 !important;
        color: #1e293b !important;
        font-size: 1.4rem !important;
        border: 4px solid rgba(34,197,94,1) !important;
        box-shadow: 0 30px 80px rgba(34,197,94,0.5) !important;
        font-weight: 700 !important;
    }
    
    .valid-names * {
        color: #1e293b !important;
    }
    
    .status-card {
        background: rgba(255,255,255,0.98) !important;
        padding: 3rem !important;
        border-radius: 30px !important;
        margin: 2rem 0 !important;
        border: 3px solid rgba(255,255,255,0.9) !important;
        color: #1e293b !important;
        box-shadow: 0 35px 90px rgba(0,0,0,0.4) !important;
    }
    
    .status-card * {
        color: #1e293b !important;
    }
    
    .snowflake {
        color: #ffffff !important;
        text-shadow: 0 0 15px rgba(255,255,255,1) !important;
        font-size: 1.5rem !important;
        position: fixed;
        top: -70px;
        animation: fall linear infinite;
        pointer-events: none;
        z-index: 500;
        filter: drop-shadow(0 0 20px rgba(255,255,255,1)) !important;
    }
    
    @keyframes fall {
        to { transform: translateY(140vh) rotate(1440deg); }
    }
</style>
"""

def generate_pin(name):
    seed = f"{name}{random.randint(1000, 9999)}"
    return str(int(hashlib.md5(seed.encode()).hexdigest(), 16) % 10000).zfill(4)

def create_christmas_effects():
    effects_html = ""
    light_positions = [
        ("5%", "5%", "#dc2626"), ("95%", "5%", "#4ade80"),
        ("5%", "95%", "#f97316"), ("95%", "95%", "#84cc16"),
        ("50%", "2%", "#eab308"), ("2%", "50%", "#ef4444"),
        ("98%", "50%", "#a3e635"), ("50%", "98%", "#dc2626")
    ]
    
    for top, left, color in light_positions:
        effects_html += f"""
        <div class="light" style="
            --top: {top}; --left: {left};
            width: 45px; height: 45px;
            background: {color};
            animation-duration: {random.uniform(1.5, 4)}s;
        "></div>
        """
    
    for i in range(120):
        effects_html += f"""
        <div class="snowflake" style="
            left: {random.randint(0, 100)}vw;
            animation-delay: {random.uniform(0, 12)}s;
            animation-duration: {random.uniform(25, 45)}s;
            font-size: {random.choice(['2.2rem', '2.8rem', '3.2rem', '2rem'])};
        ">❄️</div>
        """
    return effects_html

def is_valid_participant(name, participants):
    return name.strip().lower() in [p.lower() for p in participants]

def main():
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(create_christmas_effects(), unsafe_allow_html=True)
    
    # Initialize session state
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
            <span style="font-size: 1.6rem; font-weight: 700;">{', '.join(PARTICIPANTS)}</span> 🎄
        </div>
        """, unsafe_allow_html=True)
        
        name = st.text_input("", placeholder="👤 Enter your name here...", key="name_input")
        
        if st.button("🎊 REVEAL MY SECRET SANTA 🎊", key="reveal_btn"):
            if name.strip():
                if is_valid_participant(name, PARTICIPANTS):
                    if not st.session_state.participants_data.get(name, {}).get('drawn', False):
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
                            ❌ You have already drawn your Secret Santa! 
                            <br>Go to <strong>Check Status</strong> tab with your PIN. 🎅
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
                <div style="font-size: 2rem; margin-bottom: 2.5rem; font-weight: 700;">
                    Hey <strong>{st.session_state.user_name}</strong>!
                </div>
                Your Secret Santa is...<br>
                <strong style="font-size: 5rem; color: #dc2626 !important;">{st.session_state.secret_santa}</strong>! 🎁✨🎅
                <div style="font-size: 1.6rem; margin-top: 3rem; color: #1e293b;">
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
                        <h3 style="color: #1e293b; margin-bottom: 1.5rem; font-size: 2rem;">🎅 Your Assignment:</h3>
                        <strong style="font-size: 4rem; color: #dc2626;">{participant_data['secret_santa']}</strong>
                        <p style="font-size: 1.6rem; color: #475569;">🎁 Buy a gift for {participant_data['secret_santa']}!</p>
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
            <strong style="color: #1e293b; font-size: 1.3rem;">ℹ️ How to use:</strong><br>
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
