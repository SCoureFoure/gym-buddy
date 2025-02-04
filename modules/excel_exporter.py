import pandas as pd
from datetime import datetime
import os
import re

def parse_plan_text(plan_text):
    print("📊 Debug: Raw Plan Text Received:")
    print("-" * 40)
    print(plan_text)
    print("-" * 40)

    # Extract the table section
    table_pattern = r"(\|.*?\|\n)+"
    table_match = re.search(table_pattern, plan_text, re.DOTALL)

    if not table_match:
        print("❗ Warning: No table-like structure found in the plan text.")
        return []

    table_text = table_match.group(0)
    print("🗂️ Extracted Table Section:")
    print("-" * 40)
    print(table_text)
    print("-" * 40)

    # Row pattern to capture table rows
    row_pattern = r"\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|"
    rows = re.findall(row_pattern, table_text)

    print(f"\n🔍 Rows Found = {len(rows)}")
    parsed_data = []

    for row in rows:
        print(f"📥 Row Data: {row}")  # Debug each row

        # Skip header and separator rows (like '-----')
        if row[0].strip().lower() in ["day", ""] or all(char == '-' for char in row[0].strip()):
            continue

        # Skip empty rows
        if all(not cell.strip() for cell in row):
            continue

        parsed_data.append({
            "Day": row[0].strip(),
            "Exercise": row[1].strip(),
            "Sets": row[2].strip(),
            "Reps": row[3].strip(),
            "Suggested Weight (lbs)": row[4].strip(),
        })

    print(f"✅ Parsed Exercises = {len(parsed_data)}")
    return parsed_data

def export_plan_to_csv(plan_text):
    output_folder = "new_workout"
    os.makedirs(output_folder, exist_ok=True)

    exercises = parse_plan_text(plan_text)

    if not exercises:
        print("❗ Warning: No exercises parsed. Please check the LLM output format.")
        return

    # File name format
    now = datetime.now()
    year = now.strftime('%Y')
    month_abbr = now.strftime('%b')
    week_number = now.isocalendar()[1]

    filename = f"workout_{year}_{month_abbr}_week_{week_number}.csv"
    filepath = os.path.join(output_folder, filename)

    # Export to CSV
    df = pd.DataFrame(exercises)
    df.to_csv(filepath, index=False)

    print(f"\n✅ Plan exported successfully to {filepath}")
