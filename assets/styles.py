import streamlit as st
import random

CSS = """
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
    
    /* FIXED: Room input visibility at TOP */
    .room-input-section {
        background: rgba(255,255,255,0.98) !important;
        padding: 3rem !important;
        border-radius: 30px !important;
        margin: 2rem auto !important;
        max-width: 900px !important;
        box-shadow: 0 40px 120px rgba(0,0,0,0.5) !important;
        border: 4px solid rgba(255,255,255,0.9) !important;
        text-align: center;
    }
    
    .room-input-section * {
        color: #1f2937 !important;
        text-shadow: none !important;
    }
    
    .room-input-section [data-baseweb="input"] {
        padding: 1.5rem 2rem !important;
        font-size: 1.6rem !important;
        border: 3px solid #b91c1c !important;
        border-radius: 25px !important;
        background: #ffffff !important;
        margin-bottom: 1rem !important;
        font-weight: 600 !important;
    }
    
    .room-input-section .stButton > button {
        background: linear-gradient(45deg, #b91c1c, #dc2626) !important;
        padding: 1.5rem 4rem !important;
        font-size: 1.4rem !important;
        border-radius: 30px !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
    }
    
    /* ✅ REPLACE the universal selector with these SPECIFIC overrides */
[data-testid="stAppViewContainer"], 
.main .block-container,
.stApp > header {
    color: #ffffff !important;
}

[data-testid="stMarkdownContainer"] p, 
h1, h2, h3, .stMarkdown {
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
    
    /* [Rest of CSS classes - title, buttons, reveal-box, etc. - SAME as original] */
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
    }
    
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
        box-shadow: 
            0 80px 200px rgba(0,0,0,0.7),
            inset 0 8px 50px rgba(255,255,255,0.95) !important;
        border: 8px solid rgba(185,28,28,0.3) !important;
        animation: revealAnim 3.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards !important;
    }
    
    @keyframes revealAnim {
        0% { opacity: 0; transform: scale(0.1) rotateY(180deg); }
        50% { opacity: 0.95; transform: scale(1.15) rotateY(0deg); }
        100% { opacity: 1; transform: scale(1) rotateY(0deg); }
    }
    
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
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    
    .status-card {
        background: rgba(255,255,255,0.98) !important;
        padding: 4rem !important;
        border-radius: 35px !important;
        margin: 2.5rem 0 !important;
        border: 4px solid rgba(255,255,255,0.95) !important;
        color: #1f2937 !important;
        box-shadow: 0 45px 120px rgba(0,0,0,0.5) !important;
    }
    
    .snowflake {
    color: #ffffff !important;              /* Pure white */
    text-shadow: none !important;           /* No glow */
    position: fixed;
    top: -50px;                             /* Start higher */
    animation: fall linear infinite;
    pointer-events: none;
    z-index: 200;                           /* Lower z-index */
    opacity: 0.8 !important;
}

@keyframes fall {
    to { 
        transform: translateY(120vh) rotate(720deg);  /* Gentler spin */
    }
}
"""

def load_css():
    """Load complete CSS styles"""
    return CSS

def create_effects():
    """Create Christmas effects (lights + snowflakes)"""
    # Paste the create_christmas_effects() function from original code
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
    
    for i in range(40):
        effects_html += f"""
        <div class="snowflake" style="
            left: {random.randint(0, 100)}vw;
            animation-delay: {random.uniform(0, 20)}s;
            animation-duration: {random.uniform(25, 50)}s;
            font-size: {random.choice(['1rem', '1.2rem', '1.5rem', '1.8rem'])};
            opacity: {random.uniform(0.6, 0.9)};
        ">❄</div>
        """
    return effects_html
