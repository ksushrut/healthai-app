import streamlit as st
import sys
sys.path.append("/Users/arunabalajee/Documents/Healthai-app")
from supabase_config import supabase

def show_dashboard():
    if not st.session_state.get("logged_in", False):
        st.session_state.current_page = "login_signup"
        st.warning("Please login first.")
        st.stop()

    st.title("🏋️‍♂️ HealthAI Dashboard")
    st.write(f"Welcome, {st.session_state.get('user_email','User')}!")

    if st.button("Logout"):
        #st.session_state.clear()
        st.session_state.current_page = "_1_Login_Signup"