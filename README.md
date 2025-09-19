# Healthcare Management System

<div align="center">
  <img src="static/img/logo.png" alt="Healthcare Management Logo" height="100">
  
  <h2>Modern Healthcare Management Portal</h2>
  
  <p>A comprehensive Django-based solution for managing healthcare operations, connecting doctors and patients seamlessly.</p>
  
  <p>
    <a href="#features">Features</a> •
    <a href="#installation">Installation</a> •
    <div align="center">

    # Hospital Management System (Django)

    <img src="static/img/logo.png" alt="Hospital Management Logo" height="100">

    <h3>A modern, role-based healthcare platform built with Django</h3>

    <p>
      Doctors, Patients, and Admins collaborate through dedicated workflows: appointments, blogs, profiles, and an operational admin portal.
    </p>

    <p>
      <a href="#features">Features</a> •
      <a href="#tech-stack">Tech Stack</a> •
      <a href="#getting-started">Getting Started</a> •
      <a href="#urls">URLs</a> •
      <a href="#screenshots">Screenshots</a>
    </p>

    </div>

    ---

    ## Features

    ### Patients
    - Register/login, manage profiles and avatars
    - Book appointments with doctors and track status/history
    - Read and comment on doctors’ blogs

    ### Doctors
    - Write medical blogs with draft/publish workflow
    - Manage appointments (review, accept, decline)
    - Profile with specialty and bio

    ### Admin Portal (separate from Django’s /admin)
    - Distinct AdminUser entity with employee_id, department, hire_date
    - Role-based access (Super/System/Hospital/Department/Staff admin) and access levels
    - Operational dashboard with user/appointment insights

    ---

    ## Tech Stack

    - Backend: Python 3.x, Django
    - Frontend: HTML5, CSS3, Bootstrap 5, jQuery
    - Database: SQLite (dev) — easily swappable for PostgreSQL/MySQL
    - Auth & Security: Django auth, CSRF protection, hashed passwords, tokenized password reset via email
    - Assets & Media: Static files pipeline, media uploads for avatars and blog thumbnails

    ---

    ## Project Structure (high level)

    ```
    hospital/                # Project settings and URL routing
    users/                   # Custom user models (Users, AdminUser) + auth/views
    doctors/                 # Doctor-specific models, views, urls
    patients/                # Patient-specific models, views, urls
    admin/                   # Operational admin app (dashboard view, urls)
    templates/               # Jinja/Django templates (users/, doctors/, patients/)
    static/                  # Static assets (css, js, img)
    assets/                  # Collected static (for production)
    media/                   # Uploaded media (avatars, blog thumbnails)
    seed/                    # Fixtures: categories, specialties, status, time
    ```

    ---

    ## Getting Started

    ### Prerequisites
    - Python 3.8+
    - Git

    ### Setup

    ```bash
    # Clone the repository
    git clone https://github.com/codersupra/Hospital-Management-System.git
    cd Hospital-Management-System

    # Create and activate a virtual environment
    python -m venv .venv
    # Windows PowerShell
    .\.venv\Scripts\Activate.ps1
    # macOS/Linux
    source .venv/bin/activate

    # Or use conda
    conda create --name myenv
    conda activate myenv

    # Install dependencies
    pip install -r requirements.txt

    # Apply migrations
    python manage.py makemigrations
    python manage.py migrate

    # (Optional) Load seed data
    python manage.py loaddata seed/categories.json
    python manage.py loaddata seed/specialities.json
    python manage.py loaddata seed/status.json
    python manage.py loaddata seed/time.json

    # Create a superuser for Django admin (/admin)
    python manage.py createsuperuser

    # Run the development server
    python manage.py runserver
    ```

    Visit http://localhost:8000

    ---

    ## Configuration

    Email (for password reset) — configure these in `hospital/settings.py`:

    ```
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'your email'
    EMAIL_HOST_PASSWORD = 'your email host password'
    ```

    Static/Media paths are already configured in settings; ensure `media/` and `static/` exist.

    ---

    ## URLs

    ### User-facing
    - `/login/` — User login (Patients/Doctors)
    - `/register/` — User registration (Patients/Doctors)
    - `/password-reset/`, `/reset/<token>/` — Password reset flow
    - `/logout/` — Logout

    ### Operational Admin (custom portal)
    - `/admin-login/` — Admin login (AdminUser)
    - `/admin-register/` — Admin registration (AdminUser)
    - `/admin-dashboard/` — Admin dashboard (app-level)

    ### Django Admin (built-in)
    - `/admin/` — Django’s default admin site (requires superuser)

    Note: Custom admin URLs avoid conflicts with Django Admin by not using the `/admin/...` prefix.

    ---

    ## Contributing

    Contributions are welcome! Please open an issue or submit a pull request.

    ---

    ## License

    This project is for personal use.

    ---

    <div align="center">
    Made with ❤️
    </div>
