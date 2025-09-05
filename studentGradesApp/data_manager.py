import json, os

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"students": [], "courses": []}
    
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    # Normalize students
    for student in data.get("students", []):
        student["id"] = int(student["id"])
        student["courses"] = [int(c) for c in student.get("courses", [])]

    # Normalize courses
    for course in data.get("courses", []):
        course["id"] = int(course["id"])
        course["students"] = [int(sid) for sid in course.get("students", [])]

    return data

def save_data(data):
    print("DEBUG: Saving data:", data) 
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
