<div align="center">
  <img src="static/img/logo.png" alt="Hospital Management Logo" height="100">
  <h1>Hospital Management System (Django)</h1>
  <p>
    A modern, role-based healthcare platform built with Django, connecting doctors, patients, and administrators through dedicated workflows.
  </p>
  <p>
    <a href="#features"><strong>Features</strong></a> •
    <a href="#tech-stack"><strong>Tech Stack</strong></a> •
    <a href="#project-structure"><strong>Project Structure</strong></a> •
    <a href="#getting-started"><strong>Getting Started</strong></a> •
    <a href="#urls"><strong>URLs</strong></a> •
    <a href="#contributing"><strong>Contributing</strong></a>
  </p>
</div>

---

## ✨ Features

### 🧑‍⚕️ Patients
- **Profile Management** – Register, log in, and manage personal profiles and avatars.
- **Appointment Booking** – Book appointments with doctors, track status (pending/accepted/declined), and view history.
- **Content Engagement** – Read and comment on blogs published by doctors.

### 🩺 Doctors
- **Blog Management** – Write, edit, and publish blogs with a draft/publish workflow.
- **Appointment Management** – Review, accept, or decline appointment requests.
- **Professional Profile** – Maintain a public profile with specialty, bio, and relevant info.

### ⚙️ Administrators (Custom Portal)
- **Role-Based Access Control** – Custom `AdminUser` model with granular roles (Super, System, Hospital, Department).
- **Operational Dashboard** – Custom portal (separate from `/admin`) with analytics on users, appointments, and activity.
- **User Management** – Manage all user accounts and system settings.

---

## 🛠 Tech Stack
- **Backend:** Python 3.x, Django
- **Frontend:** HTML5, CSS3, Bootstrap 5, jQuery
- **Database:** SQLite (dev) — easily swappable for PostgreSQL or MySQL
- **Security:** Django auth, CSRF protection, hashed passwords, tokenized password reset via email
- **Assets & Media:** Django static files pipeline + media handling (avatars, blog thumbnails)

---

## 🗂 Project Structure

hospital-management-system/
├── hospital/         # Project settings and root URL routing
├── users/            # Custom User models (User, AdminUser) and auth views
├── doctors/          # Doctor-specific models, views, and URLs
├── patients/         # Patient-specific models, views, and URLs
├── admin_portal/     # Custom operational admin app (dashboard, etc.)
├── templates/        # Django templates organized by app
├── static/           # Static assets (CSS, JS, images)
├── assets/           # Collected static files for production
├── media/            # User-uploaded media (avatars, thumbnails)
└── seed/             # Data fixtures for initial setup (categories, specialties)

---

## 🚀 Getting Started

### Prerequisites
- Python **3.8+**
- Git

### Setup Instructions

**1️⃣ Clone the Repository**
```bash
git clone https://github.com/codersupra/Hospital-Management-System.git
cd Hospital-Management-System

# Create the environment
# Create venv
python -m venv .venv

# Activate environment
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
# macOS/Linux (bash)
source .venv/bin/activate

Install Dependencies

```bash
pip install -r requirements.txt

Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate

Load Initial Data (Optional)
This will populate the database with predefined categories, specialties, etc.

```bash

python manage.py loaddata seed/categories.json
python manage.py loaddata seed/specialities.json
python manage.py loaddata seed/status.json
python manage.py loaddata seed/time.json
Create a Superuser
This account is for accessing the built-in Django admin interface at /admin/.

```bash

python manage.py createsuperuser
Run the Development Server

```bash

python manage.py runserver
The application will be available at http://localhost:8000.

Configuration
To enable the password reset feature via email, configure your SMTP settings in hospital/settings.py:

Python

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'          # Your email address
EMAIL_HOST_PASSWORD = 'your-app-password'         # Your email app password
URLs
The project defines distinct URL paths for different user roles to avoid conflicts.

User-facing (Doctors/Patients)

/login/ — Main login page.

/register/ — User registration page.

/password-reset/ — Password reset request flow.

/logout/ — Logout.

Operational Admin (Custom Portal)

/admin-login/ — Login for AdminUser roles.

/admin-register/ — Registration for AdminUser roles.

/admin-dashboard/ — Main dashboard for operational management.

Django Admin (Built-in)

/admin/ — The default Django admin site (requires superuser login).

Contributing
Contributions are welcome! If you find a bug or have a feature request, please open an issue or submit a pull request.

License
This project is intended for educational and personal use.

<br>
<div align="center">
Made with ❤️
</div>
