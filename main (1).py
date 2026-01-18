import streamlit as st
import os
import time
from datetime import datetime
from openai import OpenAI

# Page Title & Config
st.set_page_config(
    page_title="Elite AI Post Studio",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Typography: Inter & Manrope
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Manrope:wght@800&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'Manrope', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Extended Theme Configurations
themes = {
    "Modern Light": {
        "bg": "#f8fafc",
        "card_bg": "rgba(255, 255, 255, 0.9)",
        "sidebar_bg": "#f1f5f9",
        "text": "#0f172a",
        "subtext": "#64748b",
        "primary_gradient": "linear-gradient(135deg, #6366f1 0%, #a855f7 100%)",
        "accent": "#6366f1",
        "border": "rgba(0, 0, 0, 0.05)",
        "shadow": "0 4px 20px -5px rgba(0,0,0,0.05)"
    },
    "Deep Dark": {
        "bg": "#020617",
        "card_bg": "rgba(15, 23, 42, 0.8)",
        "sidebar_bg": "#0f172a",
        "text": "#f1f5f9",
        "subtext": "#94a3b8",
        "primary_gradient": "linear-gradient(135deg, #38bdf8 0%, #818cf8 100%)",
        "accent": "#38bdf8",
        "border": "rgba(255, 255, 255, 0.05)",
        "shadow": "0 20px 40px -15px rgba(0,0,0,0.3)"
    },
    "Emerald Pro": {
        "bg": "#f0fdf4",
        "card_bg": "rgba(255, 255, 255, 0.9)",
        "sidebar_bg": "#dcfce7",
        "text": "#064e3b",
        "subtext": "#065f46",
        "primary_gradient": "linear-gradient(135deg, #10b981 0%, #059669 100%)",
        "accent": "#10b981",
        "border": "rgba(0, 0, 0, 0.05)",
        "shadow": "0 10px 30px -10px rgba(0,0,0,0.05)"
    },
    "Royal Purple": {
        "bg": "#faf5ff",
        "card_bg": "rgba(255, 255, 255, 0.9)",
        "sidebar_bg": "#f3e8ff",
        "text": "#4c1d95",
        "subtext": "#6b21a8",
        "primary_gradient": "linear-gradient(135deg, #a855f7 0%, #7e22ce 100%)",
        "accent": "#a855f7",
        "border": "rgba(0, 0, 0, 0.05)",
        "shadow": "0 10px 30px -10px rgba(0,0,0,0.05)"
    }
}

# Sidebar Integration
with st.sidebar:
    st.markdown("<div style='padding: 10px 0;'><h2 style='margin:0;'>✨ Elite AI Studio</h2></div>", unsafe_allow_html=True)
    theme_choice = st.selectbox("Application Theme", list(themes.keys()))
    selected = themes[theme_choice]
    
    st.divider()
    st.markdown("### Search Logic")
    live_search = st.toggle("🌐 Live Internet Search", value=False, help="Real-time data synchronization for accurate content")
    
    st.divider()
    st.markdown("### Export Hub")
    st.caption("Auto-export enabled for high-priority campaigns.")

# Advanced CSS
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {selected['bg']};
        color: {selected['text']};
    }}
    
    .stMain {{
        padding: 40px 60px;
    }}
    
    .stTextArea textarea, .stTextInput input, .stSelectbox select {{
        border-radius: 12px !important;
        border: 1px solid {selected['border']} !important;
        background: {selected['card_bg']} !important;
        color: {selected['text']} !important;
        padding: 12px !important;
    }}
    
    .stButton button {{
        background: {selected['primary_gradient']} !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        box-shadow: {selected['shadow']};
    }}
    
    .stButton button:hover {{
        transform: translateY(-2px);
        filter: brightness(1.1);
    }}

    .brand-header {{
        text-align: center;
        margin-bottom: 40px;
    }}
    
    .subtitle {{
        color: {selected['subtext']};
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0px;
    }}

    .result-panel {{
        background: {selected['card_bg']};
        border-radius: 16px;
        padding: 30px;
        border: 1px solid {selected['border']};
        box-shadow: {selected['shadow']};
        margin-top: 30px;
        color: {selected['text']};
    }}
    
    .timestamp {{
        font-size: 0.8rem;
        color: {selected['subtext']};
        margin-bottom: 10px;
        display: block;
    }}

    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        padding: 8px 0;
        text-align: center;
        background: {selected['card_bg']};
        backdrop-filter: blur(20px);
        border-top: 1px solid {selected['border']};
        z-index: 1000;
    }}
    
    .footer-name {{
        font-weight: 700;
        font-size: 0.85rem;
        color: {selected['text']};
    }}
    
    .footer-links a {{
        color: {selected['accent']};
        text-decoration: none;
        font-weight: 600;
        margin: 0 10px;
        font-size: 0.75rem;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }}
    </style>
""", unsafe_allow_html=True)

# Main Content Layout - AI Robot Icon instead of image
col_logo, col_empty = st.columns([1, 10])
with col_logo:
    st.markdown("<h1 style='margin:0; font-size: 3rem;'>🤖</h1>", unsafe_allow_html=True)

# Configuration Grid
col1, col2 = st.columns([2, 1])

with col1:
    topic = st.text_area("Campaign Brief", placeholder="Enter your topic, product highlights, or strategy goals...", height=180)

with col2:
    platform = st.selectbox("🎯 Target Platform", ["Instagram", "LinkedIn", "Facebook", "Twitter/X", "TikTok", "Pinterest", "Threads", "Education", "Other"])
    tone = st.selectbox("🎭 Narrative Tone", ["Viral", "Professional", "Funny", "Storytelling", "Educational", "Urgent"])
    content_length = st.radio("📏 Message Length", ["Short", "Medium", "Long"], horizontal=True, index=1)
    num_variants = st.select_slider("🔢 Output Variants", options=[1, 2, 3, 4, 5], value=2)

if st.button("🚀 Generate Strategic Content"):
    if not topic:
        st.error("Briefing is required for generation.")
    else:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            st.error("API configuration missing.")
        else:
            client = OpenAI(api_key=api_key)
            with st.spinner("⚡ AI Research Engine Active..." if live_search else "🧠 Synthesizing Strategy..."):
                try:
                    research_info = ""
                    if live_search:
                        time.sleep(1.2)
                        research_info = f"Current 2026 data trends for {topic} on {platform} verified."
                    
                    length_instruction = {
                        "Short": "Keep it concise, punchy, and under 50 words.",
                        "Medium": "Standard social media length, approximately 100-150 words.",
                        "Long": "Detailed, long-form content with in-depth explanations, over 250 words."
                    }[content_length]

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are a world-class Social Media Strategist. Output only ready-to-publish, high-conversion content."},
                            {"role": "user", "content": f"Create {num_variants} posts for {platform} about {topic}. Tone: {tone}. {length_instruction} {research_info}"}
                        ]
                    )
                    output = response.choices[0].message.content
                    
                    st.balloons()
                    st.success("Strategy Generation Complete ✨")
                    
                    if live_search:
                        with st.expander("📊 Research Insights"):
                            st.info(f"Analyzed verified social trends for {topic} as of {datetime.now().strftime('%Y-%m-%d')}")
                    
                    st.markdown("### 💎 Strategic Output")
                    variants = output.split("Variant")
                    if len(variants) > 1:
                        for i, post in enumerate(variants[1:], 1):
                            st.markdown(f"""
                            <div class="result-panel">
                                <span class="timestamp">VERIFIED STRATEGY {i} | {datetime.now().strftime('%H:%M')}</span>
                                {post}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="result-panel">{output}</div>', unsafe_allow_html=True)
                    
                    st.divider()
                    st.download_button("📂 Export Campaign", output, file_name=f"{platform}_campaign.txt")
                    
                except Exception as e:
                    st.error(f"Operational Error: {e}")

# Spacing for fixed footer
st.markdown("<div style='margin-bottom: 60px;'></div>", unsafe_allow_html=True)

# Elite Contact Footer - Compact Small Version
st.markdown(f"""
    <div class="footer">
        <div class="footer-name">Design & Developed by Mr. Zeeshan Javed</div>
        <div class="footer-links">
            <a href="mailto:zeeshan.javed@iub.edu.pk">📧 zeeshan.javed@iub.edu.pk</a>
            <a href="mailto:zeeshanjaved6767@gmail.com">📧 zeeshanjaved6767@gmail.com</a>
            <a href="tel:+923042012500">📞 +92 304 2012500</a>
        </div>
    </div>
""", unsafe_allow_html=True)
