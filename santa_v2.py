import streamlit as st
import random
from streamlit.components.v1 import html

# Secret Santa participants (you can customize this list)
PARTICIPANTS = [
    "Alice", "Bob", "Charlie", "Diana", "Eve", 
    "Frank", "Grace", "Henry", "Ivy", "Jack"
]

# Christmas Red-to-Green Gradient Theme CSS
css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&display=swap');
    
    /* Red to Green Christmas Gradient Background */
    .main {
        background: linear-gradient(135deg, 
            #dc2626 0%, 
            #ea580c 20%, 
            #f97316 40%, 
            #eab308 50%, 
            #84cc16 60%, 
            #22c55e 80%, 
            #16a34a 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        min-height: 100vh;
        font-family: 'Poppins', sans-serif;
        position: relative;
        overflow: hidden;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Christmas Lights Animation */
    .light {
        position: fixed;
        border-radius: 50%;
        animation: twinkle 2s ease-in-out infinite;
        box-shadow: 0 0 25px currentColor;
        z-index: 2;
    }
    
    .light:nth-child(odd) { animation-delay: 0s; }
    .light:nth-child(even) { animation-delay: 1s; }
    
    @keyframes twinkle {
        0%, 100% { opacity: 0.4; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.3); }
    }
    
    .santa-container {
        max-width: 600px;
        margin: 0 auto;
        padding: 2.5rem;
        text-align: center;
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(20px);
        border: 3px solid rgba(255,255,255,0.3);
        border-radius: 30px;
        box-shadow: 
            0 30px 60px rgba(0,0,0,0.4),
            inset 0 1px 0 rgba(255,255,255,0.5);
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
        height: 8px;
        background: linear-gradient(90deg, 
            #dc2626, #f97316, #eab308, #22c55e, #16a34a, #dc2626);
        border-radius: 30px 30px 0 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .title {
        font-size: 3.8rem;
        font-family: 'Dancing Script', cursive;
        background: linear-gradient(45deg, #fefce8, #ffffff, #fefce8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        text-shadow: 
            0 0 20px rgba(255,255,255,0.8),
            2px 2px 10px rgba(0,0,0,0.3);
        animation: titleGlow 3s ease-in-out infinite;
    }
    
    @keyframes titleGlow {
        0%, 100% { 
            text-shadow: 
                0 0 20px rgba(255,255,255,0.8),
                2px 2px 10px rgba(0,0,0,0.3);
        }
        50% { 
            text-shadow: 
                0 0 40px rgba(255,255,255,1),
                0 0 60px rgba(255,255,255,0.6),
                2px 2px 10px rgba(0,0,0,0.3);
        }
    }
    
    .subtitle {
        font-size: 1.5rem;
        color: #fefce8;
        margin-bottom: 2rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
        font-weight: 500;
    }
    
    .name-input {
        width: 100%;
        padding: 1.3rem;
        font-size: 1.7rem;
        border: 4px solid rgba(255,255,255,0.4);
        border-radius: 25px;
        background: rgba(255,255,255,0.95);
        box-shadow: 
            0 20px 40px rgba(0,0,0,0.3),
            inset 0 1px 0 rgba(255,255,255,1);
        text-align: center;
        margin-bottom: 2.5rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        transition: all 0.4s ease;
    }
    
    .name-input:focus {
        border-color: #fefce8;
        box-shadow: 
            0 25px 50px rgba(254,252,232,0.4),
            inset 0 1px 0 rgba(255,255,255,1);
        transform: scale(1.03);
    }
    
    .reveal-btn {
        background: linear-gradient(45deg, #dc2626, #f97316, #eab308);
        border: none;
        padding: 1.5rem 4rem;
        font-size: 1.5rem;
        font-weight: 800;
        border-radius: 60px;
        color: white;
        cursor: pointer;
        box-shadow: 
            0 25px 50px rgba(220,38,38,0.5),
            inset 0 1px 0 rgba(255,255,255,0.3);
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        font-family: 'Poppins', sans-serif;
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .reveal-btn:hover {
        transform: translateY(-10px);
        box-shadow: 
            0 35px 70px rgba(220,38,38,0.7),
            inset 0 1px 0 rgba(255,255,255,0.4);
    }
    
    /* Reveal Animation */
    .reveal-box {
        background: linear-gradient(45deg, #fefce8, #ffffff, #fefce8);
        padding: 4rem 2.5rem;
        border-radius: 35px;
        margin: 3rem 0;
        min-height: 240px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        font-weight: 800;
        color: #1f2937;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
        box-shadow: 
            0 35px 70px rgba(0,0,0,0.4),
            inset 0 1px 0 rgba(255,255,255,0.8);
        opacity: 0;
        transform: scale(0.2) rotateY(180deg);
        animation: revealAnim 3s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
        position: relative;
        overflow: hidden;
    }
    
    .reveal-box::before {
        content: '🎁✨🎅';
        position: absolute;
        font-size: 5rem;
        top: 15px;
        left: 50%;
        transform: translateX(-50%);
        animation: giftBounce 1.2s ease-in-out 1.5s both;
    }
    
    @keyframes giftBounce {
        0%, 60%, 100% { transform: translateX(-50%) translateY(0); }
        30%, 70% { transform: translateX(-50%) translateY(-25px); }
    }
    
    @keyframes revealAnim {
        0% { opacity: 0; transform: scale(0.2) rotateY(180deg); }
        50% { opacity: 0.8; transform: scale(1.1) rotateY(0deg); }
        100% { opacity: 1; transform: scale(1) rotateY(0deg); }
    }
    
    /* Invalid Participant Styling */
    .invalid-box {
        background: linear-gradient(45deg, #dc2626, #b91c1c);
        padding: 3rem;
        border-radius: 30px;
        margin: 2.5rem 0;
        color: #fefce8;
        font-size: 1.8rem;
        font-weight: 700;
        box-shadow: 0 25px 50px rgba(220,38,38,0.5);
        animation: shake 0.8s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
        text-align: center;
        border: 4px solid rgba(255,255,255,0.3);
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0) rotate(0deg); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-15px) rotate(-3deg); }
        20%, 40%, 60%, 80% { transform: translateX(15px) rotate(3deg); }
    }
    
    .valid-names {
        background: rgba(34,197,94,0.3);
        padding: 2rem;
        border-radius: 25px;
        margin: 2rem 0;
        color: #fefce8;
        font-size: 1.1rem;
        border: 2px solid rgba(34,197,94,0.5);
        box-shadow: 0 10px 30px rgba(34,197,94,0.3);
    }
    
    /* Enhanced Snowflakes with Red/Green tint */
    .snowflake {
        color: #fefce8;
        text-shadow: 0 0 15px rgba(255,255,255,0.9);
        font-size: 2rem;
        position: fixed;
        top: -40px;
        animation: fall linear infinite;
        pointer-events: none;
        z-index: 5;
    }
    
    @keyframes fall {
        to {
            transform: translateY(120vh) rotate(1080deg);
        }
    }
</style>
"""

def create_christmas_effects():
    """Create Christmas lights and snowflakes matching red-green theme"""
    effects_html = ""
    
    # Red-Green Christmas lights
    light_positions = [
        ("8%", "8%", "#dc2626"), ("92%", "8%", "#22c55e"),
        ("8%", "92%", "#f97316"), ("92%", "92%", "#16a34a"),
        ("50%", "3%", "#eab308"), ("3%", "50%", "#ef4444"),
        ("97%", "50%", "#059669"), ("50%", "97%", "#dc2626")
    ]
    
    for i, (top, left, color) in enumerate(light_positions):
        size = "30px" if i < 4 else "25px"
        effects_html += f"""
        <div class="light" style="
            width: {size}; height: {size};
            top: {top}; left: {left};
            background: {color};
            animation-duration: {random.uniform(1.8, 3.2)}s;
        "></div>
        """
    
    # Snowflakes
    for i in range(70):
        left = f"{random.randint(0, 100)}vw"
        delay = f"{random.randint(0, 40)}s"
        duration = f"{random.uniform(15, 30)}s"
        size = random.choice(["1.5rem", "2rem", "2.5rem"])
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
                <div style="font-size: 1.4rem; margin-bottom: 1.5rem;">Hey <strong>{st.session_state.user_name}</strong>,</div>
                Your Secret Santa is... <br><strong style="font-size: 3.5rem;">{st.session_state.secret_santa}</strong>! 🎁✨
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<p class="subtitle" style="margin-top: 2.5rem;">Spread some holiday magic! 🎅❄️</p>', unsafe_allow_html=True)
            
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
