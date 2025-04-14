import uuid

import csv
import os
from datetime import datetime

from utils.logger import logger

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
CSV_PATH = os.path.join(PROJECT_ROOT, "test_data", "users.csv")

def save_employee_to_csv(username, employee_id, password="Pass123!"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile(CSV_PATH)


    with open(CSV_PATH, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Username", "Employee ID", "Password"])
            logger.info("📄 CSV file created with headers")
        writer.writerow([timestamp, username, employee_id, password])
        logger.info(f"✅ Saved to CSV: {username}, {employee_id}")


def read_last_user_from_csv(file_path=CSV_PATH):
    if not os.path.exists(file_path):
        return []
    with open(file_path, mode="r", newline="") as file:
        reader = list(csv.reader(file))
        if len(reader) <= 0:
            return []
        last_row = reader[-1]
        if len(last_row) >= 3:
            username = last_row[1]
            employee_id = last_row[2]
            return [(username, employee_id)]

    return []

def generate_unique_employee_id():
    return  f"ID{uuid.uuid4().hex[:5]}"

def generate_unique_username(prefix="Alexandr"):
    return f"{prefix}{uuid.uuid4().hex[:5]}"