# logintest.py
import streamlit as st
from supabase_config import supabase

# ---------------- Initialize session state ---------------- #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "profile_filled" not in st.session_state:
    st.session_state.profile_filled = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# ---------------- Top-level page logic ---------------- #
if st.session_state.logged_in:
    if st.session_state.profile_filled:
        st.title("Dashboard")
        st.success(f"Welcome back, {st.session_state.user_email}!")
    else:
        st.title("Complete Your Profile")
        st.info(f"Hello {st.session_state.user_email}, please complete your profile.")
else:
    st.title("Login to HealthAI")
    with st.form(key="login_form"):
        email = st.text_input("Email", key="email_input")
        password = st.text_input("Password", type="password", key="password_input")
        submit = st.form_submit_button("Login")

        if submit:
            # Attempt login
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                if res.session:
                    user = res.user
                    # Update session state
                    st.session_state.logged_in = True
                    st.session_state.user_email = user.email

                    # Check if user has a profile
                    profile = supabase.table("User_Profiles").select("*").eq("UserID", user.id).execute()
                    st.session_state.profile_filled = bool(profile.data)

                    # Need to manually rerun, once the credentials are authenticated, else throw an error for invalid details
                    st.rerun()
                else:
                    st.error("Invalid email or password.")

            except Exception as e:
                st.error(f"Login failed: {e}")
