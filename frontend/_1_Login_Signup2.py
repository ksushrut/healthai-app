import streamlit as st
from supabase_config import supabase

def show_login_signup():
    st.title("Welcome to HealthAI")

    # --- 1) Handle Google OAuth return: exchange ?code=... for a session ---
    qp = st.query_params
    code = qp.get("code")
    if code:
        # st.query_params values can be str or list; normalize
        if isinstance(code, list):
            code = code[0]
        try:
            # Try dict form first (supabase-py v2+); fallback to plain string
            try:
                res = supabase.auth.exchange_code_for_session({"auth_code": code})
            except TypeError:
                res = supabase.auth.exchange_code_for_session(code)

            user = res.user
            if user:
                # Optional: clear code from URL so refresh doesn't re-exchange
                st.query_params.clear()
                handle_authenticated_user(user)  # sets state & st.rerun()
                st.stop()
        except Exception as e:
            st.error(f"Google sign-in failed: {e}")

    # --- 2) If a session already exists (email login or after exchange), route away ---
    session = supabase.auth.get_session()
    if session and session.user:
        handle_authenticated_user(session.user)  # sets state & st.rerun()
        st.stop()

    # --- 3) Email Login/Signup UI ---
    option = st.radio("Choose an option", ["Login", "Signup"], key="login_signup_radio")

    with st.form(key=f"{option}_form"):
        email = st.text_input("Email", key=f"{option}_email")
        password = st.text_input("Password", type="password", key=f"{option}_password")
        submit_button = st.form_submit_button(option)

        if submit_button:
            if option == "Login":
                user = login_user(email, password)
                if user:
                    handle_authenticated_user(user)
                    st.stop()
            else:
                user = signup_user(email, password)
                if user:
                    post = supabase.auth.get_session()
                    if post and post.user:
                        handle_authenticated_user(post.user)
                        st.stop()
                    else:
                        st.info("Signup successful. Please check your email to confirm, then log in.")
                        st.stop()

    st.markdown("### Or")

    # --- 4) Google OAuth button ---
    # Remember the user's intent so the router can send new users to Profile
    st.session_state["oauth_intent"] = option  # "Login" or "Signup"

    # If you set Supabase Auth > URL Configuration > Site URL, you can omit redirect_to here.
    # If you want to override, put SITE_URL in st.secrets.
    opts = {"scopes": "email profile"}
    site_url = st.secrets.get("SITE_URL", None)
    if site_url:
        opts["redirect_to"] = site_url

    oauth = supabase.auth.sign_in_with_oauth({
        "provider": "google",
        "options": opts
    })

    st.link_button(f"Continue with Google ({option})", oauth.url)


# ---------------- Helpers ---------------- #
def login_user(email: str, password: str):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if res.session:
            return res.user
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
            # Ensure Users entry exists
            existing = supabase.table("Users").select("*").eq("UserID", user.id).execute()
            if not existing.data:
                supabase.table("Users").insert({
                    "UserID": user.id,
                    "email": user.email,
                    "auth_provider": "email"
                }).execute()
            return user
        st.error("Signup failed: No user returned.")
        return None
    except Exception as e:
        st.error(f"Signup failed: {e}")
        return None

def handle_authenticated_user(user):
    # Persist minimal identity
    st.session_state["logged_in"] = True
    st.session_state["user_id"] = user.id
    st.session_state["user_email"] = user.email

    # Upsert Users (helpful for Google logins with name metadata)
    try:
        full_name = (user.user_metadata or {}).get("full_name", "") or ""
        parts = full_name.split()
        first_name = parts[0] if parts else None
        last_name = parts[-1] if len(parts) > 1 else None
        provider = (user.app_metadata or {}).get("provider", "email")
        supabase.table("Users").upsert({
            "UserID": user.id,
            "email": user.email,
            "first_name": first_name,
            "last_name": last_name,
            "auth_provider": provider
        }).execute()
    except Exception:
        pass

    # Decide destination
    prof = supabase.table("User_Profiles").select("*").eq("UserID", user.id).execute()
    has_profile = bool(prof.data)

    intent = st.session_state.get("oauth_intent")
    if intent == "Signup" and not has_profile:
        st.session_state["profile_filled"] = False
        st.session_state["current_page"] = "_2_Profile"
    else:
        st.session_state["profile_filled"] = has_profile
        st.session_state["current_page"] = "_3_Dashboard" if has_profile else "_2_Profile"

    st.rerun()
