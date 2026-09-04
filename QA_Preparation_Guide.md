# 🎓 Blood Bank Project — Viva / QA Preparation Guide

*A mock question-and-answer sheet for your project review. Read the answers, then say them in **your own words** — don't memorise word-for-word. If you understand the idea, you can answer any way the question is asked.*

**Your project in one line:** A *Blood Bank Management System* — a website (built with **Python + Flask + Firebase**) where **donors** donate blood, **patients** request blood, and an **admin** manages stock and approves requests.

---

## PART 1 — Project Overview

**Q1. Tell me about your project.**
> "My project is a Blood Bank Management System. It's a website that connects blood donors, patients who need blood, and an admin who manages everything. Donors can donate blood, patients can search for and request blood, and the admin manages the blood stock and accepts or rejects requests."

💡 *Tip: Keep the first answer short and confident. They'll ask follow-ups.*

**Q2. What are the modules / types of users?**
> "There are three modules:
> - **Admin** – manages blood stock, views all users, and accepts or rejects blood requests.
> - **Donor** – views the blood stock, donates blood, and responds to emergency needs.
> - **Patient** – searches for blood, requests it, and tracks the status of their request."

**Q3. What problem does your project solve?**
> "It replaces paper records with a digital system. It keeps track of available blood, who needs it, and who donated — and helps connect donors to patients quickly, especially in emergencies."

**Q4. Why did you choose this project?**
> "Because a blood bank solves a real-life problem that can save lives, and it let me practise building a complete system with login, a database, and different user roles."

---

## PART 2 — Programming Languages & Tools

**Q5. What programming languages did you use?**
> "**Python** for the backend (the logic), and **HTML + CSS** for the frontend (what the user sees). I also used a little **Jinja2**, which lets me put Python data into my HTML pages."

**Q6. What framework did you use, and why?**
> "I used **Flask**, a Python web framework. I chose it because it's lightweight and beginner-friendly — it lets me build a website with less code and is easy to understand."

💡 *A "framework" = a ready-made toolbox that handles the common parts of building a website, so you focus on your features.*

**Q7. What tools and libraries did you use?**
> "- **Flask** – the web framework
> - **firebase-admin** – connects my Python code to the Firebase database
> - **Werkzeug** – for securely storing passwords (it comes with Flask)
> - **Bootstrap** – for the design and styling"

**Q8. What software did you use to write the code?**
> "I used **Visual Studio Code** (VS Code) as my code editor, and I ran the project using Python in a virtual environment."

---

## PART 3 — Frontend

**Q9. What did you use for the frontend / design?**
> "**HTML** for the structure of the pages and **Bootstrap** for the styling. Bootstrap gives ready-made, good-looking buttons, forms, tables, and layouts, and it also makes the site work on mobile."

**Q10. What is Bootstrap?**
> "Bootstrap is a free **CSS framework** — a collection of pre-made design pieces like buttons, cards, and navigation bars. I added it using a **CDN link**, which means I linked to it online instead of downloading it."

**Q11. How do you show data (like a user's name) on a web page?**
> "I use **Jinja2**, Flask's templating engine. In the HTML I write a placeholder like `{{ user.name }}`, and Flask fills in the real value from the database when the page loads."

**Q12. What is `base.html` / template inheritance?**
> "I made one base template with the common parts — the navigation bar and footer. All other pages **extend** it, so I don't repeat the same code on every page; I only write the unique part of each page."

**Q13. Is your website responsive (does it work on phones)?**
> "Yes. Because I used Bootstrap, the layout automatically adjusts to phones, tablets, and computers."

---

## PART 4 — Backend

**Q14. Explain the backend of your project.**
> "The backend is written in **Python using Flask** — it's the brain of the website. When a user does something, like logging in, the browser sends a request to my Flask app. The app runs the right function, talks to the database if needed, and sends back a web page."

**Q15. What is a route?**
> "A **route** is a URL path connected to a Python function. For example, `/login` is a route — when someone visits it, Flask runs my login function. I create routes using `@app.route()`."

**Q16. What is the difference between GET and POST?**
> "**GET** is for viewing a page — like opening the login page. **POST** is for sending data to the server — like submitting the login form. My forms use POST, and I check `request.method` in my code to know which one it is."

**Q17. How does the login system work?**
> "When a user enters their email and password, my app looks up that email in the database. If it exists, it checks whether the password matches the stored (encrypted) one. If correct, I save their details in a **session** so they stay logged in, and send them to their dashboard based on their role."

**Q18. What is a session?**
> "A session is how the website **remembers who is logged in** as you move between pages. After you log in, Flask stores your details in a session so you don't have to log in again on every page. Logging out clears the session."

**Q19. How do you handle the different roles (admin/donor/patient)?**
> "When a user registers I save their **role**. When they log in I store the role in the session. Before showing a protected page I check the role — for example, only an 'admin' can open the admin pages. I made a helper function called `require_role` for this."

**Q20. How does data flow from a form to the database?**
> "The user fills a form and submits it (POST). Flask receives the data through `request.form`, my Python code processes it, and then I save it to Firebase using the firebase-admin library. To show it back, I read it from Firebase and pass it to the HTML template."

---

## PART 5 — Database

**Q21. What database did you use?**
> "I used **Firebase Firestore**, a cloud database from Google. It's a **NoSQL** database — it stores data as *documents* (like folders with fields) instead of tables with rows and columns."

**Q22. What is Firebase / Firestore?**
> "Firebase is a platform by Google for building apps, and Firestore is its database. It stores data **in the cloud**, so I don't have to install a database on my computer. My Python code connects to it using the **firebase-admin** library."

**Q23. What is the difference between SQL and NoSQL? Why did you use NoSQL?**
> "**SQL** databases (like MySQL) store data in **tables** with fixed rows and columns. **NoSQL** databases like Firestore store data as flexible **documents**. I chose Firestore because it's easy to set up, stores data online, and works well for a project like this without designing complex tables."

**Q24. How is your data organised? (Data model)**
> "Firestore uses **collections** (categories) and **documents** (individual records). I have four collections:
> - **users** – all donors, patients, and admins with their details
> - **blood_inventory** – how many units of each blood group are available
> - **requests** – blood requests made by patients
> - **donations** – records of blood donated by donors"

**Q25. How do you save and read data from the database?**
> "I use the firebase-admin library. To save, I use something like `db.collection('users').document(email).set({...})`. To read, I use `.get()` for one record or `.stream()` to loop through all records."

**Q26. What is CRUD? Did you use it?**
> "CRUD means **Create, Read, Update, Delete** — the four basic database actions. I use:
> - **Create** – registering a user or making a request
> - **Read** – showing the blood stock or the user list
> - **Update** – the admin accepting a request changes its status and reduces stock
> - **Delete** – not used much in the app yet, but it's something I can add, like letting the admin remove a user."

💡 *Be honest about Delete — saying "I could add it" shows you understand the concept.*

---

## PART 6 — Security

**Q27. How do you store passwords? Are they safe?**
> "I **never store passwords as plain text**. I use `generate_password_hash`, which converts the password into a scrambled code called a **hash**. When someone logs in, I compare the hashes, not the real password. So even if someone saw the database, they couldn't read the passwords."

**Q28. What is password hashing?**
> "Hashing turns a password into a fixed, scrambled string that **can't be reversed** back into the original. When you log in, the system hashes what you typed and checks if it matches the stored hash."

**Q29. How do you protect the admin pages?**
> "Every admin page checks the logged-in user's role first. If someone who isn't an admin tries to open it, they're redirected to the login page with a warning."

**Q30. What is the serviceAccountKey file?**
> "It's a **secret key file** that lets my Python app securely connect to Firebase — like a password for my app. I keep it private and never share or upload it online."

---

## PART 7 — "How does it work?" (Flow questions)

**Q31. Walk me through what happens when a patient requests blood.**
> "The patient fills a form choosing the blood group and number of units. When they submit, my app adds their name and contact details, and saves it as a new document in the **requests** collection with status **'pending'**. It then shows up in the patient's 'My Requests' page, the admin's requests page, and the donor's emergency list."

**Q32. What happens when the admin accepts a request?**
> "The app checks if there's enough blood of that group in stock. If yes, it **reduces the stock** by the requested units and changes the request's status to **'accepted'**. If there isn't enough, it shows an error. The patient then sees their request marked as accepted."

**Q33. What happens when a donor donates blood?**
> "The donor chooses a blood group and units. The app **adds those units to the stock** for that group, and saves a record in the **donations** collection with the donor's name and the date."

**Q34. How does the emergency list work?**
> "The emergency list shows all the patient requests that are still 'pending'. A donor can see what's urgently needed and donate that blood group, which tops up the stock so the admin can then approve the request."

---

## PART 8 — Reflective Questions

**Q35. What challenges did you face?**
> "Since I'm new to coding, understanding how the frontend, backend, and database connect was hard at first. Setting up Firebase and handling login and user roles also took time. Breaking the project into small steps helped me a lot."

**Q36. What are the limitations of your project?**
> "It's a basic system. It doesn't send email or SMS notifications, admin accounts are created manually, and there's no advanced search or reports yet."

**Q37. What future improvements would you make?**
> "I'd add email/SMS notifications, a donation-history page, search and filters, charts and reports for the admin, and I'd host it online."

**Q38. Is your project hosted online?**
> "Right now it runs locally on my computer using Flask's development server. It can be deployed online later using services like **PythonAnywhere, Render, or Heroku**."

---

## PART 9 — Rapid-fire one-liners (short, confident answers)

- **Language for backend?** → Python
- **Framework?** → Flask
- **Database?** → Firebase Firestore (NoSQL, cloud)
- **Frontend?** → HTML + Bootstrap (CSS)
- **How data is put into pages?** → Jinja2 templates (`{{ }}`)
- **How users stay logged in?** → Sessions
- **How passwords are kept safe?** → Hashing (Werkzeug)
- **How Python talks to the database?** → firebase-admin library
- **How you run it?** → `python app.py`, then open `localhost:5000` in the browser
- **What is a virtual environment (venv)?** → A separate space for this project's Python libraries so they don't mix with other projects
- **What is localhost / port 5000?** → The site running on my own computer; port 5000 is the "door" Flask uses in development

---

## PART 10 — Tips for the QA session

1. **Answer in your own words.** Understanding beats memorising — you'll handle any wording.
2. **Keep the first answer short**, then let them ask follow-ups.
3. **If you don't know something, be honest:** "I'm not sure, but I think it works like… / I'd find out by…" — that's far better than guessing wildly.
4. **Have the project running** and be ready to demo the login and one full flow (patient requests → admin accepts).
5. **Know your data flow cold:** Browser → Flask (Python) → Firebase database → back to an HTML page. If you can explain this, you can explain the whole project.
6. **Use the demo accounts** to show all three roles:
   - Admin: `admin@bloodbank.com` / `admin123`
   - Patient: `patient@bloodbank.com` / `patient123`
   - Donor: `donor@bloodbank.com` / `donor123`

---

## 📌 Tech Stack Cheat Sheet (memorise this table)

| Part | What I used |
|------|-------------|
| Backend language | Python |
| Web framework | Flask |
| Frontend | HTML, Bootstrap (CSS) |
| Templating | Jinja2 |
| Database | Firebase Firestore (NoSQL, cloud) |
| DB connection | firebase-admin library |
| Login/security | Flask sessions + password hashing (Werkzeug) |
| Editor | VS Code |

**You've got this. 💪 Read it a few times, do one practice run-through out loud, and you'll be ready.**
