# seed_inventory.py
# Run this ONCE to create all 8 blood groups in the inventory (starting at 0 units).
# Run with:  venv\Scripts\python.exe seed_inventory.py

from firebase_config import db

BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

for bg in BLOOD_GROUPS:
    doc = db.collection("blood_inventory").document(bg).get()
    if doc.exists:
        print(bg, "already exists ->", doc.to_dict().get("units", 0), "units")
    else:
        db.collection("blood_inventory").document(bg).set({"units": 0})
        print(bg, "created with 0 units")

print("Inventory ready.")
