import streamlit as st
from claude_handler import generate_script, estimate_read_time

st.set_page_config(
    page_title="ScriptNest – YouTube Script Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Sidebar using native Streamlit elements ────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:32px;padding:4px 0;">
        <svg width="38" height="38" viewBox="0 0 36 36" fill="none">
            <ellipse cx="18" cy="25" rx="14" ry="6.5" stroke="#4B35C4" stroke-width="1.8" fill="none"/>
            <ellipse cx="18" cy="25" rx="9" ry="4" stroke="#C0476E" stroke-width="1.4" fill="none"/>
            <path d="M14 17 L22 21 L14 25 Z" fill="#E8351A"/>
            <line x1="22" y1="10" x2="23.5" y2="7" stroke="#E8351A" stroke-width="1.4" stroke-linecap="round"/>
        </svg>
        <span style="font-size:20px;font-weight:700;font-family:Inter,sans-serif;">
            <span style="color:#4B35C4;">Script</span><span style="color:#E8351A;">Nest</span>
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sn-nav-item sn-nav-active">🏠 &nbsp; Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sn-nav-item">🕐 &nbsp; History</div>', unsafe_allow_html=True)
    st.markdown('<div class="sn-nav-item">📄 &nbsp; Saved Scripts</div>', unsafe_allow_html=True)
    st.markdown('<div class="sn-nav-item">📋 &nbsp; Templates</div>', unsafe_allow_html=True)
    st.markdown('<div class="sn-nav-item">❓ &nbsp; Help</div>', unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sn-topbar">
    <h1 class="sn-title">YouTube Script Generator</h1>
    <p class="sn-subtitle">Create engaging, well-structured scripts for your YouTube videos in seconds</p>
</div>
""", unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1.2], gap="large")

with left_col:
    st.markdown('<p class="sn-panel-title">Video Details</p>', unsafe_allow_html=True)
    st.markdown('<p class="sn-panel-sub">Provide some details about your video topic and let AI create a compelling script for you.</p>', unsafe_allow_html=True)

    topic = st.text_input("Video Topic *", placeholder="e.g., How to Stay Productive While Working From Home", max_chars=100)
    audience = st.text_input("Target Audience", placeholder="e.g., Students, Entrepreneurs, Content Creators...", max_chars=100)
    length = st.selectbox("Video Length", ["3 – 5 Minutes", "8 – 10 Minutes (Recommended)", "12 – 15 Minutes", "20+ Minutes (Long Form)"], index=1)
    tone = st.selectbox("Tone", ["Friendly & Informative", "Energetic & Enthusiastic", "Educational & Professional", "Conversational & Casual", "Humorous & Entertaining", "Inspirational & Motivational"])
    keypoints = st.text_area("Key Points (Optional)", placeholder="Add any key points you want to include...", height=100, max_chars=500)
    language = st.selectbox("Language", ["English", "Hindi", "Spanish", "French", "Portuguese", "German"])
    generate_btn = st.button("✨ Generate Script", use_container_width=True, type="primary")

with right_col:
    st.markdown('<p class="sn-panel-title">Your Generated Script</p>', unsafe_allow_html=True)
    st.markdown("<p class='sn-panel-sub'>Here's your custom YouTube script. You can copy or download it.</p>", unsafe_allow_html=True)

    if generate_btn:
        if not topic.strip():
            st.warning("⚠️ Please enter a video topic first.")
        else:
            script_placeholder = st.empty()
            full_script = ""
            with st.spinner("ScriptNest is writing your script..."):
                for chunk in generate_script(
                    topic=topic, tone=tone, duration=length,
                    audience=audience if audience else "general YouTube viewers",
                    extra=keypoints, language=language,
                ):
                    full_script += chunk
                    script_placeholder.markdown(f'<div class="sn-script-box">{full_script}▌</div>', unsafe_allow_html=True)

            script_placeholder.markdown(f'<div class="sn-script-box">{full_script}</div>', unsafe_allow_html=True)

            st.divider()
            word_count = len(full_script.split())
            speak_time = estimate_read_time(full_script)
            st.markdown(f'<div class="sn-footer-stats">Total Length: <strong>{speak_time}</strong> &nbsp;|&nbsp; Word Count: <strong>~{word_count:,}</strong></div>', unsafe_allow_html=True)

            clean_topic = "".join(c for c in topic if c.isalnum() or c in " _-").strip()[:40]
            st.download_button(
                label="⬇️ Download Script (.txt)",
                data=f"ScriptNest\nTopic: {topic}\nTone: {tone}\nDuration: {length}\nWords: {word_count}\n\n{'='*50}\n\n{full_script}",
                file_name=f"script_{clean_topic.replace(' ','_')}.txt",
                mime="text/plain",
                use_container_width=True,
            )
            st.session_state.update({"last_script": full_script, "last_topic": topic, "last_words": word_count, "last_time": speak_time})

    elif "last_script" in st.session_state:
        st.info(f"📌 Previously generated script for: **{st.session_state['last_topic']}**")
        st.markdown(f'<div class="sn-script-box">{st.session_state["last_script"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sn-footer-stats">Total Length: <strong>{st.session_state["last_time"]}</strong> &nbsp;|&nbsp; Word Count: <strong>~{st.session_state["last_words"]:,}</strong></div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="sn-empty-state">
            <div class="sn-empty-icon">🎬</div>
            <h3>Your script will appear here</h3>
            <p>Fill in the details on the left and click <strong>Generate Script</strong> to get started.</p>
        </div>
        """, unsafe_allow_html=True)
