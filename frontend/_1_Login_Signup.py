# pages/1_Login_Signup.py
import streamlit as st
from supabase_config import supabase

def show_login_signup():
    st.title("Welcome to HealthAI")

    # --- Check active session ---
    session = supabase.auth.get_session()
    if session and session.user:
        handle_authenticated_user(session.user)
        return

    # --- Login/Signup selection ---
    option = st.radio("Choose an option", ["Login", "Signup"], key="login_signup_radio")

    # --- Form for email/password ---
    with st.form(key=f"{option}_form"):
        email = st.text_input("Email", key=f"{option}_email")
        password = st.text_input("Password", type="password", key=f"{option}_password")
        submit_button = st.form_submit_button(option)

        if submit_button:
            if option == "Login":
                user = login_user(email, password)
                if user:
                    userAccess = handle_authenticated_user(user)
            elif option == "Signup":
                user = signup_user(email, password)
                if user:
                    handle_authenticated_user(user)
        


# ---------------- Helper Functions ---------------- #
def login_user(email: str, password: str):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if res.session:
            return res.user
        else:
            st.error("Invalid credentials.")
            return None
    except Exception as e:
        st.error(f"Login failed: {e}")
        return None

def signup_user(email: str, password: str):
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        user = res.user
        if user:
            st.success("Signup successful!")
            # Insert user into Users table if not exists
            existing = supabase.table("Users").select("*").eq("UserID", user.id).execute()
            if not existing.data:
                supabase.table("Users").insert({
                    "UserID": user.id,
                    "email": user.email,
                    "auth_provider": "email"
                }).execute()
            return user
        else:
            st.error("Signup failed: No user returned.")
            return None
    except Exception as e:
        st.error(f"Signup failed: {e}")
        return None

def handle_authenticated_user(user):
    # Save auth info
    st.session_state.logged_in = True
    st.session_state.user_id = user.id
    st.session_state.user_email = user.email

    # Decide destination
    profile = supabase.table("User_Profiles").select("*").eq("UserID", user.id).execute()
    st.session_state.profile_filled = bool(profile.data)
    st.session_state.current_page = "_3_Dashboard" if st.session_state.profile_filled else "_2_Profile"

    # 🔑 Trigger a fresh run so the top-level router executes immediately
    st.rerun()

    

    
