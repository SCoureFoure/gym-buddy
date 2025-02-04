from openai import OpenAI
from modules.importer import import_previous_workouts
import os
from dotenv import load_dotenv

def update_env(key, value):
    # Update the .env file with the new key-value pair
    with open(".env", "a") as env_file:
        env_file.write(f"\n{key}={value}")

def get_user_biometrics():
    load_dotenv()  # Ensure environment variables are loaded

    # Check if weight and height are already stored
    weight = os.getenv("USER_WEIGHT")
    height = os.getenv("USER_HEIGHT")
    gender = os.getenv("USER_GENDER")

    if not weight:
        weight = input("Enter your weight (in lbs): ")
        update_env("USER_WEIGHT", weight)

    if not height:
        height = input("Enter your height (in inches): ")
        update_env("USER_HEIGHT", height)

    if not gender:
        height = input("Enter your gender: ")
        update_env("USER_GENDER", gender)

    return weight, height, gender

def generate_workout_plan(api_key):
    client = OpenAI(api_key=api_key)

    # Get user's biometrics from .env or prompt if not available
    weight, height, gender = get_user_biometrics()

    # Prompt the user for available gym equipment
    print("Enter the gym equipment you have access to (comma-separated):")
    equipment = input("Examples: dumbbells, barbell, resistance bands, pull-up bar, kettlebells, etc.\n> ")

    previous_workouts_data = import_previous_workouts()

    # Example row to guide the model's output format
    # TODO: Enhance this to include the targeted muscle groups
    # TODO: Enchance workouts to included stretches for targeted muscle groups
    example_row = (
        "| Day | Exercise           | Sets | Reps | Suggested Weight (lbs) |\n"
        "| Day 1 | Squat            | 4    | 10   | 95                     |\n"
        "| Day 2 | Squat            | 4    | 10   | 95                     |\n"
        "| Day etc | etc            | etc  | etc  | etc                    |\n"
    )

    # Base prompt with biometrics, equipment, and example row
    base_prompt = (
        f"You are a professional gym workout planner. The user weighs {weight} lbs, is {height} inches tall, and is a {gender} "
        f"and has access to the following equipment: {equipment}. "
        "Generate a detailed 4-day workout plan covering multiple muscle groups, and a rest day between the highest intensity workouts."
        "If the plan includes a rest day, add an additional workout so there are always 4 days worth of workouts. 1 rest, would mean 5 days in chart, 2 rests would be six days"
        "The output should be in a table format with the following columns header strictly: Day, Exercise, Sets, Reps, and Suggested Weight (in lbs). "
        "Ensure the plan is balanced, progressive, and suitable for intermediate fitness levels.\n\n"
        "Here is an example of the format to follow:\n"
        f"{example_row}"
    )


    if previous_workouts_data:
        prompt = f"{base_prompt}\n\nHere are the user's recent workouts:\n{previous_workouts_data}\n\nGenerate the new weekly plan below:"
    else:
        prompt = f"{base_prompt}\n\nGenerate the new weekly plan below:"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a gym workout planner."},
            {"role": "user", "content": prompt}
        ]
    )

    plan_text = response.choices[0].message.content
    return plan_text
