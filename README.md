# JANAPATHA – Road Hazard Reporting & Follow-Up System

**Every Road Matters, Every Voice Counts.**

JANAPATHA is a web-based Road Hazard Reporting and Follow-Up System developed using Python and Django. It provides a platform for residents to report road-related problems and track their complaints until resolution.

The system helps administrators manage complaints, assign them to the appropriate departments, and allows department staff to update complaint progress and resolution details.

## Features

### Resident Module
- Resident registration and login.
- Submit road hazard complaints with descriptions and photographs.
- Track complaint status using the resident dashboard.
- View complaint details and progress history.
- Receive email notifications when complaints are resolved.

### Admin Module
- Secure administrator login.
- View and manage submitted complaints.
- Create and manage departments.
- Register department staff.
- Assign complaints to appropriate departments.
- Add administrative remarks.
- Monitor complaint status and overall progress.

### Staff Module
- Secure staff login.
- View complaints assigned to their department.
- Take responsibility for complaints.
- Update complaint progress.
- Mark complaints as completed.
- Add remarks and upload evidence photographs.

### Email Notifications
- Email notification to the administrator when a new complaint is submitted.
- Department email notification when a complaint is assigned.
- Resident email notification when a complaint is resolved.

## Technologies Used

| Category | Technologies |
|---|---|
| Backend | Python, Django |
| Frontend | HTML, CSS, Bootstrap 5, JavaScript |
| Database | MySQL |
| Image Handling | Pillow |
| Environment Configuration | python-dotenv |
| Version Control | Git, GitHub |

## Project Structure

```text
JANAPATHA/
│
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── complaints/
│   ├── migrations/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── janapatha/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   ├── accounts/
│   ├── complaints/
│   ├── base.html
│   └── home.html
│
├── static/
│   ├── css/
│   └── images/
│
├── media/
├── manage.py
├── requirements.txt
└── .gitignore
```

## Installation and Setup

Follow these steps to run JANAPATHA locally.

### 1. Clone the Repository

```bash
git clone https://github.com/A7hay/janapatha-road-hazard-system.git
```

### 2. Navigate to the Project Folder

```bash
cd janapatha-road-hazard-system
```

### 3. Create a Virtual Environment

```bash
python -m venv env
```

Activate it on Windows:

```powershell
env\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root directory (the same folder as `manage.py`).

Add your own configuration:

```env
SECRET_KEY=your_django_secret_key

DB_NAME=janapatha
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
```

**Important:** Replace the example values with your actual local configuration. Never upload your `.env` file or expose passwords and secret keys on GitHub.

### 6. Create the MySQL Database

Open MySQL and execute:

```sql
CREATE DATABASE janapatha;
```

### 7. Apply Database Migrations

```bash
python manage.py migrate
```

### 8. Create an Administrator Account

```bash
python manage.py createsuperuser
```

Follow the instructions to create your administrator credentials.

### 9. Run the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

## Application Workflow

1. Residents register and log in to the system.
2. Residents submit road hazard complaints with relevant information and photographs.
3. The administrator receives the complaint and assigns it to the appropriate department.
4. The department receives an email notification about the assigned complaint.
5. Department staff access their dashboard and take responsibility for complaints.
6. Staff update complaint progress, add remarks and upload evidence.
7. Once the complaint is resolved, its status is marked as completed.
8. The resident receives an email notification about the resolution.

## Security

- Role-based access for residents, administrators and staff.
- Django authentication and password management.
- CSRF protection through Django forms.
- Environment variables for sensitive configuration.
- `.gitignore` to exclude environment files and virtual environments.

## Future Enhancements

- Complaint tracking through unique tracking numbers.
- Improved dashboard analytics and reporting.
- Interactive map integration for complaint locations.
- Deployment to a production hosting platform.

## Project Information

**Project Name:** JANAPATHA

**Project Type:** Full-Stack Web Application

**Framework:** Django

**Database:** MySQL

**Development Status:** Completed

**Developer:** Abhay Dev P

**GitHub Repository:**  
https://github.com/A7hay/janapatha-road-hazard-system

---

*JANAPATHA – Every Road Matters, Every Voice Counts.*