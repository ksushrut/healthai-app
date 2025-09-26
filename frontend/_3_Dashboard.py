# _3_Dashboard.py
import os
import streamlit as st

def _get_gemini_model():
    """Reuse your getUserDetails helper if present; else fallback to google-generativeai."""
    # Try a helper from getUserDetails.py (optional)
    try:
        from getUserDetails import get_gemini_model  # if you defined it there
        model = get_gemini_model()
        if model:
            return model
    except Exception:
        pass

    # Fallback local config
    import google.generativeai as genai
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        # Try st.secrets if not copied to env yet
        try:
            key = st.secrets.get("GOOGLE_API_KEY", None)
            if key:
                os.environ["GOOGLE_API_KEY"] = key
                api_key = key
        except Exception:
            pass
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is not set. Add it to your env or .streamlit/secrets.toml")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.0-flash-001")

def _build_weekly_plan_prompt(profile: dict) -> str:
    name = (profile.get("first_name") or "User").strip()
    goal = (profile.get("goal") or "Weight Loss")
    diet = (profile.get("dietary_preferences") or "Vegetarian")

    return f"""You are a concise health assistant. Return your answer in EXACTLY the structure and markdown below (do not add extra sections or headings). Personalize food items to respect allergies/dietary preferences and goal, but keep the same structure and calorie splits.

=== Weekly Diet Plan ===

## {name}'s Weekly {diet} {goal} Diet Plan

*Calorie Target:* Approximately 1800-2000 calories per day (This is an estimate and may need adjustment based on activity level. Consult a doctor or registered dietitian for personalized recommendations.)

*Note:*  Portion sizes should be adjusted based on individual hunger levels and activity.  Focus on whole, unprocessed foods.  Drink plenty of water throughout the day. This plan provides a variety of options, feel free to swap similar options within the same category.

*Day 1:*

•⁠  ⁠*Breakfast (350 calories):* Oatmeal (1/2 cup dry) with berries (1/2 cup) and a sprinkle of nuts (1/4 cup).
•⁠  ⁠*Lunch (400 calories):*  Large salad with mixed greens, chickpeas (1/2 cup), cucumber, tomatoes, and a light vinaigrette dressing. Add a whole-wheat pita bread (1 small).
•⁠  ⁠*Snack (150 calories):* Apple slices with 2 tablespoons of peanut butter.
•⁠  ⁠*Dinner (500 calories):*  Vegetable curry (1.5 cups) with brown rice (1/2 cup).
•⁠  ⁠*Snack (200 calories):*  Greek yogurt (1 cup) with a handful of berries.

*Day 2:*

•⁠  ⁠*Breakfast (300 calories):*  Whole-wheat toast (2 slices) with avocado (1/4 avocado) and a poached egg (optional, adds ~70 calories).
•⁠  ⁠*Lunch (450 calories):* Lentil soup (1.5 cups) with a side salad.
•⁠  ⁠*Snack (100 calories):*  A handful of almonds (about 23).
•⁠  ⁠*Dinner (550 calories):*  Vegetable stir-fry with tofu (1/2 block) and brown rice noodles (1/2 cup).
•⁠  ⁠*Snack (200 calories):*  Cottage cheese (1/2 cup) with chopped vegetables.

*Day 3:*

•⁠  ⁠*Breakfast (350 calories):*  Smoothie with spinach, banana, almond milk, and protein powder (vegetarian).
•⁠  ⁠*Lunch (400 calories):*  Quinoa salad with black beans, corn, bell peppers, and a lime dressing.
•⁠  ⁠*Snack (150 calories):*  Baby carrots and hummus (2 tablespoons).
•⁠  ⁠*Dinner (500 calories):*  Vegetarian chili (1.5 cups) with a side of whole-wheat crackers.
•⁠  ⁠*Snack (200 calories):*  Air-popped popcorn (3 cups).

*Day 4:*

•⁠  ⁠*Breakfast (300 calories):*  Whole-wheat pancakes (2 small) with fruit and a small amount of maple syrup.
•⁠  ⁠*Lunch (450 calories):*  Leftover vegetarian chili.
•⁠  ⁠*Snack (100 calories):*  A small pear.
•⁠  ⁠*Dinner (550 calories):*  Vegetable and paneer (Indian cheese, optional) curry with brown rice.
•⁠  ⁠*Snack (200 calories):*  Greek yogurt with granola (1/4 cup).

*Day 5:*

•⁠  ⁠*Breakfast (350 calories):*  Scrambled tofu with vegetables and whole-wheat toast (1 slice).
•⁠  ⁠*Lunch (400 calories):*  Large salad with roasted sweet potatoes, chickpeas, and feta cheese (optional, adds ~50 calories).
•⁠  ⁠*Snack (150 calories):*  Rice cakes (2) with avocado (1/8 avocado).
•⁠  ⁠*Dinner (500 calories):*  Vegetarian pizza on a whole-wheat crust with lots of vegetables.
•⁠  ⁠*Snack (200 calories):*  A small bowl of berries.

*Day 6:*

•⁠  ⁠*Breakfast (300 calories):*  Breakfast burrito with scrambled tofu, black beans, salsa, and whole-wheat tortilla.
•⁠  ⁠*Lunch (450 calories):*  Leftover vegetarian pizza.
•⁠  ⁠*Snack (100 calories):*  A handful of trail mix (nuts, seeds, dried fruit – watch portion size).
•⁠  ⁠*Dinner (550 calories):):*  Pasta with marinara sauce and lots of vegetables.
•⁠  ⁠*Snack (200 calories):*  Edamame (1 cup).

*Day 7:*

•⁠  ⁠*Breakfast (350 calories):*  Yogurt parfait with granola, berries, and a drizzle of honey.
•⁠  ⁠*Lunch (400 calories):*  Sandwich on whole-wheat bread with hummus, vegetables, and sprouts.
•⁠  ⁠*Snack (150 calories):):*  Banana with almond butter (1 tablespoon).
•⁠  ⁠*Dinner (500 calories):*  Roasted vegetables with chickpeas and a lemon-herb dressing.
•⁠  ⁠*Snack (200 calories):):*  Dark chocolate (small square, 70% cocoa or higher).

This is a sample plan. Adjust portion sizes and food choices based on your preferences and how you feel. Remember to consult with a healthcare professional or registered dietitian before making significant dietary changes, especially if you have any underlying health conditions. Regular exercise will also enhance your weight loss efforts.

Personalize for this user context (do NOT change the structure above, only swap foods/notes if necessary to respect allergies/dietary preferences and goal):
{profile}
"""

def _generate_weekly_plan(profile: dict) -> str:
    model = _get_gemini_model()
    prompt = _build_weekly_plan_prompt(profile)
    resp = model.generate_content(prompt)
    return (getattr(resp, "text", "") or "").strip()

def render_dashboard():
    st.title("Dashboard")

    profile = st.session_state.get("profile")
    if not profile:
        st.info("No profile found. Please fill your details on the Profile page.")
        if st.button("Go to Profile"):
            st.session_state["route"] = "profile"
            st.rerun()
        return

    with st.expander("Profile summary"):
        st.json(profile)

    if st.button("Generate Weekly Plan"):
        with st.spinner("Generating your plan…"):
            try:
                st.session_state.generated_plan = _generate_weekly_plan(profile)
            except Exception as e:
                st.session_state.generated_plan = f"Error generating plan: {e}"

    plan = st.session_state.get("generated_plan")
    if plan:
        st.markdown(plan)
    else:
        st.info("Click **Generate Weekly Plan** to get your personalized output.")
