# app.py — the main program that runs the Blood Bank website.

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from firebase_config import db   # our database connection

app = Flask(__name__)

# A "secret key" lets Flask keep users securely logged in (called a session).
app.secret_key = "blood-bank-secret-key-change-me"

# The 8 blood groups, used to fill dropdowns and the stock table.
BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]


def now_iso():
    """Current date & time as text."""
    return datetime.now(timezone.utc).isoformat()


def require_role(role):
    """If the visitor is NOT logged in with this role, return a redirect to send them away.
    If they ARE allowed, return None. Used at the top of protected pages."""
    if session.get("role") != role:
        flash("Please log in as " + role + " to view that page.", "warning")
        return redirect(url_for("login"))
    return None


def require_login():
    """Allow ANY logged-in user (any role). Returns a redirect if nobody is logged in."""
    if not session.get("email"):
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))
    return None


# ================= PUBLIC PAGES =================
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        name = request.form["name"].strip()
        password = request.form["password"]
        phone = request.form["phone"].strip()
        blood_group = request.form["blood_group"]
        city = request.form["city"].strip()
        role = request.form["role"]          # "donor" or "patient"

        if db.collection("users").document(email).get().exists:
            flash("An account with this email already exists. Please log in.", "warning")
            return redirect(url_for("login"))

        db.collection("users").document(email).set({
            "name": name,
            "email": email,
            "password": generate_password_hash(password),
            "phone": phone,
            "blood_group": blood_group,
            "city": city,
            "role": role,
            "created_at": now_iso(),
        })
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", blood_groups=BLOOD_GROUPS)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user_doc = db.collection("users").document(email).get()
        if not user_doc.exists:
            flash("No account found with that email.", "danger")
            return redirect(url_for("login"))

        user = user_doc.to_dict()
        if not check_password_hash(user["password"], password):
            flash("Incorrect password. Please try again.", "danger")
            return redirect(url_for("login"))

        session["email"] = email
        session["name"] = user["name"]
        session["role"] = user["role"]
        flash("Welcome back, " + user["name"] + "!", "success")
        return redirect(url_for(user["role"] + "_dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


@app.route("/profile", methods=["GET", "POST"])
def profile():
    guard = require_login()
    if guard:
        return guard
    user_ref = db.collection("users").document(session["email"])

    # Saving changes to the profile.
    if request.method == "POST":
        new_name = request.form["name"].strip()
        user_ref.update({
            "name": new_name,
            "phone": request.form["phone"].strip(),
            "blood_group": request.form["blood_group"],
            "city": request.form["city"].strip(),
        })
        session["name"] = new_name   # keep the greeting in the top bar up to date
        flash("Your profile has been updated.", "success")
        return redirect(url_for("profile"))

    # Showing the current details.
    user = user_ref.get().to_dict()
    return render_template("profile.html", user=user, blood_groups=BLOOD_GROUPS)


# ================= DONOR MODULE =================
@app.route("/donor/dashboard")
def donor_dashboard():
    guard = require_role("donor")
    if guard:
        return guard
    inventory = get_inventory_dict()
    total_units = sum(inventory.values())
    emergency_count = sum(1 for r in db.collection("requests").stream()
                          if r.to_dict().get("status") == "pending")
    return render_template("donor_dashboard.html",
                           total_units=total_units, emergency_count=emergency_count)


@app.route("/donor/inventory")
def donor_inventory():
    guard = require_role("donor")
    if guard:
        return guard
    inventory = get_inventory_dict()
    return render_template("donor_inventory.html", blood_groups=BLOOD_GROUPS, inventory=inventory)


@app.route("/donor/donate", methods=["GET", "POST"])
def donor_donate():
    guard = require_role("donor")
    if guard:
        return guard

    if request.method == "POST":
        blood_group = request.form["blood_group"]
        try:
            units = int(request.form["units"])
        except (ValueError, KeyError):
            flash("Please enter a valid number of units.", "danger")
            return redirect(url_for("donor_donate"))
        if units < 1:
            flash("Units must be at least 1.", "danger")
            return redirect(url_for("donor_donate"))

        # Add the donated units to that blood group's stock.
        inv_ref = db.collection("blood_inventory").document(blood_group)
        inv_doc = inv_ref.get()
        current = inv_doc.to_dict().get("units", 0) if inv_doc.exists else 0
        inv_ref.set({"units": current + units})

        # Keep a record of who donated, and when.
        me = db.collection("users").document(session["email"]).get().to_dict()
        db.collection("donations").add({
            "donor_email": session["email"],
            "donor_name": me.get("name", session.get("name")),
            "blood_group": blood_group,
            "units": units,
            "created_at": now_iso(),
        })
        flash("Thank you for donating " + str(units) + " unit(s) of " + blood_group + "! 🩸", "success")
        return redirect(url_for("donor_dashboard"))

    # GET: show the form. A blood group may be pre-selected from the emergency list.
    preselect = request.args.get("bg", "")
    return render_template("donor_donate.html", blood_groups=BLOOD_GROUPS, preselect=preselect)


@app.route("/donor/emergency")
def donor_emergency():
    guard = require_role("donor")
    if guard:
        return guard
    emergency = []
    for r in db.collection("requests").stream():
        d = r.to_dict()
        if d.get("status") == "pending":
            emergency.append(d)
    emergency.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return render_template("donor_emergency.html", requests=emergency)


def get_inventory_dict():
    """Return {blood_group: units} for all 8 groups (missing groups count as 0)."""
    stored = {d.id: d.to_dict().get("units", 0) for d in db.collection("blood_inventory").stream()}
    return {bg: stored.get(bg, 0) for bg in BLOOD_GROUPS}


@app.route("/patient/dashboard")
def patient_dashboard():
    guard = require_role("patient")
    if guard:
        return guard
    inventory = get_inventory_dict()
    total_units = sum(inventory.values())
    my_pending = sum(1 for r in db.collection("requests").stream()
                     if r.to_dict().get("patient_email") == session.get("email")
                     and r.to_dict().get("status") == "pending")
    return render_template("patient_dashboard.html", total_units=total_units, my_pending=my_pending)


@app.route("/patient/search")
def patient_search():
    guard = require_role("patient")
    if guard:
        return guard
    inventory = get_inventory_dict()
    return render_template("patient_search.html", blood_groups=BLOOD_GROUPS, inventory=inventory)


@app.route("/patient/request", methods=["GET", "POST"])
def patient_request():
    guard = require_role("patient")
    if guard:
        return guard

    if request.method == "POST":
        blood_group = request.form["blood_group"]
        try:
            units = int(request.form["units"])
        except (ValueError, KeyError):
            flash("Please enter a valid number of units.", "danger")
            return redirect(url_for("patient_request"))
        if units < 1:
            flash("Units must be at least 1.", "danger")
            return redirect(url_for("patient_request"))

        # Pull the patient's own name/phone/city from their profile to attach to the request.
        me = db.collection("users").document(session["email"]).get().to_dict()
        db.collection("requests").add({
            "patient_email": session["email"],
            "patient_name": me.get("name", session.get("name")),
            "phone": me.get("phone", ""),
            "city": me.get("city", ""),
            "blood_group": blood_group,
            "units": units,
            "status": "pending",
            "created_at": now_iso(),
        })
        flash("Your blood request has been submitted! Track it under 'My Requests'.", "success")
        return redirect(url_for("patient_my_requests"))

    return render_template("patient_request.html", blood_groups=BLOOD_GROUPS)


@app.route("/patient/my-requests")
def patient_my_requests():
    guard = require_role("patient")
    if guard:
        return guard
    my_requests = []
    for r in db.collection("requests").stream():
        d = r.to_dict()
        if d.get("patient_email") == session.get("email"):
            my_requests.append(d)
    my_requests.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return render_template("patient_my_requests.html", requests=my_requests)


# ================= ADMIN MODULE =================
@app.route("/admin/dashboard")
def admin_dashboard():
    guard = require_role("admin")
    if guard:
        return guard

    # Gather some quick stats to show on the dashboard.
    users = [u.to_dict() for u in db.collection("users").stream()]
    total_donors = sum(1 for u in users if u.get("role") == "donor")
    total_patients = sum(1 for u in users if u.get("role") == "patient")

    inventory = {d.id: d.to_dict().get("units", 0) for d in db.collection("blood_inventory").stream()}
    total_units = sum(inventory.values())

    pending = sum(1 for r in db.collection("requests").stream()
                  if r.to_dict().get("status") == "pending")

    return render_template("admin_dashboard.html",
                           total_donors=total_donors,
                           total_patients=total_patients,
                           total_units=total_units,
                           pending=pending)


@app.route("/admin/inventory", methods=["GET", "POST"])
def admin_inventory():
    guard = require_role("admin")
    if guard:
        return guard

    # The admin submitted the "Set" form to change a blood group's stock.
    if request.method == "POST":
        bg = request.form["blood_group"]
        try:
            units = int(request.form["units"])
        except (ValueError, KeyError):
            flash("Please enter a valid number of units.", "danger")
            return redirect(url_for("admin_inventory"))
        db.collection("blood_inventory").document(bg).set({"units": units})
        flash("Updated " + bg + " stock to " + str(units) + " units.", "success")
        return redirect(url_for("admin_inventory"))

    # Show the current stock. Any blood group not yet in the database shows as 0.
    stored = {d.id: d.to_dict().get("units", 0) for d in db.collection("blood_inventory").stream()}
    inventory = {bg: stored.get(bg, 0) for bg in BLOOD_GROUPS}
    return render_template("admin_inventory.html", blood_groups=BLOOD_GROUPS, inventory=inventory)


@app.route("/admin/users")
def admin_users():
    guard = require_role("admin")
    if guard:
        return guard
    users = [u.to_dict() for u in db.collection("users").stream()
             if u.to_dict().get("role") != "admin"]
    users.sort(key=lambda u: u.get("role", ""))
    return render_template("admin_users.html", users=users)


@app.route("/admin/requests")
def admin_requests():
    guard = require_role("admin")
    if guard:
        return guard
    requests_list = []
    for r in db.collection("requests").stream():
        d = r.to_dict()
        d["id"] = r.id          # remember the document id so we can accept/reject it
        requests_list.append(d)
    requests_list.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return render_template("admin_requests.html", requests=requests_list)


@app.route("/admin/requests/<req_id>/<action>", methods=["POST"])
def admin_handle_request(req_id, action):
    guard = require_role("admin")
    if guard:
        return guard

    req_ref = db.collection("requests").document(req_id)
    req_doc = req_ref.get()
    if not req_doc.exists:
        flash("Request not found.", "danger")
        return redirect(url_for("admin_requests"))
    req = req_doc.to_dict()

    if action == "accept":
        bg = req["blood_group"]
        units = int(req["units"])
        inv_doc = db.collection("blood_inventory").document(bg).get()
        current = inv_doc.to_dict().get("units", 0) if inv_doc.exists else 0
        if current >= units:
            db.collection("blood_inventory").document(bg).set({"units": current - units})
            req_ref.update({"status": "accepted"})
            flash("Request accepted. " + str(units) + " units of " + bg + " deducted from stock.", "success")
        else:
            flash("Not enough " + bg + " in stock (" + str(current) + " available, "
                  + str(units) + " requested).", "danger")
    elif action == "reject":
        req_ref.update({"status": "rejected"})
        flash("Request rejected.", "info")
    else:
        flash("Unknown action.", "danger")

    return redirect(url_for("admin_requests"))


# ================= START THE WEBSITE =================
if __name__ == "__main__":
    app.run(debug=True)
