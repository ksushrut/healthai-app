import streamlit as st
from _1_Login_Signup import show_login_signup
from _2_Profile import show_profile
from _3_Dashboard import show_dashboard
from supabase_config import supabase


# --- Initialize session state ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "profile_filled" not in st.session_state:
    st.session_state.profile_filled = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "_1_Login_Signup"
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None


# --- Check Supabase session (Google or Email) ---
session = supabase.auth.get_session()
if session and not st.session_state.logged_in:
    user = session.user

    # Record / update user in Users table
    supabase.table("Users").upsert({
        "UserID": user.id,
        "email": user.email,
        "first_name": (user.user_metadata.get("full_name", "").split(" ")[0]
                       if user.user_metadata and user.user_metadata.get("full_name") else None),
        "last_name": (user.user_metadata.get("full_name", "").split(" ")[-1]
                      if user.user_metadata and user.user_metadata.get("full_name") else None),
        "auth_provider": "google" if user.app_metadata.get("provider") == "google" else "email"
    }).execute()

    # Save session state
    st.session_state.logged_in = True
    st.session_state.user_id = user.id
    st.session_state.user_email = user.email

    # Decide navigation
    if st.session_state.get("oauth_intent") == "Signup":
        st.session_state.current_page = "_2_Profile"
    else:
        profile_check = supabase.table("User_Profiles").select("*").eq("UserID", user.id).execute()
        if profile_check.data:
            st.session_state.profile_filled = True
            st.session_state.current_page = "_3_Dashboard"
        else:
            st.session_state.profile_filled = False
            st.session_state.current_page = "_2_Profile"


# --- Router ---
if st.session_state.current_page == "_1_Login_Signup":
    show_login_signup()

elif st.session_state.current_page == "_2_Profile":
    show_profile()

elif st.session_state.current_page == "_3_Dashboard":
    show_dashboard()
