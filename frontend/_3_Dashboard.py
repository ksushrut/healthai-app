import streamlit as st
from supabase_config import supabase

def show_dashboard():
    if not st.session_state.get("logged_in", False):
        st.session_state["current_page"] = "_1_Login_Signup2"
        st.warning("Please login first.")
        st.stop()

    st.title("🏋️‍♂️ HealthAI Dashboard")
    st.write(f"Welcome, {st.session_state.get('user_email', 'User')}!")

    if st.button("Logout"):
        try:
            supabase.auth.sign_out()
        except Exception as e:
            st.info(f"Sign-out note: {e}")

        st.session_state["logged_in"] = False
        st.session_state["profile_filled"] = False
        st.session_state["user_id"] = None
        st.session_state["user_email"] = None
        st.session_state["oauth_intent"] = None

        st.session_state["current_page"] = "_1_Login_Signup2"
        st.rerun()
