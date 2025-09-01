# Barter or Buy

Barter or Buy is a Django-based application that helps users check market prices for crops and compare prices for bartering purposes. Built as a final project at the culmination of the FNB App Academy 2025, to demonstrate full-stack development skills, it includes dynamic forms, clean separation of logic, and reusable templates.

---

## ?? Features

- Check current market price of a crop
- Compare two crops for fair bartering
- Clean, responsive HTML templates
- Form validation using Django Forms
- Environment variables for secure settings

---

## ?? Tech Stack

- Python 3
- Django 4.2
- HTML5 / CSS3
- SQLite3 (default)

---

## ?? Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/barter.git
cd barter

python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

pip install -r requirements.txt

cp .env.example .env

python manage.py runserver

```

Then visit http://127.0.0.1:8000/ in your browser.

## ?? Project Structure

barterapp/
¦
+-- main/                # Core app
¦   +-- views.py         # Handles crop pricing and comparison logic
¦   +-- forms.py         # Django Forms for input validation
¦   +-- urls.py
¦   +-- templates/main/
¦   +-- static/main/
¦   +-- tests.py         # Unit tests
¦
+-- barterapp/           # Project settings
¦   +-- settings.py
¦
+-- .env.example         # Sample secrets file
+-- requirements.txt
+-- manage.py

## ?? About Me

This project was built by Deserai, an aspiring full-stack developer.
Feel free to connect with me on LinkedIn or check out more projects!


