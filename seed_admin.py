# seed_admin.py
# Run this ONCE to create the admin account (admins are not created from the website).
# Run it with:  venv\Scripts\python.exe seed_admin.py

from werkzeug.security import generate_password_hash
from datetime import datetime, timezone
from firebase_config import db

ADMIN_EMAIL = "admin@bloodbank.com"
ADMIN_PASSWORD = "admin123"      # change this if you like

existing = db.collection("users").document(ADMIN_EMAIL).get()
if existing.exists:
    print("Admin already exists:", ADMIN_EMAIL)
else:
    db.collection("users").document(ADMIN_EMAIL).set({
        "name": "Administrator",
        "email": ADMIN_EMAIL,
        "password": generate_password_hash(ADMIN_PASSWORD),
        "phone": "-",
        "blood_group": "-",
        "city": "-",
        "role": "admin",
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    print("Admin account created!")
    print("  Email:   ", ADMIN_EMAIL)
    print("  Password:", ADMIN_PASSWORD)
