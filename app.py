import streamlit as st
from claude_handler import generate_script, estimate_read_time
import time
import base64

# ── Page Config ─────────────────────────
st.set_page_config(page_title="ScriptNest AI", page_icon="🎬", layout="wide")

# ── Load Logo (FIXED) ─────────────────────────
def get_base64_logo():
    with open("logo.png", "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = get_base64_logo()

# ── Custom CSS (🔥 Premium UI) ─────────────────────────
st.markdown("""
<style>

/* Background */
body {
    background: linear-gradient(135deg, #020617, #0f172a);
}

/* Navbar */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 24px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border-radius: 14px;
    margin-bottom: 25px;
}

/* Logo */
.logo {
    display: flex;
    align-items: center;
    gap: 12px;
}
.logo img {
    height: 50px;
}
.logo span {
    font-size: 1.6rem;
    font-weight: bold;
    background: linear-gradient(90deg, #ff4d4d, #9333ea);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Hero */
.hero {
    text-align: center;
    margin-top: 10px;
    animation: fadeIn 1.2s ease-in;
}
.hero h1 {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #ff4d4d, #9333ea);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p {
    color: #94a3b8;
    font-size: 1.1rem;
}

/* Card */
.card {
    background: rgba(255,255,255,0.05);
    padding: 22px;
    border-radius: 16px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    margin-top: 20px;
}

/* Output */
.output-box {
    background: #020617;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #334155;
    color: #e2e8f0;
    font-family: monospace;
    white-space: pre-wrap;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #ff4d4d, #9333ea);
    color: white;
    border-radius: 12px;
    height: 48px;
    font-weight: bold;
    font-size: 16px;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #020617;
}

/* Animation */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(-20px);}
    to {opacity: 1; transform: translateY(0);}
}

</style>
""", unsafe_allow_html=True)

# ── Navbar ─────────────────────────
st.markdown(f"""
<div class="navbar">
    <div class="logo">
        <img src="data:image/png;base64,{logo_base64}">
        <span>ScriptNest</span>
    </div>
    <div style="color:#94a3b8;">AI Script Generator ⚡</div>
</div>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────
st.markdown("""
<div class="hero">
<h1>Create Viral YouTube Scripts 🚀</h1>
<p>Powered by AI • Fast • Smart • Creator-Friendly</p>
</div>
""", unsafe_allow_html=True)

# ── Input Section ─────────────────────────
col1, col2 = st.columns([3,1])

with col1:
    topic = st.text_input("🎯 Enter your video topic")

with col2:
    st.write("")
    st.write("")
    generate = st.button("✨ Generate Script")

st.markdown('</div>', unsafe_allow_html=True)

# ── Sidebar ─────────────────────────
with st.sidebar:
    st.image("logo.png", use_container_width=True)
    st.header("⚙️ Settings")

    tone = st.selectbox("Tone", ["Energetic", "Educational", "Casual", "Professional"])
    duration = st.selectbox("Length", ["Short", "Medium", "Long"])
    audience = st.text_input("Audience")
    extra = st.text_area("Extra Instructions")

# ── Generate Script ─────────────────────────
if generate:
    if not topic:
        st.warning("⚠️ Enter topic first")
    else:
        script_box = st.empty()
        full_script = ""

        # 🔥 AUTO LANGUAGE DETECTION (ONLY ADDITION)
        if "hindi" in topic.lower():
            language_instruction = "Write the script in Hindi (Devanagari script)."
        else:
            language_instruction = "Write the script in English."

        with st.spinner("🔥 AI is creating magic..."):
            for chunk in generate_script(
                topic, tone, duration,
                audience or "general audience",
                extra + "\n" + language_instruction
            ):
                full_script += chunk
                script_box.markdown(
                    f'<div class="output-box">{full_script}▌</div>',
                    unsafe_allow_html=True
                )
                time.sleep(0.01)

        script_box.markdown(
            f'<div class="output-box">{full_script}</div>',
            unsafe_allow_html=True
        )

        # ── Analytics ─────────────────────────
        st.markdown("### 📊 Analytics")

        col1, col2 = st.columns(2)
        col1.metric("Words", len(full_script.split()))
        col2.metric("Read Time", estimate_read_time(full_script))

        # Download
        st.download_button("📥 Download Script", full_script)

else:
    st.info("👆 Enter topic to generate script")
