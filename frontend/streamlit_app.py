import streamlit as st
from _1_Login_Signup2 import show_login_signup
from _2_Profile import show_profile
from _3_Dashboard import show_dashboard
from supabase_config import supabase

st.set_page_config(page_title="HealthAI", page_icon="🩺", layout="wide")

# --- Init session state ---
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("profile_filled", False)
st.session_state.setdefault("current_page", "_1_Login_Signup2")
st.session_state.setdefault("user_id", None)
st.session_state.setdefault("user_email", None)
st.session_state.setdefault("oauth_intent", None)  # "Login" or "Signup"

def go(page_name: str) -> None:
    st.session_state["current_page"] = page_name
    st.rerun()

# --- If a valid Supabase session exists and we aren't marked logged in yet, hydrate state & route ---
session = supabase.auth.get_session()
if session and not st.session_state["logged_in"]:
    user = session.user

    # Upsert Users (safe for both email & Google)
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

    st.session_state["logged_in"] = True
    st.session_state["user_id"] = user.id
    st.session_state["user_email"] = user.email

    has_profile = bool(
        supabase.table("User_Profiles").select("*").eq("UserID", user.id).execute().data
    )

    if st.session_state.get("oauth_intent") == "Signup" and not has_profile:
        st.session_state["profile_filled"] = False
        go("_2_Profile")
    else:
        st.session_state["profile_filled"] = has_profile
        go("_3_Dashboard" if has_profile else "_2_Profile")

# --- Router ---
ROUTES = {
    "_1_Login_Signup2": show_login_signup,
    "_2_Profile": show_profile,
    "_3_Dashboard": show_dashboard,
}

ROUTES.get(st.session_state["current_page"], show_login_signup)()
