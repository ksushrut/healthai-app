# _2_Profile.py
import streamlit as st
from supabase_config import supabase

def _load_existing_profile(user_id: str):
    try:
        resp = (
            supabase
            .table("User_Profiles")
            .select("*")
            .eq("UserID", user_id)
            .limit(1)
            .execute()
        )
        rows = resp.data or []
        return rows[0] if rows else None
    except Exception:
        return None

def _upsert_profile(user_id: str, payload: dict):
    # Ensure UserID is present in payload for upsert-by-constraint uniqueness
    payload = {"UserID": user_id, **payload}
    return supabase.table("User_Profiles").upsert(payload).execute()

def render_profile():
    # Hard gate: must be logged in
    if not st.session_state.get("logged_in") or not st.session_state.get("user_id"):
        st.session_state["current_page"] = "_1_Login_Signup2"
        st.rerun()

    st.title("Profile")

    user_id = st.session_state["user_id"]

    # Prefill from DB or session
    db_profile = _load_existing_profile(user_id)
    ss_profile = st.session_state.get("profile", {})

    defaults = {
        "first_name": (ss_profile.get("first_name") or (db_profile or {}).get("first_name") or ""),
        "last_name":  (ss_profile.get("last_name")  or (db_profile or {}).get("last_name")  or ""),
        "height_cm":  (ss_profile.get("height_cm")  or (db_profile or {}).get("height_cm")  or 170),
        "weight_kg":  (ss_profile.get("weight_kg")  or (db_profile or {}).get("weight_kg")  or 70),
        "sex":        (ss_profile.get("sex")        or (db_profile or {}).get("sex")        or "Male"),
        "goal":       (ss_profile.get("goal")       or (db_profile or {}).get("goal")       or "Weight Loss"),
        "allergies":  (ss_profile.get("allergies")  or (db_profile or {}).get("allergies")  or ""),
        "dietary_preferences": (ss_profile.get("dietary_preferences") or (db_profile or {}).get("dietary_preferences") or "Vegetarian"),
        "activity_level":      (ss_profile.get("activity_level")      or (db_profile or {}).get("activity_level")      or "Moderate"),
    }

    with st.form("profile_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            first_name = st.text_input("First name", value=str(defaults["first_name"]))
            height_cm  = st.number_input("Height (cm)", min_value=50, max_value=250, step=1,
                                         value=int(defaults["height_cm"]))
            sex        = st.selectbox("Sex", ["Male", "Female", "Other"],
                                      index=["Male","Female","Other"].index(defaults["sex"]) if defaults["sex"] in ["Male","Female","Other"] else 0)
            allergies  = st.text_input("Allergies (comma-separated)", value=str(defaults["allergies"]))
        with c2:
            last_name  = st.text_input("Last name", value=str(defaults["last_name"]))
            weight_kg  = st.number_input("Weight (kg)", min_value=20, max_value=300, step=1,
                                         value=int(defaults["weight_kg"]))
            goal       = st.selectbox("Primary Goal", ["Weight Loss", "Muscle Gain", "Maintenance"],
                                      index=["Weight Loss","Muscle Gain","Maintenance"].index(defaults["goal"]) if defaults["goal"] in ["Weight Loss","Muscle Gain","Maintenance"] else 0)
            dietary_preferences = st.text_input("Dietary Preferences", value=str(defaults["dietary_preferences"]))

        activity_level = st.selectbox(
            "Activity Level",
            ["Sedentary","Light","Moderate","Active","Athlete"],
            index=["Sedentary","Light","Moderate","Active","Athlete"].index(defaults["activity_level"]) if defaults["activity_level"] in ["Sedentary","Light","Moderate","Active","Athlete"] else 2
        )

        submitted = st.form_submit_button("Save & Continue")

    if submitted:
        profile_payload = {
            "first_name": first_name.strip(),
            "last_name": last_name.strip(),
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "sex": sex,
            "goal": goal,
            "allergies": allergies.strip(),
            "dietary_preferences": dietary_preferences.strip(),
            "activity_level": activity_level,
        }

        # Save to DB
        try:
            _upsert_profile(user_id, profile_payload)
            st.success("Profile saved.")
        except Exception as e:
            st.error(f"Failed to save profile to database: {e}")
            # still keep session copy so user can continue
        finally:
            # Keep a local session copy for the Dashboard (fast access for LLM)
            st.session_state["profile"] = profile_payload
            st.session_state["profile_filled"] = True
            st.session_state["current_page"] = "_3_Dashboard"
            st.rerun()

    # If a profile already exists, offer a quick continue
    if db_profile or st.session_state.get("profile_filled"):
        if st.button("Go to Dashboard"):
            st.session_state["current_page"] = "_3_Dashboard"
            st.rerun()
