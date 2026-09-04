# firebase_config.py
# Connects your Python code to your Firebase (Firestore) database.

import os
import firebase_admin
from firebase_admin import credentials, firestore

# Find the secret key file sitting next to this file
# (so it works no matter which folder you run the app from).
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(BASE_DIR, "serviceAccountKey.json")

# Connect to Firebase using that key — but only connect once.
if not firebase_admin._apps:
    cred = credentials.Certificate(KEY_PATH)
    firebase_admin.initialize_app(cred)

# "db" is your live database. Other files import this to read & write data.
db = firestore.client()
