import streamlit as st

# Simple in-memory users (temporary)
if "users" not in st.session_state:
    st.session_state.users = {
        "admin": "1234"
    }

def login():
    st.subheader("🔐 Login to ScriptNest")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("✅ Login Successful")
            st.rerun()
        else:
            st.error("❌ Invalid credentials")

def signup():
    st.subheader("📝 Create Account")

    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")

    if st.button("Sign Up"):
        if new_user in st.session_state.users:
            st.warning("⚠️ User already exists")
        else:
            st.session_state.users[new_user] = new_pass
            st.success("✅ Account created! Please login.")
