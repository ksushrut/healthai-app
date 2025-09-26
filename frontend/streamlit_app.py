# streamlit_app.py
import os
import streamlit as st

st.set_page_config(page_title="HealthAI", page_icon="💪", layout="wide")

# Make GOOGLE_API_KEY available from secrets if present (non-fatal if missing)
if not os.getenv("GOOGLE_API_KEY"):
    try:
        k = st.secrets.get("GOOGLE_API_KEY", None)
        if k:
            os.environ["GOOGLE_API_KEY"] = k
    except Exception:
        pass

# ---- Import pages ----
# Login: keep your file/code unchanged; we just call show_login_signup()
from _1_Login_Signup2 import show_login_signup

# Profile and Dashboard renderers
try:
    from _2_Profile import render_profile
except Exception as e:
    def render_profile():
        st.error(f"Could not import render_profile from _2_Profile.py: {e}")

try:
    from _3_Dashboard import render_dashboard
except Exception as e:
    def render_dashboard():
        st.error(f"Could not import render_dashboard from _3_Dashboard.py: {e}")


def _resolve_route() -> str:
    """
    Decide which page to show (no sidebar).
    - If not logged in -> login
    - If logged in and profile not filled -> profile
    - Else -> dashboard
    """
    if not st.session_state.get("logged_in"):
        return "_1_Login_Signup2"

    # Prefer whatever your login handler set. Otherwise infer.
    current = st.session_state.get("current_page")
    if current:
        return current

    if st.session_state.get("profile_filled"):
        return "_3_Dashboard"
    return "_2_Profile"


def main():
    route = _resolve_route()

    if route == "_1_Login_Signup2":
        # Your own login page sets:
        #   st.session_state["logged_in"] = True
        #   st.session_state["user_id"]   = <uuid>
        #   st.session_state["user_email"] = <email>
        #   st.session_state["current_page"] = "_2_Profile" or "_3_Dashboard"
        #   (in handle_authenticated_user())
        show_login_signup()
        return

    if route == "_2_Profile":
        # Guard: if someone hits this URL directly without login, bounce to login
        if not st.session_state.get("logged_in"):
            st.session_state["current_page"] = "_1_Login_Signup2"
            st.rerun()
        render_profile()
        return

    if route == "_3_Dashboard":
        # Guard: must be logged in
        if not st.session_state.get("logged_in"):
            st.session_state["current_page"] = "_1_Login_Signup2"
            st.rerun()
        render_dashboard()
        return

    # Fallback
    st.error("Unknown route. Redirecting to login…")
    st.session_state["current_page"] = "_1_Login_Signup2"
    st.rerun()


if __name__ == "__main__":
    main()
