# Task Management Project

A Django-based task management system with three roles: **SuperAdmin**, **Admin**, and **User**.  
Each role has specific permissions for managing users, admins, and tasks.

---

## Features

### SuperAdmin
- Manage admins (create, edit, delete, assign roles, promote/demote)
- Manage users (create, edit, delete, assign to admins)
- Assign users to admins
- Manage all tasks across users
- View all task reports
- Full access to the admin panel

### Admin
- Assign tasks to their users
- View and manage tasks assigned to their users
- View completion reports (including worked hours) submitted by users
- Cannot manage user roles

### User
- View assigned tasks
- Update task status and submit completion reports (with worked hours)
- Can only interact with their own tasks

---

## Setup

### Requirements

- Python 3.8+
- See [`requirements.txt`](requirements.txt) for Python dependencies

### Installation

1. **Clone the repository:**
    ```sh
    git clone <your-repo-url>
    cd task_management -project
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    venv\Scripts\activate  # On Windows
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations:**
    ```sh
    python manage.py migrate
    ```

5. **Create a superuser:**
    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**
    ```sh
    python manage.py runserver
    ```

---

## Usage

- **Login:**  
  Visit [http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/) to log in.
- **SuperAdmin Panel:**  
  [http://127.0.0.1:8000/superadmin/dashboard/](http://127.0.0.1:8000/superadmin/dashboard/)
- **Admin Panel:**  
  [http://127.0.0.1:8000/api/admin/dashboard/](http://127.0.0.1:8000/api/admin/dashboard/)
- **Django Admin:**  
  [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Project Structure

```
core/
    models.py
    views.py
    forms.py
    urls.py
    templates/
        admin/
        superadmin/
        registration/
task_management/
    settings.py
    urls.py
requirements.txt
```

---

## API

- JWT authentication is enabled.
- Obtain token: `POST /api/token/`
- Refresh token: `POST /api/token/refresh/`
- User APIs: `/api/tasks/`, `/api/tasks/<id>/`, etc.

---

## Customization

- **Roles:**  
  The `User` model includes a `role` field (`superadmin`, `admin`, `user`).
- **Assigning Users to Admins:**  
  Use the `assigned_admin` field in the user form.

---

## License

MIT License

---

## Credits

- Built with [Django](https://www.djangoproject.com/) and [Django REST Framework](https://www.django-rest-framework.org/).
