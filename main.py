import os
import shutil
from dotenv import load_dotenv
from modules.planner import generate_workout_plan
from modules.excel_exporter import export_plan_to_csv

def move_new_workouts():
    new_workout_folder = "new_workout"
    previous_workout_folder = "previous_workouts"

    os.makedirs(previous_workout_folder, exist_ok=True)

    for filename in os.listdir(new_workout_folder):
        if filename.endswith(".csv"):
            src = os.path.join(new_workout_folder, filename)
            dest = os.path.join(previous_workout_folder, filename)

            if not os.path.exists(dest):
                shutil.move(src, dest)
                print(f"📦 Moved '{filename}' to 'previous_workouts'")
            else:
                print(f"⚠️ Duplicate detected: '{filename}' already exists. Skipping.")

def main():
    print("✅ Program started!")
    load_dotenv(dotenv_path=".env")
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in .env file. Please check your file and try again.")
        exit(1)
    else:
        print(f"🔑 API key loaded successfully. (Key starts with: {api_key[:8]})")

    # ✅ Automatically move workouts on startup
    print("📦 Moving any new workouts to 'previous_workouts' folder...")
    move_new_workouts()

    print("🏋️ Welcome to Gym Buddy!")
    print("🚫 'Chat with Gym Buddy' is currently disabled.")
    print("2️⃣ Generate Weekly Workout Plan")
    choice = input("Select an option (2): ")

    if choice == "2":
        plan = generate_workout_plan(api_key)
        print("💾 Exporting workout plan to CSV...")
        export_plan_to_csv(plan)
        print("✅ Plan successfully exported to the 'new_workout' folder.")
    else:
        print("❌ Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
