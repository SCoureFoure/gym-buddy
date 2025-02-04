import pandas as pd
import os

def import_previous_workouts(folder='previous_workouts', num_files=3):
    if not os.path.exists(folder):
        return ""

    workout_files = sorted(
        [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.xlsx')],
        reverse=True
    )[:num_files]

    all_workouts = []
    for file in workout_files:
        df = pd.read_excel(file)
        all_workouts.append(df.to_string(index=False))

    return "\n\n".join(all_workouts)
