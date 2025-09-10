import json

def calculate_bmi(weight, height):
    """Calculate BMI given weight (kg) and height (cm)."""
    height_m = height / 100
    return round(weight / (height_m ** 2), 2)

def collect_user_profile():
    print("\n=== Personalized Nutrition Profile Setup ===\n")

    # Basic details
    name = input("Enter your name: ").strip()
    age = int(input("Enter your age (in years): "))
    gender = input("Enter your gender (Male / Female / Other): ").strip().lower()

    # Physical measurements
    height = float(input("Enter your height (in cm): "))
    weight = float(input("Enter your weight (in kg): "))
    bmi = calculate_bmi(weight, height)

    # Optional health metrics
    blood_sugar = input("Enter your fasting blood sugar level (mg/dL) [optional]: ").strip()
    blood_pressure = input("Enter your blood pressure (e.g. 120/80) [optional]: ").strip()

    # Dietary preferences
    print("\nChoose your dietary preference:")
    print("1. Vegetarian")
    print("2. Vegan")
    print("3. Keto")
    print("4. Paleo")
    print("5. High-protein")
    print("6. No preference")
    diet_choice = input("Enter your choice (1-6): ")

    diet_map = {
        "1": "Vegetarian",
        "2": "Vegan",
        "3": "Keto",
        "4": "Paleo",
        "5": "High-protein",
        "6": "No preference"
    }
    dietary_preference = diet_map.get(diet_choice, "No preference")

    # Allergies input
    allergies = input("\nEnter any food allergies (comma-separated, leave blank if none): ")
    allergies_list = [a.strip() for a in allergies.split(",")] if allergies else []

    # Health & fitness goals
    print("\nChoose your goal:")
    print("1. Weight Loss")
    print("2. Weight Gain")
    print("3. Muscle Gain")
    print("4. Maintain Current Weight")
    print("5. Improve Overall Health")
    goal_choice = input("Enter your choice (1-5): ")

    goal_map = {
        "1": "Weight Loss",
        "2": "Weight Gain",
        "3": "Muscle Gain",
        "4": "Maintain Current Weight",
        "5": "Improve Overall Health"
    }
    dietary_goal = goal_map.get(goal_choice, "Improve Overall Health")

    # Calorie target (optional input)
    calorie_target = input("\nEnter your daily calorie goal (leave blank to auto-calculate): ")
    calorie_target = int(calorie_target) if calorie_target else None

    # Final structured profile
    user_profile = {
        "name": name,
        "age": age,
        "gender": gender,
        "height_cm": height,
        "weight_kg": weight,
        "bmi": bmi,
        "blood_sugar_mg_dl": blood_sugar if blood_sugar else None,
        "blood_pressure": blood_pressure if blood_pressure else None,
        "dietary_preference": dietary_preference,
        "allergies": allergies_list,
        "dietary_goal": dietary_goal,
        "calorie_target": calorie_target
    }

    # Save to JSON
    with open(name+"_profile.json", "w") as f:
        json.dump(user_profile, f, indent=4)

    print("\n✅ Profile successfully created and saved as '<user_name>_profile.json'")
    return user_profile

if __name__ == "__main__":
    profile = collect_user_profile()
    print("\n=== Your Profile ===")
    print(json.dumps(profile, indent=4))