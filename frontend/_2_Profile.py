import streamlit as st
from supabase_config import supabase

def show_profile():
    if not st.session_state.get("logged_in", False):
        st.session_state["current_page"] = "_1_Login_Signup2"
        st.warning("Please login first.")
        st.stop()

    user_id = st.session_state.get("user_id")
    st.title("📝 Complete Your Profile")

    profile = supabase.table("User_Profiles").select("*").eq("UserID", user_id).execute()
    existing = profile.data[0] if profile.data else {}

    height = st.number_input("Height (cm)", value=existing.get("height_cm", 170))
    weight = st.number_input("Weight (kg)", value=existing.get("weight_kg", 70))
    sex = st.selectbox("Sex", ["male", "female", "other"],
                       index=["male","female","other"].index(existing.get("sex","male")))
    goal = st.selectbox("Goal", ["weight_loss","muscle_gain","maintenance"],
                        index=["weight_loss","muscle_gain","maintenance"].index(existing.get("goal","weight_loss")))

    if st.button("Save Profile"):
        supabase.table("User_Profiles").upsert({
            "UserID": user_id,
            "height_cm": height,
            "weight_kg": weight,
            "sex": sex,
            "goal": goal
        }).execute()

        st.session_state["profile_filled"] = True
        st.session_state["current_page"] = "_3_Dashboard"
        st.rerun()
