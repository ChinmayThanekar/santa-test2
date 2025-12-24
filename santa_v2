import streamlit as st
import random
from streamlit.components.v1 import html

# Secret Santa participants (you can customize this list)
PARTICIPANTS = [
    "Alice", "Bob", "Charlie", "Diana", "Eve", 
    "Frank", "Grace", "Henry", "Ivy", "Jack"
]

# Custom CSS with Christmas theme and reveal animation [web:44][web:45]
css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        font-family: 'Poppins', sans-serif;
    }
    
    .santa-container {
        max-width: 600px;
        margin: 0 auto;
        padding: 2rem;
        text-align: center;
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }
    
    .title {
        font-size: 3rem;
        background: linear-gradient(45deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2rem;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px #ff6b6b; }
        to { text-shadow: 0 0 30px #feca57; }
    }
    
    .name-input {
        width: 100%;
        padding: 1rem;
        font-size: 1.5rem;
        border: none;
        border-radius: 15px;
        background: rgba(255,255,255,0.9);
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 2rem;
        font-family: 'Poppins', sans-serif;
    }
    
    .reveal-btn {
        background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
        border: none;
        padding: 1.2rem 3rem;
        font-size: 1.3rem;
        font-weight: 700;
        border-radius: 50px;
        color: white;
        cursor: pointer;
        box-shadow: 0 15px 35px rgba(255,107,107,0.4);
        transition: all 0.3s ease;
        font-family: 'Poppins', sans-serif;
    }
    
    .reveal-btn:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 45px rgba(255,107,107,0.6);
    }
    
    /* Reveal Animation */
    .reveal-box {
        background: linear-gradient(45deg, #ff9ff3, #feca57);
        padding: 3rem;
        border-radius: 25px;
        margin: 2rem 0;
        min-height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        box-shadow: 0 25px 50px rgba(0,0,0,0.2);
        opacity: 0;
        transform: scale(0.5) rotateY(90deg);
        animation: revealAnim 2s ease-out forwards;
        position: relative;
        overflow: hidden;
    }
    
    @keyframes revealAnim {
        0% { opacity: 0; transform: scale(0.5) rotateY(90deg); }
        50% { opacity: 0.7; transform: scale(1.1) rotateY(0deg); }
        100% { opacity: 1; transform: scale(1) rotateY(0deg); }
    }
    
    .snowflake {
        color: #fff;
        font-size: 2rem;
        position: fixed;
        top: -20px;
        animation: fall linear infinite;
        pointer-events: none;
        z-index: 1000;
    }
    
    @keyframes fall {
        to {
            transform: translateY(100vh) rotate(360deg);
        }
    }
    
    .confetti {
        position: fixed;
        width: 10px;
        height: 10px;
        background: #feca57;
        top: -10px;
        animation: confetti-fall 3s linear infinite;
        pointer-events: none;
        z-index: 1000;
    }
    
    @keyframes confetti-fall {
        0% { transform: translateY(-100vh) rotate(0deg); opacity: 1; }
        100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
    }
</style>
"""

def create_snowflakes():
    """Create falling snowflakes effect"""
    snowflakes_html = ""
    import time
    for i in range(50):
        left = f"{random.randint(0, 100)}vw"
        delay = f"{random.randint(0, 20)}s"
        duration = f"{random.uniform(10, 20)}s"
        size = random.choice(["1rem", "1.5rem", "2rem"])
        snowflakes_html += f"""
        <div class="snowflake" style="
            left: {left};
            animation-delay: {delay};
            animation-duration: {duration};
            font-size: {size};
        ">❄</div>
        """
    return snowflakes_html

def main():
    st.markdown(css, unsafe_allow_html=True)
    
    # Add snowflakes
    st.markdown(create_snowflakes(), unsafe_allow_html=True)
    
    # Welcome page state
    if 'revealed' not in st.session_state:
        st.session_state.revealed = False
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    
    container = st.container()
    
    with container:
        st.markdown('<div class="santa-container">', unsafe_allow_html=True)
        
        if not st.session_state.revealed:
            st.markdown('<h1 class="title">🎅 Secret Santa 🎁</h1>', unsafe_allow_html=True)
            st.markdown('<p style="font-size: 1.3rem; color: white; margin-bottom: 2rem;">Enter your name to discover your Secret Santa!</p>', unsafe_allow_html=True)
            
            name = st.text_input("", 
                               placeholder="Enter your name here...",
                               key="name_input",
                               help="Type your name and press Enter or click Reveal!")
            
            if st.button("🎊 REVEAL MY SECRET SANTA 🎊", key="reveal_btn", help="Click to find out!"):
                if name.strip():
                    st.session_state.user_name = name.strip()
                    
                    # Find secret santa (simple random assignment, no self-assignment)
                    other_names = [n for n in PARTICIPANTS if n.lower() != name.lower()]
                    if other_names:
                        secret_santa = random.choice(other_names)
                        st.session_state.secret_santa = secret_santa
                        st.session_state.revealed = True
                        st.rerun()
                else:
                    st.error("Please enter your name first! 🎄")
        else:
            # Reveal animation
            st.markdown(f"""
            <div class="reveal-box">
                Your Secret Santa is... <br><strong>{st.session_state.secret_santa}!</strong> 🎁✨
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<p style="font-size: 1.2rem; color: white; margin-top: 2rem;">Spread some holiday magic! 🎅</p>', unsafe_allow_html=True)
            
            if st.button("🔄 Try Another Name", key="reset_btn"):
                st.session_state.revealed = False
                st.session_state.user_name = ""
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Secret Santa 🎅",
        page_icon="🎁",
        layout="wide"
    )
    main()
