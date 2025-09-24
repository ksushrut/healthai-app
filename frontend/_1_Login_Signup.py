# pages/1_Login_Signup.py
import streamlit as st
import sys
import webbrowser
import time
from streamlit_supabase_auth import login_form, logout_button
from supabase import create_client

sys.path.append("/Users/arunabalajee/Documents/Healthai-app")
from supabase_config import supabase



def show_login_signup():
    st.title("Welcome to HealthAI")

    # --- Check if user already has an active session ---
    session = supabase.auth.get_session()
    if session and session.user:
        handle_authenticated_user(session.user)
        return

    # --- Choose Login or Signup ---
    option = st.radio("Choose an option", ["Login", "Signup"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # --- Signup with Email ---
    if option == "Signup":
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        if st.button("Sign Up with Email"):
            signup_with_email(email, password, first_name, last_name)

    # --- Login with Email ---
    elif option == "Login":
        if st.button("Login with Email"):
            login_with_email(email, password)

    st.markdown("---")
    st.subheader("Or")

    # --- Google Authentication ---
    if st.button("Continue with Google"):
        google_oauth_login()

    # --- Poll for session after OAuth redirect ---
    if "oauth_polling_done" not in st.session_state:
        st.session_state.oauth_polling_done = True
        session = supabase.auth.get_session()
        if session and session.user:
            handle_authenticated_user(session.user)


# ---------------- Helper Functions ---------------- #

def signup_with_email(email, password, first_name, last_name):
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        user = res.user
        if user:
            supabase.table("Users").insert({
                "UserID": user.id,
                "email": user.email,
                "first_name": first_name,
                "last_name": last_name,
                "auth_provider": "email"
            }).execute()
            st.success("Signup successful! Please log in.")
            st.session_state.current_page = "_1_Login_Signup"
        else:
            st.error("Signup failed: No user returned.")
    except Exception as e:
        st.error(f"Signup failed: {e}")


def login_with_email(email, password):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if res.session:
            handle_authenticated_user(res.user)
            user = res.user
            st.session_state.logged_in = True
            st.session_state.user_id = user.id
            st.session_state.user_email = user.email
            profile_check = supabase.table("User_Profiles").select("*").eq("UserID", user.id).execute()
            if profile_check.data:
                st.session_state.profile_filled = True
                st.session_state.current_page = "_3_Dashboard"
            else:
                st.session_state.profile_filled = False
                st.session_state.current_page = "_2_Profile"
        else:
            st.error("Login failed")
    except Exception as e:
        st.error(f"Login failed: {e}")


def google_oauth_login():
    res = supabase.auth.sign_in_with_oauth({
        "provider": "google",
        "options": {
            "redirect_to": "http://localhost:8501"  # minimal page to close tab
        }
    })
    # Open in browser tab; user completes login
    webbrowser.open(res.url, new=1, autoraise=True)
    st.info("Google login window opened. Please complete login.")

# --- Check session after redirect ---
session = supabase.auth.get_session()
if session and session.user:
    user = session.user
    st.session_state.logged_in = True
    st.session_state.user_id = user.id
    st.session_state.user_email = user.email

    # Ensure user exists in Users table
    existing_user = supabase.table("Users").select("*").eq("UserID", user.id).execute()
    if not existing_user.data:
        supabase.table("Users").insert({
            "UserID": user.id,
            "email": user.email,
            "first_name": user.user_metadata.get("full_name", "").split(" ")[0],
            "last_name": " ".join(user.user_metadata.get("full_name", "").split(" ")[1:]),
            "auth_provider": "google"
        }).execute()

    # Decide where to go
    profile_check = supabase.table("User_Profiles").select("*").eq("UserID", user.id).execute()
    if profile_check.data:
        st.session_state.profile_filled = True
        st.session_state.current_page = "_3_Dashboard"
    else:
        st.session_state.profile_filled = False
        st.session_state.current_page = "_2_Profile"


def handle_authenticated_user(user):
    st.session_state.logged_in = True
    st.session_state.user_id = user.id
    st.session_state.user_email = user.email

    # Check if user exists in Users table
    existing_user = supabase.table("Users").select("*").eq("UserID", user.id).execute()
    if not existing_user.data:
        # New user: insert into Users table
        full_name = user.user_metadata.get("full_name", "")
        first_name = full_name.split(" ")[0] if full_name else ""
        last_name = " ".join(full_name.split(" ")[1:]) if full_name else ""
        supabase.table("Users").insert({
            "UserID": user.id,
            "email": user.email,
            "first_name": first_name,
            "last_name": last_name,
            "auth_provider": "google"
        }).execute()
        st.success(f"New user {user.email} added to Users table!")
    else:
        st.info(f"Welcome back, {user.email}!")

    # Check if profile exists
    profile_check = supabase.table("User_Profiles").select("*").eq("UserID", user.id).execute()
    if profile_check.data:
        st.session_state.profile_filled = True
        st.session_state.current_page = "_3_Dashboard"
    else:
        st.session_state.profile_filled = False
        st.session_state.current_page = "_2_Profile"


# ---------------- Call Function ---------------- #
show_login_signup()
