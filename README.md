# 🩸 Blood Bank Management System

A web-based Blood Bank Management System built with **Python (Flask)** and **Firebase Firestore**.

The system connects three types of users — **Donors**, **Patients**, and an **Admin** — to manage blood donations, blood stock, and emergency blood requests in one place.

> 📚 Developed as a college project.

---

## 📖 About the Project

Blood banks often rely on manual registers to track donors, available blood units, and patient requests. This project replaces that with a simple digital system where:

- Donors can see what blood is needed and donate voluntarily
- Patients can search for blood and raise a request
- The Admin can manage stock and approve or reject requests

---

## ✨ Features

### 👤 Donor Module
- Register and log in as a donor
- View current blood stock with **Needed! / Low stock / Good** indicators
- Donate blood (automatically adds units to the inventory)
- View the **Emergency list** of pending patient requests and donate directly for a needed blood group
- View and update their own profile

### 🧑‍⚕️ Patient Module
- Register and log in as a patient
- Search the blood inventory by blood group (**Available / Out of stock**)
- Submit a blood request with the required units
- Track the status of their requests (**Pending / Accepted / Rejected**)
- View and update their own profile

### 🛠️ Admin Module
- Dashboard with an overview of stock, users and pending requests
- Manage the blood inventory (update units for each blood group)
- View all registered donors and patients
- **Accept or reject** blood requests — accepting automatically reduces the stock
- Requests are rejected safely if there is not enough blood available

### 🔐 Common
- Role-based login (donor / patient / admin) with protected pages
- Passwords stored securely using hashing (never as plain text)
- Responsive design that works on mobile and desktop

---

## 🧰 Tech Stack

| Part | Technology |
|------|-----------|
| Backend language | Python |
| Web framework | Flask |
| Database | Firebase Firestore (NoSQL, cloud) |
| Database connection | firebase-admin (Firebase Admin SDK) |
| Frontend | HTML, Bootstrap 5 |
| Templating | Jinja2 |
| Authentication | Flask sessions + Werkzeug password hashing |

---

## 🗂️ Database Structure (Firestore)

The data is stored in the cloud in four collections:

| Collection | Description |
|-----------|-------------|
| `users` | All donors, patients and admins — name, email, hashed password, phone, blood group, city, role |
| `blood_inventory` | Available units for each of the 8 blood groups |
| `requests` | Blood requests raised by patients, with their status |
| `donations` | Record of every donation made by donors |

---

## 📁 Project Structure

```
Project/
├── app.py                  # Main Flask application (all routes)
├── firebase_config.py      # Connects the app to Firebase Firestore
├── seed_admin.py           # Creates the default admin account
├── seed_inventory.py       # Sets up the 8 blood groups in the inventory
├── requirements.txt        # Python libraries used
├── templates/              # All HTML pages (Jinja2 templates)
│   ├── base.html           # Shared layout (navbar + footer)
│   ├── home.html
│   ├── login.html / register.html / profile.html
│   ├── donor_*.html
│   ├── patient_*.html
│   └── admin_*.html
└── serviceAccountKey.json  # Firebase secret key (NOT included in this repo)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3 installed
- A Firebase project with **Firestore** enabled

### 1. Clone the repository
```bash
git clone https://github.com/Anzil75/<your-repo-name>.git
cd <your-repo-name>
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
```
```bash
venv\Scripts\activate
```

### 3. Install the required libraries
```bash
pip install -r requirements.txt
```

### 4. Add your Firebase key
1. In the [Firebase Console](https://console.firebase.google.com/), open your project
2. Go to **Project settings → Service accounts → Generate new private key**
3. Save the downloaded file as **`serviceAccountKey.json`** in the project folder

> ⚠️ This file is a secret credential. It is listed in `.gitignore` and must **never** be uploaded or shared.

### 5. Set up the initial data
```bash
python seed_inventory.py
```
```bash
python seed_admin.py
```

### 6. Run the application
```bash
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

---

## 🔑 Default Admin Login

| Email | Password |
|-------|----------|
| `admin@bloodbank.com` | `admin123` |

> Admin accounts are not created through registration — they are created only by running `seed_admin.py`.

Donors and patients can sign up themselves from the **Register** page.

---

## 🔄 How It Works

**When a patient requests blood:**
1. The patient submits a request → it is saved with the status **pending**
2. It appears on the patient's "My Requests" page, the admin's requests page, and the donors' emergency list
3. A donor can donate that blood group, which adds units to the stock
4. The admin accepts the request → the stock is reduced and the status becomes **accepted**

**Overall data flow:**
> Browser → Flask (Python) → checks the session and role → reads/writes Firebase Firestore → renders an HTML page with Jinja2, styled with Bootstrap → sends the page back to the browser

---

## 🔒 Security

- Passwords are hashed with Werkzeug (`generate_password_hash`) and are never stored in plain text
- Flask sessions keep users logged in across pages
- Every protected page checks the user's role before granting access
- The Firebase service account key is kept private and excluded from version control

---

## 🚧 Future Improvements

- Email / SMS notifications for emergency requests
- Donation history page for the admin
- Search and filter options for users and requests
- Charts and reports on the admin dashboard
- Deploy the app online

---

## 👨‍💻 Author

**Anzil**
College Project — Blood Bank Management System
