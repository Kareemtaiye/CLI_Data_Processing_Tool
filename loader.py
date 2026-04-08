import os
import sys
import csv


def load_csv(filepath):
    """Load csv file and return a list of row dicts"""

    # check if file path exits
    if not os.path.exists(filepath):
        print(f"[ERROR] path doesn't exist: {filepath}")
        sys.exit(1)

    # Ensure its a CSV file
    if (ext := filepath.split(".")[-1]) != "csv":
        print(f"[ERROR] file with {filepath} is not a CSV. Extension read - {ext}")

    # Read the csv file
    with open(filepath, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # Empty file or contains only column names
    if not rows:
        print("[ERROR] CSV file is empty or has no data row")
        sys.exit(1)

    return [data for data in rows]
