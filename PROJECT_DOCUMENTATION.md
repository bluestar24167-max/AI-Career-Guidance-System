# AI-Powered Career Guidance System
## Complete Project Documentation & Team Learning Guide

---

**Project Name:** AI-Powered Career Guidance System (branded as *CareerFlow*)
**Technology Stack:** Python, Django, MySQL, Ollama (Llama 3.2), Bootstrap, HTML/CSS/JavaScript
**Project Type:** Academic / Educational Web Application

---

# TABLE OF CONTENTS

**PART 1 — DETAILED DOCUMENTATION**

- Chapter 1 – Project Overview
- Chapter 2 – Complete Project Workflow
- Chapter 3 – How the Project Was Built From Scratch
- Chapter 4 – Detailed Django Request-Response Cycle
- Chapter 5 – Actual Project Folder Structure
- Chapter 6 – Complete User Journey
- Chapter 7 – Important Code Concepts
- Chapter 8 – Database and Data Flow
- Chapter 9 – Running the Project on Another Computer
- Chapter 10 – Git and GitHub Workflow
- Chapter 11 – Project Challenges and Lessons Learned
- Chapter 12 – Future Improvements

**PART 2 — TECHNICAL WORKFLOWS**

**PART 3 — TEAM KNOWLEDGE ASSIGNMENTS**

**PART 4 — FINAL TEAM LEARNING CHECKLIST**

---
---

# PART 1 — DETAILED DOCUMENTATION

---

## CHAPTER 1 — PROJECT OVERVIEW

### 1.1 Project Name

**AI-Powered Career Guidance System** — branded in the application as **CareerFlow**.

### 1.2 Introduction

The AI-Powered Career Guidance System is a web application that helps students choose the right career path by analysing their educational background, skills, interests, and career preferences. Instead of giving the same generic advice to every student, this system uses Artificial Intelligence (AI) to provide personalised, role-specific career guidance.

The system is built with Python and Django on the backend, MySQL for the database, Bootstrap for the frontend, and Ollama (running the Llama 3.2 large language model) for the AI functionality.

### 1.3 Background

Today's job market changes rapidly. New roles appear every year, technology creates new opportunities, and students often feel overwhelmed by the number of choices available. Traditional career counselling — whether from a school counsellor or an online quiz — typically provides generic advice that does not consider each student's unique profile.

This project addresses that gap by building an intelligent system that takes a student's specific information (education, skills, interests) and uses AI to generate personalised career recommendations, aptitude assessments, and a structured learning roadmap.

### 1.4 Problem Statement

Choosing the right career can be difficult for students because:

- There are many career options and technology is continuously creating new opportunities.
- Traditional career counselling may provide generalised recommendations that do not consider an individual's specific skills, interests, educational background, and career preferences.
- Students often lack a clear, actionable plan for entering their chosen career.
- There is no easy way for students to assess their own readiness for specific roles.

### 1.5 Need for the Project

There is a clear need for a system that can:

1. Understand each student's unique profile (education, skills, interests).
2. Recommend specific career paths and job roles tailored to that profile.
3. Assess a student's readiness for those roles through aptitude testing.
4. Provide a structured learning roadmap with concrete steps and resources.
5. Deliver everything in a single, easy-to-use web application.

### 1.6 Proposed Solution

The **AI-Powered Career Guidance System** is a web application that:

1. Collects student information (education, branch, skills, interests).
2. Uses AI to recommend career categories and job roles.
3. Lets students choose their target roles.
4. Generates role-specific aptitude questions using AI.
5. Evaluates student performance and identifies strengths and skill gaps.
6. Produces a personalised career report with:
   - Career suitability analysis
   - Strengths and areas for improvement
   - A step-by-step learning roadmap with curated resources
   - A LinkedIn job search link for the chosen roles
7. Allows students to download a PDF version of their career report.

### 1.7 Target Users

- **Primary Users:** College and university students seeking career guidance.
- **Secondary Users:** Career counsellors who want to recommend a structured tool to students.
- **Administrators:** Faculty or administrators who can view all registered students and assessments via an admin dashboard.

### 1.8 Main Objectives

1. Help students make informed career decisions.
2. Provide personalised rather than generic career guidance.
3. Identify suitable career paths based on individual student profiles.
4. Evaluate knowledge through role-specific aptitude tests.
5. Provide actionable learning recommendations with trusted resource links.
6. Generate downloadable PDF career reports.
7. Track student assessment history over time.

### 1.9 Major Features

| Feature | Description |
|---|---|
| Student Registration & Login | Students create accounts and log in with email and password |
| Profile Management | Students add and edit their education, skills, and interests |
| AI Role Suggestions | AI suggests complementary job roles based on the student's interests |
| Target Role Selection | Students choose from popular roles or add custom roles |
| AI-Generated Aptitude Test | 10 role-specific multiple-choice questions generated by AI |
| Assessment Evaluation | Automatic scoring and identification of strengths and skill gaps |
| AI Career Summary | An AI-generated evidence-based career readiness analysis |
| Learning Roadmap | A structured 4-stage learning plan with curated resource links |
| Career Recommendation Page | A full-page view of the student's personalised roadmap and insights |
| PDF Report Download | A downloadable PDF containing the student's profile, score, and AI recommendation |
| Assessment History | A table showing all past assessments with dates and scores |
| Admin Dashboard | An admin page showing total students, assessments, and a summary of all data |

---

## CHAPTER 2 — COMPLETE PROJECT WORKFLOW

### 2.1 Main Application Flow (End-to-End)

This is the primary workflow from start to finish:

```
START
  ↓
Student opens the application (home page)
  ↓
Student registers or logs in
  ↓
Django receives the request, creates/checks session
  ↓
Student is directed to the Dashboard
  ↓
Student fills in profile (education, skills, interests)
  ↓
Student clicks "Start AI Assessment"
  ↓
Role Selection page opens
  ↓
Student selects target roles (from popular list, search, or custom input)
  ↓
[Optional] Student clicks "Suggest roles from my interests" → AI generates complementary role suggestions
  ↓
Student confirms roles and clicks "Confirm roles & start assessment"
  ↓
Django calls AI Engine to generate aptitude questions
  ↓
AI generates 10 role-specific multiple-choice questions
  ↓
Questions are displayed to the student
  ↓
Student answers all 10 questions
  ↓
Django evaluates answers (compares selected vs. correct answer)
  ↓
AI generates a career readiness summary based on performance
  ↓
A learning roadmap is built (from curated resources, matched to the role track)
  ↓
Results page displays: score, AI summary, strengths, skill gaps, learning roadmap
  ↓
Student can view the full "Career Recommendation" page
  ↓
Student can download the PDF report
  ↓
END
```

### 2.2 User Registration and Login Flow

```
Student visits /register/
  ↓
Fills in: full name, email, password, education, branch, year, college, city, phone, skills, interests
  ↓
Submits form (POST request)
  ↓
Django validates the form using StudentRegistrationForm (ModelForm)
  ↓
Student record is saved to the database
  ↓
Student is redirected to /login/
  ↓
Student enters email and password
  ↓
Django queries Student table for matching email + password
  ↓
If found: session is created (student_id, student_name stored in session)
  ↓
If not found: "Invalid Email or Password" error is displayed
  ↓
Student is redirected to /dashboard/
```

### 2.3 Assessment Flow

```
Student clicks "Start AI Assessment" from Dashboard
  ↓
Role Selection page opens (/assessment/)
  ↓
Student browses popular roles or adds custom roles
  ↓
[Optional] AI suggests complementary roles via /assessment/recommend-roles/
  ↓
Student submits selected roles (POST to /assessment/)
  ↓
Roles are saved to student.profile (target_roles field) and stored in session
  ↓
Student is redirected to /assessment/test/
  ↓
Django calls generate_job_assessment(roles) → sends prompt to Ollama
  ↓
AI returns 10 multiple-choice questions in JSON format
  ↓
Questions are validated and displayed in the test template
  ↓
Student selects one option for each question
  ↓
Form is submitted (POST to /assessment/test/)
  ↓
Django iterates through questions, compares selected vs. correct answer
  ↓
Score is calculated (number of correct answers)
  ↓
analyze_performance() is called → AI generates career readiness summary
  ↓
build_learning_roadmap() creates a structured roadmap from curated resources
  ↓
Assessment record is saved to database (student, roles, score, answers, analysis, report)
  ↓
Results page is displayed (/assessment/test/ → result.html)
```

### 2.4 Career Recommendation and PDF Download Flow

```
Student clicks "View my roadmap" or "Open full roadmap"
  ↓
/careers/recommend/ page opens
  ↓
Django fetches the student's most recent Assessment record
  ↓
The page displays: AI summary, learning roadmap, strengths, skill gaps, job search link
  ↓
Student clicks "Download report ↓"
  ↓
/careers/download-report/ view is triggered
  ↓
download_pdf() generates a PDF using ReportLab
  ↓
PDF contains: student details, target roles, score, AI recommendation text
  ↓
PDF file is returned to the browser as a downloadable file (AI_Career_Report.pdf)
```

### 2.5 Admin Dashboard Flow

```
Admin visits /admin-dashboard/
  ↓
Django fetches all Student records and all Assessment records
  ↓
Dashboard page displays:
  - Total Students count
  - Total Assessments count
  - Reports Generated count
  - Table of all registered students (ID, name, email, education, branch, city)
  - Table of all assessments (student name, target roles, score, report text)
```

---

## CHAPTER 3 — HOW THE PROJECT WAS BUILT FROM SCRATCH

### Step 1: Planning the Project

Before writing any code, the project was planned by:

**Identifying the Problem:**
Students struggle to find careers that match their unique skills, interests, and educational background. Generic career advice is not personalised enough.

**Defining the Users:**
The primary users are college/university students. Administrators can also view data.

**Deciding the Features:**
- Student registration and login
- Profile management (education, skills, interests)
- AI-powered career recommendations
- Role-specific aptitude assessments
- Personalised career reports
- PDF report download
- Admin dashboard

**Designing the User Workflow:**
Register → Login → Fill Profile → Choose Roles → Take Assessment → View Results → View Roadmap → Download Report

**Choosing the Technology Stack:**

| Component | Technology | Why |
|---|---|---|
| Backend | Python + Django | Django is a powerful, beginner-friendly framework with built-in admin, ORM, and template engine |
| Frontend | HTML + CSS + Bootstrap + JavaScript | Bootstrap provides responsive design; JavaScript handles dynamic UI (role selection, AI suggestions) |
| Database | MySQL | Reliable relational database for storing students, careers, and assessments |
| AI | Ollama + Llama 3.2 | A local, free, open-source LLM running on Ollama — no paid API keys required |
| PDF Generation | ReportLab | A Python library for generating PDF documents programmatically |
| Environment Variables | python-dotenv | Securely loads secrets from a `.env` file |

---

### Step 2: Setting Up Python

Python is the programming language used for this project. Django is a Python web framework, so Python must be installed first.

**How to install Python:**
1. Visit https://www.python.org/downloads/
2. Download the latest version for your operating system.
3. During installation on Windows, check "Add Python to PATH".
4. On macOS/Linux, Python is usually pre-installed.

**How to check your Python version:**
```bash
python --version
```
or
```bash
python3 --version
```

You should see a version number like `Python 3.11.0` or higher.

**Why Python?**
- Easy to read and write.
- Huge library ecosystem (Django, ReportLab, requests, etc.).
- Excellent for web development and AI integration.
- Large community and many learning resources.

---

### Step 3: Creating a Virtual Environment

**What is a virtual environment?**
A virtual environment is an isolated copy of Python for a specific project. It keeps the packages (libraries) for one project separate from other projects on the same computer.

**Why is it necessary?**
Without a virtual environment, every project would share the same set of installed packages. If Project A needs Django 4.0 and Project B needs Django 6.0, they would conflict. A virtual environment solves this by giving each project its own set of packages.

**How to create one:**
```bash
python -m venv venv
```
This creates a folder called `venv` in your project directory.

**How to activate it:**

On Windows:
```bash
venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

After activation, your terminal prompt will usually show `(venv)` at the beginning, indicating the virtual environment is active.

**How to deactivate:**
```bash
deactivate
```

---

### Step 4: Installing Django

**What is Django?**
Django is a high-level Python web framework. It provides tools and shortcuts that make building websites much faster than writing everything from scratch. Django follows the "batteries included" philosophy — it includes an admin panel, database management, form handling, security features, and more.

**Why was Django selected?**
- Built-in admin panel (we use this for the admin dashboard).
- ORM (Object-Relational Mapper) for working with databases using Python code instead of raw SQL.
- Template engine for mixing Python logic with HTML.
- Excellent security features (CSRF protection, SQL injection prevention).
- Large community and documentation.

**How to install Django:**
```bash
pip install Django
```

For this project, we also install several other packages (listed in `requirements.txt`):
```bash
pip install -r requirements.txt
```

Key packages installed include:
- `Django==6.0.7` — the web framework
- `mysqlclient==2.2.8` — allows Django to connect to MySQL
- `requests==2.34.2` — for making HTTP requests to the Ollama AI service
- `reportlab==5.0.0` — for generating PDF reports
- `python-dotenv==1.0.1` — for loading environment variables from a `.env` file
- `google-generativeai` and `groq` — alternative AI provider libraries (not actively used in the current version)

---

### Step 5: Creating the Django Project

**Creating the project:**
```bash
django-admin startproject career_guidance
```

This creates a project folder called `career_guidance` with the following files:

| File | What it does |
|---|---|
| `manage.py` | A command-line tool for managing the project (running the server, creating migrations, etc.) |
| `settings.py` | The main configuration file — database settings, installed apps, secret key, etc. |
| `urls.py` | The main URL routing file — maps web addresses to views |
| `wsgi.py` | Web Server Gateway Interface — used for deploying the application on a production server |
| `asgi.py` | Asynchronous Server Gateway Interface — used for asynchronous deployment (not needed in development) |

**What is `manage.py`?**
This file is the entry point for all Django management commands. When you run `python manage.py runserver`, `python manage.py migrate`, etc., Django uses this file.

The most important line in `manage.py` is:
```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'career_guidance.settings')
```
This tells Django to use `career_guidance/settings.py` for all configuration.

---

### Step 6: Creating Applications

**What is the difference between a Django project and a Django app?**

- A **Django project** is the entire web application (in our case, the AI-Powered Career Guidance System).
- A **Django app** is a single module within the project that handles a specific feature.

Think of it like a university: the university is the project, and each department (Computer Science, Mathematics, English) is an app. Each app has its own models, views, URLs, and templates.

**Why divide into multiple apps?**
- Keeps code organised and modular.
- Makes it easier for different team members to work on different parts.
- Makes the codebase easier to understand and maintain.

**The apps in our project (registered in `settings.py`):**

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',        # User authentication (registration, login, logout)
    'students',        # Student profile model and forms
    'careers',         # Career listing, recommendations, and PDF download
    'assessment',      # Aptitude test generation, submission, and evaluation
    'ai_engine',       # AI integration with Ollama (the brain of the system)
    'reports',         # Report-related functionality (currently placeholder)
    'adminpanel',      # Admin dashboard view
]
```

**Responsibility of each app:**

| App | Responsibility |
|---|---|
| `accounts` | Home page, login, registration, logout, dashboard, profile viewing, profile editing |
| `students` | Student data model, student registration form |
| `careers` | Career listing, career detail view, career recommendation page, PDF report download |
| `assessment` | Target role selection, role recommendations, aptitude test generation, test submission, evaluation, assessment history |
| `ai_engine` | Ollama connection, prompt engineering, assessment question generation, performance analysis, learning roadmap building |
| `adminpanel` | Admin dashboard showing all students and assessments |
| `reports` | Placeholder app for future report functionality (currently empty) |

---

### Step 7: Creating Models and Database Structure

**What is a database?**
A database is a structured way to store and retrieve data. Think of it like a set of spreadsheets — each spreadsheet is a "table," each column is a "field," and each row is a "record."

**What are Django models?**
Django models are Python classes that define the structure of your database tables. Instead of writing SQL commands, you write Python code, and Django translates it into database operations.

**The models in our project:**

#### Student Model (`students/models.py`)

```python
class Student(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    education = models.CharField(max_length=100, blank=True)
    branch = models.CharField(max_length=100, blank=True)
    year = models.CharField(max_length=30, blank=True)
    college = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    skills = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    target_roles = models.JSONField(default=list, blank=True)
    experience_level = models.CharField(max_length=30, default="Beginner")
    created_at = models.DateTimeField(auto_now_add=True)
```

| Field | Purpose |
|---|---|
| `full_name` | Student's full name |
| `email` | Unique email address (used for login) |
| `password` | Password stored as plain text *(note: this should be hashed in production)* |
| `education` | Educational qualification (Diploma, B.Tech, Degree, etc.) |
| `branch` | Specialization (Computer Engineering, IT, etc.) |
| `year` | Current year of study (1st, 2nd, 3rd, Final) |
| `college` | Name of the college or university |
| `city` | City where the student is located |
| `phone` | Phone number |
| `skills` | Free-text field for technical skills (e.g., "Python, HTML, CSS") |
| `interests` | Free-text field for career interests (e.g., "AI, Web Development") |
| `target_roles` | JSON field storing a list of target roles the student has selected |
| `experience_level` | Defaults to "Beginner" |
| `created_at` | Automatically set when the student is created |

#### Career Model (`careers/models.py`)

```python
class Career(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    required_skills = models.TextField()
    average_salary = models.CharField(max_length=50)
```

This model stores predefined career listings (title, description, skills, salary).

#### Assessment Model (`assessment/models.py`)

```python
class Assessment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    target_roles = models.JSONField(default=list)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    report = models.TextField()
    answers = models.JSONField(default=list)
    analysis = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
```

| Field | Purpose |
|---|---|
| `student` | Links to the Student who took the assessment (foreign key) |
| `target_roles` | The roles the student was assessed for |
| `score` | Number of correct answers |
| `total_questions` | Total number of questions (always 10) |
| `report` | The AI-generated career readiness summary text |
| `answers` | JSON list of every question, the student's selected answer, whether it was correct, and the skill tested |
| `analysis` | JSON object containing `strengths`, `skill_gaps`, `summary`, and `roadmap` |
| `created_at` | Timestamp when the assessment was completed |

**Migrations:**
Migrations are Django's way of applying model changes to the database. When you create or modify a model, you run:

```bash
python manage.py makemigrations    # Creates a migration file (a plan for database changes)
python manage.py migrate           # Applies the migration file to the actual database
```

In this project, migrations were created for:
- `students` — creates the `students_student` table
- `careers` — creates the `careers_career` table
- `assessment` — creates the `assessment_assessment` table

---

### Step 8: Creating Views

**What is a Django view?**
A view is a Python function (or class) that receives a web request and returns a web response. It is the "brain" of each page — it decides what data to fetch, how to process it, and which template to render.

**How views work:**

```
Browser sends a request → Django matches URL → Calls the view function → View processes data → Returns an HTML page (or JSON/redirect)
```

**Key views in this project:**

| View | File | What it does |
|---|---|---|
| `home` | `accounts/views.py` | Renders the home page |
| `login_page` | `accounts/views.py` | Handles student login (email + password) |
| `register_page` | `accounts/views.py` | Handles student registration |
| `dashboard` | `accounts/views.py` | Shows the student dashboard after login |
| `profile` | `accounts/views.py` | Displays the student's profile |
| `edit_profile` | `accounts/views.py` | Allows editing profile fields |
| `choose_targets` | `assessment/views.py` | Role selection page — lets students pick target roles |
| `role_recommendations` | `assessment/views.py` | AJAX endpoint — returns AI-suggested roles as JSON |
| `aptitude_test` | `assessment/views.py` | Generates and displays the AI aptitude test, then evaluates answers |
| `assessment_history` | `assessment/views.py` | Shows all past assessments |
| `career_list` | `careers/views.py` | Lists all careers |
| `recommend_career` | `careers/views.py` | Shows the full personalised roadmap page |
| `download_report` | `careers/views.py` | Generates and downloads a PDF report |
| `admin_dashboard` | `adminpanel/views.py` | Admin page with student and assessment summaries |

---

### Step 9: Creating URLs

**What is URL routing?**
URL routing is how Django decides which view function to call based on the web address the user visits. Each URL pattern is like a mapping: "When the user visits this address, call this view."

**How URL routing works in this project:**

Django uses a two-level URL system:

1. **Main `urls.py`** (`career_guidance/urls.py`) — the root URL configuration.
2. **App-level `urls.py`** files (`assessment/urls.py`, `careers/urls.py`, `adminpanel/urls.py`) — handle URLs for specific apps.

**Main URL Configuration (`career_guidance/urls.py`):**

```python
from django.contrib import admin
from django.urls import path, include
from accounts import views

urlpatterns = [
    # Home
    path("", views.home, name="home"),

    # Authentication
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("logout/", views.logout_page, name="logout"),

    # Student
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),

    # Apps
    path("assessment/", include("assessment.urls")),
    path("careers/", include("careers.urls")),

    # Django Admin
    path("admin/", admin.site.urls),

    # Admin Dashboard
    path("admin-dashboard/", include("adminpanel.urls")),
]
```

**Breaking down the syntax:**

```python
path("assessment/", include("assessment.urls"))
```

- `"assessment/"` — the URL prefix. When a user visits `/assessment/`, Django strips this prefix and passes the rest to the included URL file.
- `include("assessment.urls")` — Django now looks at `assessment/urls.py` for the remaining URL pattern.
- So, a visit to `/assessment/test/` is matched by `path("test/", ...)` inside `assessment/urls.py`.

**Assessment URL Configuration (`assessment/urls.py`):**

```python
urlpatterns = [
    path("", views.choose_targets, name="choose_targets"),
    path("recommend-roles/", views.role_recommendations, name="role_recommendations"),
    path("test/", views.aptitude_test, name="assessment_test"),
    path("history/", views.assessment_history, name="assessment_history"),
]
```

| URL | View | Name |
|---|---|---|
| `/assessment/` | `choose_targets` | `choose_targets` |
| `/assessment/recommend-roles/` | `role_recommendations` | `role_recommendations` |
| `/assessment/test/` | `aptitude_test` | `assessment_test` |
| `/assessment/history/` | `assessment_history` | `assessment_history` |

**Careers URL Configuration (`careers/urls.py`):**

```python
urlpatterns = [
    path("", views.career_list, name="career_list"),
    path("<int:career_id>/", views.career_detail, name="career_detail"),
    path("recommend/", views.recommend_career, name="recommend_career"),
    path("download-report/", views.download_report, name="download_report"),
]
```

The `<int:career_id>` is a URL parameter — it captures a number from the URL and passes it to the view as `career_id`. For example, `/careers/5/` passes `career_id=5`.

**The complete URL flow:**

```
Browser URL → urls.py → View function → Processing → Template/Response → Browser displays page
```

---

### Step 10: Creating Templates

**What are templates?**
Templates are HTML files with special Django syntax that allow you to display dynamic data. They connect the Python backend (views) with the frontend (what the user sees).

**How templates work:**

1. A view function fetches data and passes it to a template.
2. The template uses Django template tags (`{{ variable }}`, `{% tag %}`) to insert that data into HTML.
3. Django sends the rendered HTML back to the browser.

**Template inheritance:**
All templates in this project extend a single base template called `base.html`. This means:

- `base.html` contains the common structure: navigation bar, Bootstrap CSS/JS, fonts, and a footer.
- Each page template defines only its unique content inside `{% block content %}...{% endblock %}`.

**Base Template (`templates/base.html`):**

The base template includes:
- Bootstrap 5.3.7 CSS and JS (loaded from CDN)
- Google Fonts (DM Sans and Space Grotesk)
- A custom stylesheet (`static/css/style.css`)
- A responsive navigation bar with conditional links (shows "Dashboard" and "Log out" if logged in, or "Log in" and "Get started" if not)
- A `{% block content %}` area where child templates insert their content

**Template structure:**

```
templates/
├── base.html                 # Base template (shared layout)
├── home/
│   └── index.html            # Home/landing page
├── accounts/
│   ├── login.html            # Login page
│   └── register.html         # Registration page
├── students/
│   ├── dashboard.html        # Student dashboard
│   ├── profile.html          # Profile view
│   └── edit_profile.html     # Profile edit form
├── assessment/
│   ├── roles.html            # Target role selection (with inline JavaScript)
│   ├── test.html             # Aptitude test questions
│   ├── result.html           # Assessment results (score, roadmap, strengths, gaps)
│   └── history.html          # Assessment history table
├── careers/
│   ├── list.html             # Career listing page
│   ├── detail.html           # Individual career detail page
│   └── recommendation.html   # Full personalised roadmap page
└── adminpanel/
    └── dashboard.html        # Admin dashboard
```

**Key template features used:**

- **Template variables:** `{{ student.full_name }}`, `{{ assessment.score }}`
- **Template tags:** `{% if %}`, `{% for %}`, `{% empty %}`
- **Template filters:** `{{ student.full_name|slice:":1" }}` (gets the first character for the avatar), `{{ student.skills|default:"Not added" }}`, `{{ assessment.created_at|date:"M j, Y" }}`
- **Template inheritance:** `{% extends "base.html" %}`, `{% block title %}...{% endblock %}`, `{% block content %}...{% endblock %}`
- **Static files:** `{% load static %}`, `{% static 'css/style.css' %}`
- **URL reverse:** `{% url 'choose_targets' %}`, `{% url 'role_recommendations' %}`
- **Auto-escaping:** `{{ student.interests|escapejs }}` (safely embeds user data inside JavaScript)

---

### Step 11: Creating Static Files

**What are static files?**
Static files are files that don't change dynamically — CSS stylesheets, JavaScript files, images, and fonts.

**How Django serves static files:**

In `settings.py`:
```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

This tells Django to look for static files in the `static/` folder at the project root.

**Static file structure:**

```
static/
├── css/
│   └── style.css        # All custom CSS styles
└── js/                  # (currently empty — JavaScript is inline in templates)
```

During development (`DEBUG = True`), Django automatically serves static files. In production, you would use a web server like Nginx or a service like AWS S3.

---

### Step 12: Integrating AI

This is a major component of the project. The AI functionality uses **Ollama** running the **Llama 3.2 (3B parameter)** large language model locally on the developer's machine.

#### What the AI Component Does

The AI is used for three core tasks:

1. **Generating role-specific aptitude questions** — Given a list of target roles, AI creates 10 multiple-choice questions that test skills relevant to those roles.
2. **Generating a career readiness summary** — After a student completes the assessment, AI analyses their strengths and gaps and writes a personalised career readiness statement.
3. **Suggesting complementary career roles** — When a student selects some roles, AI suggests additional roles that match their interests.

#### How Ollama Works

Ollama is a tool that lets you run large language models (LLMs) locally on your computer. Instead of calling a cloud API (like OpenAI or Google), you call a local server running on your machine.

**The Ollama connection (`ai_engine/ollama.py`):**

```python
import requests

def generate_response(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2:3b", "prompt": prompt, "stream": False},
            timeout=90,
        )
        response.raise_for_status()
        return response.json().get("response", "We could not generate a detailed AI summary.")
    except (requests.RequestException, ValueError, KeyError):
        return "AI summary is temporarily unavailable."
```

**What this code does:**
1. Sends an HTTP POST request to `http://localhost:11434/api/generate` — this is the address where Ollama runs locally.
2. Sends the prompt (the text instructions) along with the model name (`llama3.2:3b`).
3. Waits for the AI to respond (up to 90 seconds).
4. Returns the AI's response as a string.
5. If anything goes wrong (Ollama is not running, network error, etc.), returns a graceful fallback message.

#### How Prompts Are Structured

Each AI call uses a carefully crafted prompt. Here are the three main prompts:

**Prompt 1: Generating Aptitude Questions (`ai_engine/assessment_engine.py`):**

```python
prompt = f"""
Create exactly 10 multiple-choice questions strictly for these confirmed target job roles: {', '.join(roles)}.
Test only shared or directly relevant technical concepts, practical workplace scenarios, tools, and domain skills needed for these roles.
Do not ask about the student's interests, personality, education, or unrelated aptitude.
Return JSON only: {{"questions":[{{"question":"...","options":["...","...","...","..."],"answer":"exact option","skill":"specific competency"}}]}}.
Every question has four options, one correct answer, and a concrete competency label.
"""
```

This prompt instructs the AI to:
- Create exactly 10 questions.
- Focus only on the skills needed for the specified roles.
- Return results in JSON format with `question`, `options`, `answer`, and `skill` fields.
- Validate: the response is only accepted if it has exactly 10 questions, each with 4 options, a valid answer, and a skill label.

**Prompt 2: Career Readiness Summary (`ai_engine/assessment_engine.py`):**

```python
prompt = f"""
Assess job readiness for target roles: {', '.join(roles)}. Score: {score}/{total}.
Demonstrated strengths: {', '.join(strengths) or 'None yet'}.
Skill gaps: {', '.join(gaps) or 'None identified'}.
Write a concise evidence-based summary: what is ready, what to prioritise next, and a realistic readiness statement. Do not mention interests.
"""
```

This tells the AI to write a concise, evidence-based summary of the student's career readiness based on their assessment performance.

**Prompt 3: Role Suggestions (`ai_engine/job_recommendations.py`):**

```python
prompt = f"""
You are a career adviser. Suggest 3 to 5 complementary job roles for a student.
Interests: {interests or 'Not provided'}
Current target roles: {', '.join(current_roles) or 'None'}
Return JSON only: {{"roles": [{{"name": "Role", "reason": "Short specific reason"}}]}}.
Do not repeat current roles. Keep every reason under 24 words.
"""
```

#### Fallback Mechanisms

Every AI call has a fallback. If Ollama is down or returns invalid data:

- **Aptitude questions:** Falls back to a set of 10 pre-written general professional questions (stored in `_fallback_questions()`).
- **Career summary:** Returns a default summary message.
- **Role suggestions:** Returns a hardcoded list of 5 popular roles (Software Engineer, Data Analyst, Cloud Engineer, QA Engineer, Product Designer).

This means the application still works even when AI is unavailable.

#### The Learning Roadmap (`ai_engine/roadmap.py`)

The roadmap is built locally (no AI call needed). It uses a curated `RESOURCE_LIBRARY` dictionary that maps role tracks (web, backend, data, ml, design, security, general) to structured lessons. Each lesson has a title, outcome, provider, URL, duration, instructions, and a project idea.

The `_track_for()` function determines which track to use based on the student's target roles:
- "Machine Learning", "AI Engineer" → `ml` track
- "Data Analyst", "BI Analyst" → `data` track
- "UX Designer", "Product Designer" → `design` track
- "Cybersecurity", "Security Analyst" → `security` track
- "Backend Developer", "Software Engineer" → `backend` track
- "Frontend Developer", "Full Stack" → `web` track
- Everything else → `general` track

#### Security Practices

- **No API keys are exposed in the code.** Ollama runs locally and does not require API keys.
- The `.env` file (which stores `DJANGO_SECRET_KEY` and database credentials) is listed in `.gitignore` and is never uploaded to GitHub.
- Environment variables are loaded using `python-dotenv` in `settings.py`.

---

## CHAPTER 4 — DETAILED DJANGO REQUEST-RESPONSE CYCLE

Every time a user interacts with the website, the following cycle occurs:

### Stage 1: User Action
The user clicks a button, fills in a form, or types a URL in the browser.

### Stage 2: Browser Sends HTTP Request
The browser sends an HTTP request (GET or POST) to the Django server. For example:
- **GET** `/dashboard/` — "Give me the dashboard page."
- **POST** `/assessment/test/` — "Here are my assessment answers."

### Stage 3: Django Receives the Request
Django's development server receives the request and begins processing it.

### Stage 4: URL Routing
Django's URL resolver (`career_guidance/urls.py`) examines the URL path and finds the matching pattern:
```python
path("dashboard/", views.dashboard, name="dashboard")
```
If the URL starts with `/assessment/`, Django follows the `include("assessment.urls")` directive and looks at `assessment/urls.py` for the remaining path.

### Stage 5: View Function is Called
Django calls the corresponding view function (e.g., `dashboard(request)`). The view receives the `request` object, which contains:
- The HTTP method (GET or POST)
- Form data (for POST requests)
- Session data (including `student_id` if logged in)
- URL parameters

### Stage 6: View Processes Data
The view performs its logic:
- Checks if the user is logged in (by checking `request.session["student_id"]`)
- Fetches data from the database (e.g., `Student.objects.get(id=...)`)
- Calls AI functions if needed (e.g., `generate_job_assessment(roles)`)
- Saves data to the database (e.g., `Assessment.objects.create(...)`)

### Stage 7: Database and/or AI Service
If the view needs data:
- **Database:** Django's ORM translates Python code into SQL queries. For example, `Student.objects.get(id=5)` becomes `SELECT * FROM students_student WHERE id = 5`.
- **AI Service:** The view sends a prompt to Ollama via HTTP POST and receives the AI's response.

### Stage 8: View Prepares the Response
The view returns a response — typically a rendered template or a redirect:
```python
return render(request, "students/dashboard.html", {"student": student})
```
This tells Django to render the `dashboard.html` template and pass the `student` variable to it.

### Stage 9: Template Renders Data
Django's template engine processes the template:
- Replaces `{{ student.full_name }}` with the actual name.
- Executes `{% for %}` loops and `{% if %}` conditions.
- Produces a complete HTML document.

### Stage 10: Browser Displays the Result
The rendered HTML is sent back to the browser. The browser parses the HTML, loads CSS and JavaScript, and displays the page to the user.

**Summary flow:**

```
User clicks button
  → Browser sends HTTP request
  → Django receives request
  → urls.py identifies matching URL
  → Django calls the corresponding view
  → View processes data (database/AI)
  → View prepares response (template + context data)
  → Template renders data into HTML
  → Browser displays the page
```

---

## CHAPTER 5 — EXPLAIN THE ACTUAL PROJECT FOLDER STRUCTURE

```
AI_Career_Guidance/
│
├── manage.py                          # Django management script — entry point for all commands
├── requirements.txt                   # Python package dependencies
├── .gitignore                         # Files excluded from Git (venv/, __pycache__/, db.sqlite3, .env)
├── .env                               # Environment variables (SECRET_KEY, DB credentials) — NOT in Git
├── README.md                          # Project overview and setup instructions
├── db.sqlite3                         # SQLite database (used as fallback; main DB is MySQL)
│
├── career_guidance/                   # Main Django project configuration
│   ├── __init__.py
│   ├── settings.py                    # All project settings (DB, apps, static files, secret key)
│   ├── urls.py                        # Root URL configuration — maps URLs to apps
│   ├── wsgi.py                        # WSGI entry point for deployment
│   └── asgi.py                        # ASGI entry point for async deployment
│
├── accounts/                          # Authentication app
│   ├── models.py                      # (empty — uses Student model from students app)
│   ├── views.py                       # home, login, register, logout, dashboard, profile, edit_profile
│   ├── urls.py                        # URL patterns for auth pages
│   └── admin.py                       # (empty)
│
├── students/                          # Student profile app
│   ├── models.py                      # Student model (full_name, email, skills, interests, etc.)
│   ├── forms.py                       # StudentRegistrationForm (ModelForm for registration)
│   ├── views.py                       # (empty — views handled by accounts app)
│   └── admin.py                       # Registers Student model in Django admin
│
├── careers/                           # Career listings and recommendation app
│   ├── models.py                      # Career model (title, description, required_skills, salary)
│   ├── views.py                       # career_list, career_detail, recommend_career, download_report
│   ├── urls.py                        # URL patterns for career pages
│   ├── pdf_report.py                  # PDF generation using ReportLab
│   └── admin.py                       # Registers Career model in Django admin
│
├── assessment/                        # Assessment/quiz app
│   ├── models.py                      # Assessment model (student, score, report, analysis, answers)
│   ├── views.py                       # choose_targets, role_recommendations, aptitude_test, history
│   ├── urls.py                        # URL patterns for assessment pages
│   └── admin.py                       # Registers Assessment model in Django admin
│
├── ai_engine/                         # AI integration (no views — used as a library by other apps)
│   ├── ollama.py                      # Generic Ollama API call function
│   ├── assessment_engine.py           # generate_job_assessment(), analyze_performance(), fallback questions
│   ├── job_recommendations.py         # recommend_roles() — AI role suggestion with fallback
│   ├── roadmap.py                     # build_learning_roadmap() — curated resource-based roadmap
│   └── views.py                       # (empty)
│
├── adminpanel/                        # Admin dashboard app
│   ├── views.py                       # admin_dashboard — shows all students and assessments
│   ├── urls.py                        # URL pattern for /admin-dashboard/
│   └── admin.py                       # (empty)
│
├── reports/                           # Report app (placeholder for future functionality)
│   ├── models.py                      # (empty)
│   └── views.py                       # (empty)
│
├── templates/                         # HTML templates (shared across all apps)
│   ├── base.html                      # Base template (navbar, Bootstrap, fonts, footer)
│   ├── home/index.html                # Landing page
│   ├── accounts/login.html            # Login form
│   ├── accounts/register.html         # Registration form
│   ├── students/dashboard.html        # Student dashboard
│   ├── students/profile.html          # Profile view
│   ├── students/edit_profile.html     # Profile edit form
│   ├── assessment/roles.html          # Role selection (with inline JavaScript for dynamic UI)
│   ├── assessment/test.html           # Aptitude test questions
│   ├── assessment/result.html         # Assessment results with roadmap
│   ├── assessment/history.html        # Assessment history table
│   ├── careers/list.html              # Career listing
│   ├── careers/detail.html            # Career detail page
│   ├── careers/recommendation.html    # Full personalised roadmap page
│   └── adminpanel/dashboard.html      # Admin dashboard
│
└── static/                            # Static files
    └── css/
        └── style.css                  # All custom CSS styles
```

### Files Team Members Should Modify Carefully

| File | Caution Level | Reason |
|---|---|---|
| `career_guidance/settings.py` | HIGH | Controls the entire project configuration. Changing the database, installed apps, or secret key can break the project. |
| `career_guidance/urls.py` | MEDIUM | Root URL routing. Incorrect changes can break all page access. |
| `.env` | HIGH | Contains secret keys and database credentials. Never commit this to Git. |
| `ai_engine/assessment_engine.py` | MEDIUM | Core AI logic. Changing prompts affects question quality and career analysis. |
| `ai_engine/roadmap.py` | MEDIUM | Contains the curated resource library. Changing resources affects the learning roadmap. |
| `students/models.py` | HIGH | Changing the Student model requires new migrations. |
| `assessment/models.py` | HIGH | Changing the Assessment model requires new migrations. |

---

## CHAPTER 6 — EXPLAIN THE COMPLETE USER JOURNEY

### Scenario: A student named Priya uses the application

**Step 1: Priya opens the application**

Priya opens her browser and goes to `http://127.0.0.1:8000/`. The home page loads, showing the CareerFlow branding with the tagline "Your next career move starts with clarity." She sees three steps: Personal profile, Smart assessment, Action plan.

She clicks "Build my roadmap →" to get started.

**Step 2: Priya creates an account**

The registration page opens. She fills in:
- Full name: Priya Sharma
- Email: priya@example.com
- Password: [hidden]
- Education: B.Tech
- Branch: Computer Engineering
- Year: 3rd Year
- College: ABC Engineering College
- City: Mumbai
- Phone: 9876543210
- Skills: Python, HTML, CSS, JavaScript
- Interests: Web Development, Data Science, AI

She clicks "Create account →". Django validates her form using `StudentRegistrationForm`, saves the Student record to the database, and redirects her to the login page.

**Step 3: Priya logs in**

She enters her email and password. Django's `login_page` view queries the database:
```python
student = Student.objects.get(email=email, password=password)
```
If the email and password match, Django stores `student.id` and `student.full_name` in the session and redirects her to the dashboard.

**Step 4: Priya sees her dashboard**

The dashboard page loads with the greeting "Good to see you, Priya Sharma." She sees four action cards:
1. **Your profile** — to view/edit her profile
2. **AI assessment** — marked as "START HERE"
3. **Learning roadmap** — to view her plan
4. **Assessment history** — to review past results

She clicks "AI assessment →".

**Step 5: Priya selects target roles**

The role selection page opens. She sees a list of popular roles:
AI Engineer, Backend Developer, Cloud Engineer, Cybersecurity Analyst, Data Analyst, Data Scientist, DevOps Engineer, Frontend Developer, Full Stack Developer, Machine Learning Engineer, Product Designer, QA Engineer, Software Engineer, UX Designer.

She clicks "+ Frontend Developer" and "+ Full Stack Developer" from the popular list. She also types "React Developer" in the search box and clicks "Add role".

She clicks "Suggest roles from my interests". JavaScript sends a POST request to `/assessment/recommend-roles/` with her interests and current roles. The AI responds with complementary suggestions. She adds "Backend Developer" from the suggestions.

She now has 4 target roles selected. She clicks "Confirm roles & start assessment →".

**Step 6: Django generates the aptitude test**

Django calls `generate_job_assessment(["Frontend Developer", "Full Stack Developer", "React Developer", "Backend Developer"])`. This function:
1. Sends a prompt to Ollama asking for 10 multiple-choice questions.
2. Receives a JSON response with questions, options, correct answers, and skill labels.
3. Validates the response (exactly 10 questions, 4 options each, valid answer).
4. Returns the validated quiz.

The test page loads showing 10 questions, each with a skill label (e.g., "Problem solving", "Web frameworks", "Database design").

**Step 7: Priya takes the assessment**

Priya reads each question and selects her answer. For example:
- Question 1 (Skill: "Problem solving"): She selects "Clarify success criteria and constraints"
- Question 2 (Skill: "Web frameworks"): She selects "Use component-based state management"
- ... and so on for all 10 questions.

She clicks "Submit assessment →".

**Step 8: Django evaluates her answers**

The `aptitude_test` view:
1. Retrieves the quiz from the session.
2. Iterates through each question, comparing Priya's selected answer to the correct answer.
3. Calculates her score (e.g., 7/10).
4. Builds a list of strengths (skills where she answered correctly) and gaps (skills where she answered incorrectly).

**Step 9: AI generates her career readiness summary**

Django calls `analyze_performance()`:
1. Collects her strengths and skill gaps from the answer analysis.
2. Builds a learning roadmap using `build_learning_roadmap()` — this is a curated roadmap based on her role track (web/backend, since she chose Frontend, Full Stack, React, Backend).
3. Sends a prompt to Ollama with her score, strengths, and gaps, asking for an evidence-based career readiness summary.
4. AI returns a summary like: "Priya demonstrates solid problem-solving and code quality skills. She should prioritise deepening her web framework knowledge..."

**Step 10: Results page is displayed**

The results page shows:
- **Score:** 7/10
- **AI Summary:** The career readiness analysis
- **Strengths:** Problem solving, Code quality, Debugging
- **Priority Gaps:** Web frameworks, Database design
- **Learning Roadmap:** A 4-stage learning plan with resources:
  1. HTML & CSS foundations (Weeks 1–4) — MDN Learn
  2. JavaScript essentials (Weeks 5–8) — javascript.info
  3. React fundamentals (Weeks 9–12) — React Learn
  4. Version control with Git (Weeks 13–16) — GitHub Skills

**Step 11: Priya views her full roadmap**

She clicks "Open full roadmap". The career recommendation page loads with:
- Her target roles at the top
- The full 4-stage learning roadmap
- Her assessment insights (strengths and gaps)
- The AI insight summary
- A "Explore matching roles →" button linking to LinkedIn job search

**Step 12: Priya downloads her PDF report**

She clicks "Download report ↓". Django's `download_pdf()` function:
1. Creates a PDF using ReportLab.
2. Includes her name, email, education, branch, skills, interests.
3. Includes her target roles and score.
4. Includes the AI recommendation text.
5. Returns the PDF as a downloadable file named `AI_Career_Report.pdf`.

---

## CHAPTER 7 — EXPLAIN IMPORTANT CODE CONCEPTS

### 7.1 Settings Configuration (`career_guidance/settings.py`)

**Purpose:** Controls all project settings — database, installed apps, security, templates, and static files.

**Key sections explained:**

```python
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
```
- `BASE_DIR` points to the project root folder.
- `load_dotenv()` reads the `.env` file and loads its variables into the environment.

```python
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY is not set in the .env file")
```
- Loads the secret key from the `.env` file.
- If the key is missing, the project raises an error immediately (instead of running insecurely).

```python
INSTALLED_APPS = [
    ...
    'accounts',
    'students',
    'careers',
    'assessment',
    'ai_engine',
    'reports',
    'adminpanel',
]
```
- Registers all custom apps with Django.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv("DB_NAME", "career_guidance"),
        'USER': os.getenv("DB_USER", "root"),
        'PASSWORD': os.getenv("DB_PASSWORD", ""),
        'HOST': os.getenv("DB_HOST", "localhost"),
        'PORT': os.getenv("DB_PORT", "3306"),
    }
}
```
- Configures MySQL as the database backend.
- All credentials come from environment variables with sensible defaults.

```python
TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        ...
    },
]
```
- Tells Django to look for templates in the `templates/` folder at the project root.

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```
- Configures static file serving from the `static/` folder.

### 7.2 Login View (`accounts/views.py`)

**Purpose:** Handles student login — verifies credentials and creates a session.

```python
def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            student = Student.objects.get(email=email, password=password)
            request.session["student_id"] = student.id
            request.session["student_name"] = student.full_name
            return redirect("/dashboard/")
        except Student.DoesNotExist:
            return render(request, "accounts/login.html", {"error": "Invalid Email or Password"})

    return render(request, "accounts/login.html")
```

**Line-by-line explanation:**
1. `if request.method == "POST"` — Only process when the form is submitted (not on initial page load).
2. `email = request.POST.get("email")` — Extract the email from the submitted form data.
3. `password = request.POST.get("password")` — Extract the password from the form.
4. `Student.objects.get(email=email, password=password)` — Query the database for a student matching both email and password. If no match, Django raises `Student.DoesNotExist`.
5. `request.session["student_id"] = student.id` — Store the student's ID in the browser session (this is how Django "remembers" who is logged in).
6. `return redirect("/dashboard/")` — Redirect to the dashboard.
7. `except Student.DoesNotExist` — If no student was found, re-render the login page with an error message.

**Note:** The password is stored and compared as plain text. In a production system, you should use Django's built-in `authenticate()` and `make_password()` functions to hash passwords.

### 7.3 Aptitude Test View (`assessment/views.py`)

**Purpose:** Generates the AI quiz on GET, then evaluates answers on POST.

```python
def aptitude_test(request):
    student = _student_or_login(request)
    if not student:
        return redirect("/login/")
    roles = _clean_roles(request.session.get("confirmed_target_roles", student.target_roles))
    if not roles:
        return redirect("choose_targets")

    if request.method == "GET":
        quiz = generate_job_assessment(roles)
        request.session["job_quiz"] = quiz
        request.session["confirmed_target_roles"] = roles
        return render(request, "assessment/test.html", {"roles": roles, "questions": quiz["questions"]})

    # POST — evaluate answers
    quiz = request.session.get("job_quiz")
    if not quiz:
        return redirect("choose_targets")

    answers, score = [], 0
    for index, question in enumerate(quiz.get("questions", [])):
        selected = request.POST.get(f"q{index}", "")
        correct = selected == question.get("answer")
        score += int(correct)
        answers.append({...})

    analysis = analyze_performance(student, roles, answers, score, len(answers))
    assessment = Assessment.objects.create(
        student=student, target_roles=roles, score=score,
        total_questions=len(answers), answers=answers,
        analysis=analysis, report=analysis["summary"]
    )
    request.session.pop("job_quiz", None)
    return render(request, "assessment/result.html", {...})
```

**How it works:**
1. **GET request:** Generates 10 AI questions, stores them in the session, and displays them.
2. **POST request:** Reads the submitted answers, scores them, calls `analyze_performance()` for AI analysis and roadmap building, saves the assessment to the database, and shows the results.

### 7.4 PDF Report Generation (`careers/pdf_report.py`)

**Purpose:** Generates a downloadable PDF with the student's profile and AI recommendation.

```python
from io import BytesIO
from django.http import FileResponse
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from xml.sax.saxutils import escape

def download_pdf(student, assessment, ai_response):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>AI Career Guidance Report</b>", styles["Title"]))
    story.append(Paragraph(f"<b>Student:</b> {student.full_name}", styles["BodyText"]))
    # ... more student details ...
    story.append(Paragraph(f"<b>Aptitude Score:</b> {assessment.score}/{assessment.total_questions}", styles["BodyText"]))
    story.append(Paragraph("<b>AI Recommendation</b>", styles["Heading2"]))
    story.append(Paragraph(escape(ai_response).replace("\n", "<br/>"), styles["BodyText"]))

    doc.build(story)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="AI_Career_Report.pdf")
```

**How it works:**
1. Creates an in-memory buffer (a temporary space in RAM).
2. Uses ReportLab's `SimpleDocTemplate` to build the PDF structure.
3. Adds paragraphs for student name, email, education, skills, interests, target roles, score, and the AI recommendation.
4. `escape(ai_response)` ensures any special HTML characters in the AI text are safely escaped.
5. `doc.build(story)` compiles everything into a PDF.
6. `FileResponse` sends the PDF to the browser as a downloadable file.

### 7.5 Learning Roadmap Builder (`ai_engine/roadmap.py`)

**Purpose:** Creates a structured learning plan with curated resource links, matched to the student's target role track.

The roadmap is not generated by AI — it uses a pre-built `RESOURCE_LIBRARY` dictionary with 7 tracks (web, backend, data, ml, design, security, general), each containing 4 lessons. The function:
1. Determines the track based on the student's roles.
2. Selects the appropriate 4 lessons.
3. Adds duration labels ("Weeks 1–4", "Weeks 5–8", etc.).
4. Includes instructions and project ideas.
5. Generates a LinkedIn job search URL for the student's roles.

---

## CHAPTER 8 — DATABASE AND DATA FLOW

### 8.1 Database Overview

The project uses **MySQL** as its primary database. Django's ORM (Object-Relational Mapper) translates Python code into SQL queries automatically.

**Tables in the database:**

| Table | Model | Purpose |
|---|---|---|
| `students_student` | Student | Stores all student registration and profile data |
| `careers_career` | Career | Stores predefined career listings |
| `assessment_assessment` | Assessment | Stores assessment results, scores, answers, AI analysis, and reports |

### 8.2 Data Flow: Registration to Report

```
User Input (Registration Form)
  ↓
StudentRegistrationForm (students/forms.py)
  ↓  validates data
Student.objects.create() → MySQL (students_student table)
  ↓
Login → session created (student_id stored in browser cookie)
  ↓
Dashboard → Student.objects.get(id=session["student_id"])
  ↓
Role Selection → student.target_roles updated, session["confirmed_target_roles"] set
  ↓
Aptitude Test → generate_job_assessment(roles) → Ollama API → Quiz stored in session
  ↓
Submit Answers → Score calculated locally → analyze_performance() → Ollama API → Roadmap built locally
  ↓
Assessment.objects.create() → MySQL (assessment_assessment table)
  ↓
Result Page ← reads from Assessment model
  ↓
Recommendation Page ← reads Assessment, Student data
  ↓
PDF Download ← reads Student + Assessment, generates PDF with ReportLab
```

### 8.3 What Is Stored vs. What Is Temporary

| Data | Where it lives | Lifetime |
|---|---|---|
| Student profile | MySQL database | Permanent (until deleted) |
| Career listings | MySQL database | Permanent |
| Assessment results | MySQL database | Permanent |
| AI quiz questions | Browser session (cookie) | Temporary — cleared after submission |
| Confirmed target roles | Browser session (cookie) | Temporary — re-set on each assessment |
| Login state | Browser session (cookie) | Temporary — cleared on logout |

### 8.4 How Data Moves Between Components

1. **Form → View:** User submits a form. Django extracts data from `request.POST`.
2. **View → Model:** View calls Django ORM methods (`Student.objects.get()`, `Assessment.objects.create()`) to read/write the database.
3. **View → AI Engine:** View calls functions in `ai_engine/` with relevant data.
4. **AI Engine → Ollama:** `ai_engine` functions send HTTP POST requests to `localhost:11434`.
5. **AI Engine → View:** AI functions return processed data (quiz, summary, roadmap).
6. **View → Template:** View passes data to templates via the `context` dictionary.
7. **Template → Browser:** Django renders the template with data and sends HTML to the browser.

---

## CHAPTER 9 — RUNNING THE PROJECT ON ANOTHER COMPUTER

### Step-by-Step Setup Guide

#### Step 1: Install Python

Visit https://www.python.org/downloads/ and install Python 3.10 or later.

Verify installation:
```bash
python --version
```

#### Step 2: Install Git (optional)

Download from https://git-scm.com/. Git is needed to clone the repository from GitHub.

#### Step 3: Clone or Download the Project

Using Git:
```bash
git clone https://github.com/bluestar24167-max/AI-Career-Guidance-System.git
cd AI-Career-Guidance-System
```

Or download the ZIP from GitHub and extract it.

#### Step 4: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

On Windows:
```bash
venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

#### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 6: Install and Configure MySQL

1. Install MySQL from https://dev.mysql.com/downloads/mysql/
2. Start the MySQL service.
3. Create a database:
```sql
CREATE DATABASE career_guidance;
```

#### Step 7: Configure Environment Variables

Create a file called `.env` in the project root with:
```
DJANGO_SECRET_KEY=your-random-secret-key-here
DB_NAME=career_guidance
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_HOST=localhost
DB_PORT=3306
```

To generate a secret key, you can use:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Important:** Never upload the `.env` file to GitHub.

#### Step 8: Run Migrations

```bash
python manage.py migrate
```

This creates the database tables.

#### Step 9: Install and Start Ollama

1. Install Ollama from https://ollama.com/
2. Pull the Llama 3.2 model:
```bash
ollama pull llama3.2:3b
```
3. Start the Ollama server (it usually starts automatically).

#### Step 10: Start the Django Development Server

```bash
python manage.py runserver
```

#### Step 11: Open in Browser

Go to http://127.0.0.1:8000/ in your web browser.

---

### Common Errors and Solutions

#### Error: "python is not recognized"

**Cause:** Python is not in your system's PATH.
**Solution:** Reinstall Python and check "Add Python to PATH" during installation. Or use `py` instead of `python` on Windows.

#### Error: "No module named django"

**Cause:** Django is not installed, or the virtual environment is not activated.
**Solution:**
1. Make sure the virtual environment is activated (you should see `(venv)` in your terminal).
2. Run `pip install -r requirements.txt`.

#### Error: "DJANGO_SECRET_KEY is not set"

**Cause:** The `.env` file is missing or not in the correct location.
**Solution:** Create the `.env` file in the project root with the required variables.

#### Error: "ModuleNotFoundError: No module named 'students'"

**Cause:** The app is not registered in `INSTALLED_APPS`, or the virtual environment is not activated.
**Solution:** Check that all apps are listed in `settings.py` and that you're in the virtual environment.

#### Error: "django.db.utils.OperationalError: (1049, 'Unknown database')"

**Cause:** The MySQL database has not been created.
**Solution:** Open MySQL and run `CREATE DATABASE career_guidance;`

#### Error: "Port 8000 is already in use"

**Cause:** Another process is using port 8000.
**Solution:** Use a different port:
```bash
python manage.py runserver 8080
```

#### Error: AI responses are empty or show fallback messages

**Cause:** Ollama is not running or the Llama 3.2 model is not installed.
**Solution:**
1. Make sure Ollama is running (`ollama serve` or check if it's running in the system tray).
2. Verify the model is available: `ollama list`
3. If not installed: `ollama pull llama3.2:3b`

#### Error: "Static files not loading" or broken styling

**Cause:** Static files are not configured correctly.
**Solution:** Verify that `STATICFILES_DIRS` in `settings.py` includes `BASE_DIR / "static"`.

#### Error: Migration issues

**Cause:** Database schema is out of sync with models.
**Solution:**
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## CHAPTER 10 — GIT AND GITHUB WORKFLOW

### 10.1 What is Git?

Git is a version control system. It tracks changes to files over time, allowing you to:
- Save "snapshots" (commits) of your project at any point.
- Revert to a previous version if something goes wrong.
- Work on different features simultaneously using branches.
- Collaborate with other developers.

### 10.2 What is GitHub?

GitHub is a website that hosts Git repositories online. It allows you to:
- Store your project in the cloud.
- Share your code with others.
- Collaborate using pull requests and issues.
- Track bugs and manage projects.

### 10.3 Git vs. GitHub

| Git | GitHub |
|---|---|
| A tool installed on your computer | A website/service |
| Tracks changes locally | Stores repositories online |
| Works without internet | Requires internet |
| Command-line tool | Web interface + CLI |

### 10.4 Key Git Concepts

| Concept | Explanation |
|---|---|
| **Repository (repo)** | A folder that Git is tracking. Contains all project files and their history. |
| **Commit** | A snapshot of changes at a specific point in time. Each commit has a message describing what changed. |
| **Branch** | A parallel version of the project. You can work on a new feature in a branch without affecting the main code. |
| **Remote** | The online version of your repository (on GitHub). |
| **Push** | Upload your local commits to the remote (GitHub). |
| **Pull** | Download changes from the remote to your local machine. |
| **Clone** | Download a complete copy of a remote repository to your computer. |
| **`.gitignore`** | A file that tells Git which files/folders to ignore (not track). |

### 10.5 The `.gitignore` File

Our `.gitignore` contains:
```
venv/
__pycache__/
*.pyc
db.sqlite3
.env
```

This ensures that:
- `venv/` (virtual environment) is not uploaded — it's large and can be recreated.
- `__pycache__/` and `*.pyc` (Python cache files) are not uploaded.
- `db.sqlite3` (local database) is not uploaded.
- `.env` (secret keys and credentials) is **never** uploaded — this is critical for security.

### 10.6 Basic Git Workflow

```
1. Make changes to your code files
2. Check what changed:        git status
3. Stage the changes:         git add filename.py
4. Commit with a message:     git commit -m "Description of changes"
5. Push to GitHub:            git push origin main
```

**Example session:**
```bash
# You edit accounts/views.py
git status                     # Shows "modified: accounts/views.py"
git add accounts/views.py      # Stages the file
git commit -m "Add profile edit functionality"
git push origin main           # Uploads to GitHub
```

### 10.7 Why Secret Keys Must Not Be Uploaded

If someone obtains your `DJANGO_SECRET_KEY`, they can:
- Forge session cookies (impersonate any user).
- Tamper with signed data.
- Potentially compromise the entire application.

This is why the `.env` file is in `.gitignore` and should **never** be committed to Git.

---

## CHAPTER 11 — PROJECT CHALLENGES AND LESSONS LEARNED

### Challenge 1: Managing Multiple Django Apps

**Problem:** The project has 7 custom apps. Organising code across multiple apps and ensuring they work together can be confusing.

**Cause:** Each app has its own models, views, URLs, and templates. Keeping track of which app handles which feature requires careful planning.

**Solution:** Clear app separation by responsibility:
- `accounts` handles authentication.
- `students` handles the student data model.
- `assessment` handles quizzes and evaluation.
- `ai_engine` handles AI calls (used as a library, not directly accessed by users).
- `careers` handles recommendations and PDF generation.

**Lesson:** Plan your app structure before coding. Each app should have a single, clear responsibility.

### Challenge 2: Connecting URLs and Views Across Apps

**Problem:** URLs are split between the root `urls.py` and app-level `urls.py` files. Forgetting to include an app's URLs or using wrong names causes broken links.

**Cause:** Django's two-level URL system requires each app to be properly included in the root configuration.

**Solution:** Using the `name` parameter in URL patterns allows templates to use `{% url 'name' %}` instead of hardcoding URLs, making refactoring easier.

**Lesson:** Always use named URLs and `{% url %}` template tags. Avoid hardcoding paths in templates.

### Challenge 3: Handling AI Responses

**Problem:** AI responses are unpredictable — they may be malformed JSON, missing fields, or completely empty.

**Cause:** Large language models do not always follow instructions precisely, especially regarding JSON formatting.

**Solution:** 
- Validate AI responses (check JSON structure, field presence, data types).
- Set a timeout on every API call (45–120 seconds).
- Provide fallback responses for every AI call.

**Lesson:** Never trust AI output directly. Always validate and handle failures gracefully.

### Challenge 4: Storing Quiz State Between Requests

**Problem:** The quiz is generated on GET and submitted on POST. How do you keep the questions between these two requests?

**Cause:** HTTP is stateless — each request is independent.

**Solution:** Store the quiz in the browser session (`request.session["job_quiz"]`). The session is tied to the user's browser cookie.

**Lesson:** Use Django sessions for temporary, per-user data that needs to persist across a few requests.

### Challenge 5: Environment Variable Configuration

**Problem:** The secret key and database credentials must be configured differently on each developer's machine.

**Cause:** Hardcoding credentials in `settings.py` is a security risk and makes the project non-portable.

**Solution:** Use `python-dotenv` to load variables from a `.env` file. The `.env` file is in `.gitignore` and is never uploaded to GitHub.

**Lesson:** Always use environment variables for secrets. Never commit credentials to version control.

### Challenge 6: Database Migrations

**Problem:** After modifying a model, the database schema becomes out of sync, causing errors.

**Cause:** Django tracks model changes through migration files. If you modify a model without running `makemigrations` and `migrate`, the database doesn't know about the changes.

**Solution:** Always run:
```bash
python manage.py makemigrations
python manage.py migrate
```
after modifying any model.

**Lesson:** Treat migrations as part of your code. Commit migration files to Git.

### Challenge 7: Frontend-Backend Integration with JavaScript

**Problem:** The role selection page uses JavaScript to dynamically add/remove roles and to call the AI suggestion endpoint. Integrating Django templates with JavaScript requires careful handling of template tags and CSRF tokens.

**Cause:** Django template tags (`{% url %}`, `{{ variable }}`) are rendered on the server side, while JavaScript runs in the browser.

**Solution:** 
- Embed Django template tags inside `<script>` blocks for URL resolution.
- Use `{{ student.interests|escapejs }}` to safely embed data in JavaScript.
- Include `{% csrf_token %}` and use `X-CSRFToken` header for AJAX requests.

**Lesson:** When mixing templates and JavaScript, be mindful of escaping and CSRF protection.

---

## CHAPTER 12 — FUTURE IMPROVEMENTS

### Current Features (What Exists Now)

- Student registration and login (session-based)
- Profile management
- AI-powered role suggestions
- Target role selection
- AI-generated aptitude questions (with fallback)
- Automatic assessment evaluation
- AI career readiness summary
- Curated learning roadmap with resource links
- PDF report download
- Assessment history
- Admin dashboard

### Suggested Future Enhancements

#### 1. Secure Authentication System
**What:** Replace the current plain-text password system with Django's built-in `auth` module, which provides password hashing, password reset, and session security.
**Why:** Plain-text passwords are a serious security vulnerability.

#### 2. Student Dashboard with Progress Tracking
**What:** Add charts and statistics to the dashboard showing assessment scores over time, skill improvement, and learning milestones.
**Why:** Visual progress tracking motivates students to continue learning.

#### 3. Saved Career History and Comparison
**What:** Allow students to take multiple assessments over time and compare their results. Show how their readiness has improved.
**Why:** Career guidance is not a one-time event — students need to see their growth.

#### 4. Advanced Recommendation Engine
**What:** Use machine learning models (not just LLM prompts) trained on career outcome data to provide more accurate recommendations.
**Why:** A trained model can identify patterns that a general-purpose LLM might miss.

#### 5. Admin Analytics Dashboard
**What:** Add visual analytics to the admin dashboard — charts showing popular careers, average scores, skill gap trends, and student demographics.
**Why:** Administrators need actionable insights, not just raw tables.

#### 6. Multilingual Support
**What:** Add internationalization (i18n) support to serve the application in multiple languages.
**Why:** Makes the system accessible to non-English-speaking students.

#### 7. Mobile Responsive / PWA Version
**What:** Optimise the application for mobile devices and make it installable as a Progressive Web App.
**Why:** Many students access the internet primarily through their phones.

#### 8. Cloud Deployment
**What:** Deploy the application to a cloud platform (e.g., AWS, Heroku, Railway) so it's accessible from anywhere.
**Why:** The current setup requires running locally on a development machine.

#### 9. Integration with Online Learning Platforms
**What:** Connect with platforms like Coursera, Udemy, or edX to provide direct course enrolment links.
**Why:** Students can immediately start learning without searching for resources.

#### 10. Resume Analysis
**What:** Allow students to upload their resume. AI analyses it and suggests improvements based on their target roles.
**Why:** A strong resume is critical for getting interviews.

---
---

# PART 2 — TECHNICAL WORKFLOWS

These workflows are clean, text-based diagrams suitable for conversion into visual flowcharts.

---

## Workflow 1 — Complete Application Flow

```
User → Registration/Login → Dashboard → Profile Completion → Role Selection
  → AI Role Suggestions → Confirm Roles → AI Aptitude Test Generation
  → Student Takes Test → Answer Evaluation → AI Career Analysis
  → Learning Roadmap Generation → Results Display → Career Recommendation Page
  → PDF Report Download
```

**Explanation of each stage:**

1. **User:** A new or returning student.
2. **Registration/Login:** Creates an account or authenticates via session-based login.
3. **Dashboard:** Central hub with links to profile, assessment, roadmap, and history.
4. **Profile Completion:** Student adds education, skills, and interests — this data feeds the AI engine.
5. **Role Selection:** Student chooses target roles from a curated list, search, or custom input.
6. **AI Role Suggestions:** Optional AI call suggests complementary roles based on the student's interests.
7. **Confirm Roles:** Student locks in their target roles.
8. **AI Aptitude Test Generation:** Ollama generates 10 role-specific MCQs.
9. **Student Takes Test:** Student selects answers for all questions.
10. **Answer Evaluation:** Django compares selected vs. correct answers, calculates score.
11. **AI Career Analysis:** Ollama generates an evidence-based readiness summary.
12. **Learning Roadmap Generation:** Curated roadmap built locally based on role track.
13. **Results Display:** Score, AI summary, strengths, gaps, and roadmap shown.
14. **Career Recommendation Page:** Full-page view with all insights and a LinkedIn job search link.
15. **PDF Report Download:** ReportLab generates a downloadable PDF report.

---

## Workflow 2 — Django Request Flow

```
Browser URL Request
  ↓
Django URL Resolver (urls.py)
  ↓  matches URL pattern
View Function (views.py)
  ↓  processes data
Database (MySQL via ORM) and/or AI Service (Ollama via HTTP)
  ↓  returns data
View prepares context dictionary
  ↓
Template Engine renders HTML
  ↓
HTTP Response sent to Browser
  ↓
Browser displays page
```

---

## Workflow 3 — AI Integration Flow

```
User Information (skills, interests, target roles)
  ↓
Django View collects data
  ↓
Prompt Construction (role-specific instructions + user data)
  ↓
HTTP POST to Ollama (localhost:11434/api/generate)
  ↓  model: llama3.2:3b
Ollama Processes Prompt → Generates Response
  ↓
Django receives JSON/text response
  ↓
Response Validation (JSON parsing, field checking, format verification)
  ↓  if invalid → Fallback response used
Validated Data → Application Display (template rendering)
  ↓
Student sees AI-generated content
```

---

## Workflow 4 — Assessment Flow

```
Target Role Selection (roles.html)
  ↓  POST
Roles saved to Student model and session
  ↓
Redirect to /assessment/test/
  ↓
generate_job_assessment(roles) → Ollama API
  ↓  returns 10 MCQs in JSON
Questions validated and stored in session
  ↓
Questions displayed in test.html
  ↓  Student answers all questions → POST
Answers compared to correct answers (local evaluation)
  ↓
Score calculated (e.g., 7/10)
  ↓
analyze_performance() → Ollama API → AI summary
  ↓
build_learning_roadmap() → curated resource-based roadmap
  ↓
Assessment saved to database (score, answers, analysis, report)
  ↓
Results displayed (result.html) → Score, AI summary, roadmap, strengths, gaps
```

---

## Workflow 5 — Git Development Workflow

```
Local Code Changes (edit files in IDE)
  ↓
git status → see which files changed
  ↓
git add filename.py → stage specific files
  ↓
git commit -m "Description of changes" → save snapshot locally
  ↓
git push origin main → upload to GitHub
  ↓
Team members pull changes: git pull origin main
```

---

# PART 3 — TEAM KNOWLEDGE ASSIGNMENTS

---

## Member 1 — Django Architecture and Project Structure

### Learn

1. **Django project vs. app:** Understand that `career_guidance` is the project and `accounts`, `students`, `assessment`, etc. are apps.
2. **Folder structure:** Know what each top-level folder and important file does.
3. **`settings.py`:** Understand how database, apps, templates, and static files are configured.
4. **`urls.py`:** Understand root URL configuration and how `include()` delegates to app-level URL files.
5. **Request-response cycle:** Trace the complete path from browser request to rendered page.
6. **Views and templates:** Understand how views pass data to templates and how templates render HTML.
7. **Sessions:** Understand how `request.session` stores login state and quiz data.

### Practical Work

**Task:** Create a new simple page (e.g., "About Us") that:
1. Has a URL route (`/about/`).
2. Has a view function in `accounts/views.py`.
3. Has an HTML template (`templates/home/about.html`) extending `base.html`.
4. Is linked from the home page.

### Deliverables

- A short explanation document (1–2 pages) describing the project's Django architecture.
- A simple workflow diagram showing the request-response cycle.
- A demonstration of the "About" page you implemented.

---

## Member 2 — AI Integration and Career Recommendation System

### Learn

1. **How Ollama works:** Understand that it runs locally, does not require API keys, and uses HTTP requests.
2. **How AI is connected with Django:** Study `ai_engine/ollama.py` — the single function that calls Ollama.
3. **Prompt engineering:** Study the three main prompts in `assessment_engine.py` and `job_recommendations.py`. Understand how they instruct the AI.
4. **Response validation:** Study how AI responses are parsed, validated, and how fallbacks work.
5. **Environment variables:** Understand how `.env` files work and why secrets must not be in Git.
6. **The roadmap builder:** Study `roadmap.py` — how it maps roles to learning tracks and resources.

### Practical Work

**Task:**
1. Trace the complete AI workflow from role selection to results page.
2. Modify one prompt in `assessment_engine.py` (e.g., change the wording slightly) and observe how it affects the AI output.
3. Test the fallback mechanism by temporarily stopping Ollama and verifying the application still works.

### Deliverables

- An AI workflow diagram (text-based) showing every AI call, its input, and its output.
- An explanation of how the three prompts differ in purpose and structure.
- A brief security best practices summary (API keys, environment variables, `.gitignore`).

---

## Member 3 — Assessment and Evaluation System

### Learn

1. **Role selection flow:** Study `assessment/views.py` — how `choose_targets` works, how roles are cleaned and saved.
2. **Question generation:** Study `generate_job_assessment()` in `ai_engine/assessment_engine.py` — how questions are generated, validated, and how fallbacks work.
3. **Test display:** Study `templates/assessment/test.html` — how questions are rendered with radio buttons.
4. **Answer submission:** Study the POST handling in `aptitude_test()` — how answers are extracted and scored.
5. **Evaluation logic:** Understand the `analyze_performance()` function — how strengths and gaps are derived from answer-level data.
6. **Assessment history:** Study `assessment_history` view and the history template.

### Practical Work

**Task:**
1. Document the complete assessment flow as a detailed flowchart (text-based).
2. Write 3 test cases (e.g., "student answers all questions correctly", "student answers none correctly", "no target roles selected").
3. If feasible, add one small improvement (e.g., a "time taken" feature, or a progress indicator showing "Question 3 of 10").

### Deliverables

- An assessment flowchart showing every step from role selection to result display.
- Three test cases with expected inputs and outputs.
- An explanation of the evaluation logic (how score, strengths, and gaps are calculated).

---

## Member 4 — Reports, UI, GitHub, and Deployment Preparation

### Learn

1. **Report generation:** Study `careers/pdf_report.py` — how ReportLab generates the PDF.
2. **Career recommendation page:** Study `careers/views.py` and `templates/careers/recommendation.html` — how the full roadmap is displayed.
3. **Templates and static files:** Understand template inheritance (`base.html`) and CSS configuration (`static/css/style.css`).
4. **Git and GitHub:** Understand commits, branches, pushes, pulls, and `.gitignore`.
5. **`requirements.txt`:** Understand how Python dependencies are managed.
6. **Running the project:** Study Chapter 9 and be able to set up the project on another machine.

### Practical Work

**Task:**
1. Improve one UI component (e.g., add a new section to the dashboard, improve the styling of the results page, or add a print-friendly version of the roadmap).
2. Prepare a beginner-friendly setup guide (as a `SETUP_GUIDE.md` file) that a new team member can follow to run the project on their machine.
3. Create a Git workflow diagram showing the typical development process.

### Deliverables

- One improved UI component (committed to Git).
- A `SETUP_GUIDE.md` file with step-by-step instructions.
- A Git/GitHub workflow diagram.

---

# PART 4 — FINAL TEAM LEARNING CHECKLIST

Every team member should be able to answer "Yes" to each item before the project presentation.

---

## General Project Knowledge

- [ ] I can explain the problem this project solves.
- [ ] I can describe the complete user workflow from registration to PDF download.
- [ ] I can name all 7 Django apps and their responsibilities.
- [ ] I can explain the difference between a Django project and a Django app.

## Folder Structure

- [ ] I know what `settings.py`, `urls.py`, `manage.py`, `wsgi.py`, and `asgi.py` do.
- [ ] I know where templates are stored and how they relate to views.
- [ ] I know where static files (CSS) are stored.
- [ ] I know which files contain AI logic and which contain view logic.

## URL Routing and Views

- [ ] I can explain how a URL like `/assessment/test/` is matched to the `aptitude_test` view.
- [ ] I can explain the difference between GET and POST requests.
- [ ] I can trace what happens when a student submits the assessment form.

## Templates and Static Files

- [ ] I understand template inheritance (`base.html` → child templates).
- [ ] I can explain how `{{ variable }}` and `{% for %}` work.
- [ ] I know how static files are loaded using `{% static %}`.

## Database and Data Flow

- [ ] I can name the 3 models and their key fields.
- [ ] I can explain how Django ORM translates Python to SQL.
- [ ] I can describe what data is stored permanently (database) vs. temporarily (session).
- [ ] I can run `makemigrations` and `migrate` after changing a model.

## AI Integration

- [ ] I know that the project uses Ollama with Llama 3.2 (local, no API keys).
- [ ] I can explain what happens when `generate_job_assessment()` is called.
- [ ] I can explain the three main AI prompts and their purposes.
- [ ] I can explain how fallback responses work when AI is unavailable.
- [ ] I can explain how the learning roadmap is built (curated resources, not AI-generated).

## Assessment Workflow

- [ ] I can trace the complete flow from role selection to result display.
- [ ] I can explain how answers are evaluated (local comparison, not AI).
- [ ] I can explain how `analyze_performance()` works.

## Report Generation

- [ ] I can explain how `download_pdf()` generates a PDF using ReportLab.
- [ ] I can describe what information is included in the PDF report.

## Environment Variables and Security

- [ ] I know what goes in the `.env` file.
- [ ] I understand why `.env` is in `.gitignore`.
- [ ] I can explain why passwords should be hashed (and that the current implementation uses plain text).

## Running the Project

- [ ] I can set up the project on a new computer from scratch.
- [ ] I can create a virtual environment and install dependencies.
- [ ] I can configure MySQL and run migrations.
- [ ] I can start Ollama and verify it's running.
- [ ] I can start the Django development server.

## Common Errors and Troubleshooting

- [ ] I can troubleshoot "Python not recognized."
- [ ] I can troubleshoot "Module not found" errors.
- [ ] I can troubleshoot database connection errors.
- [ ] I can troubleshoot Ollama connection failures.
- [ ] I can troubleshoot port conflicts.

## Git and GitHub Workflow

- [ ] I can explain the difference between Git and GitHub.
- [ ] I can use `git status`, `git add`, `git commit`, `git push`.
- [ ] I can explain what `.gitignore` does.
- [ ] I can explain why the `.env` file must not be committed.

## Current Project Features

- [ ] I can list all major features of the application.
- [ ] I can demonstrate the complete user journey live.

## Future Enhancement Ideas

- [ ] I can suggest at least 3 realistic future improvements.
- [ ] I can distinguish between current features and proposed future features.

---

# APPENDIX — KEY DEPENDENCIES

| Package | Version | Purpose |
|---|---|---|
| Django | 6.0.7 | Web framework |
| mysqlclient | 2.2.8 | MySQL database connector |
| requests | 2.34.2 | HTTP requests to Ollama |
| reportlab | 5.0.0 | PDF generation |
| python-dotenv | 1.0.1 | Environment variable loading |
| Pillow | 12.3.0 | Image processing |
| google-generativeai | 2.16.0 | Alternative AI provider (not actively used) |
| groq | 1.6.0 | Alternative AI provider (not actively used) |
| httpx | 0.28.1 | Async HTTP client |
| certifi | 2026.7.22 | SSL certificate verification |
| charset-normalizer | 3.4.9 | Character encoding normalization |
| idna | 3.18 | Internationalized domain names |
| pyasn1 | 0.6.4 | ASN.1 types |
| pyparsing | 3.0 | Parsing library |
| pydantic | 2.13.4 | Data validation |
| cffi | 2.1.0 | C FFI |
| cryptography | 50.0.0 | Cryptographic operations |
| typing-extensions | 4.16.0 | Backported typing features |
| h11 | 0.16.0 | HTTP/1.1 protocol |
| anyio | 4.14.2 | Async I/O |
| sniffio | 1.3.1 | Async library detection |
| asgiref | 3.12.1 | ASGI utilities |
| tzdata | 2026.3 | Timezone data |
| urlib3 | 2.7.0 | URL handling |
| websockets | 16.1.1 | WebSocket support |
| setuptools | 81.1.0 | Package building |
| sqlparse | 0.5.5 | SQL parsing |

---

# APPENDIX — COMPLETE URL MAP

| URL Path | View Function | App | Name |
|---|---|---|---|
| `/` | `accounts.views.home` | accounts | `home` |
| `/login/` | `accounts.views.login_page` | accounts | `login` |
| `/register/` | `accounts.views.register_page` | accounts | `register` |
| `/logout/` | `accounts.views.logout_page` | accounts | `logout` |
| `/dashboard/` | `accounts.views.dashboard` | accounts | `dashboard` |
| `/profile/` | `accounts.views.profile` | accounts | `profile` |
| `/edit-profile/` | `accounts.views.edit_profile` | accounts | `edit_profile` |
| `/assessment/` | `assessment.views.choose_targets` | assessment | `choose_targets` |
| `/assessment/recommend-roles/` | `assessment.views.role_recommendations` | assessment | `role_recommendations` |
| `/assessment/test/` | `assessment.views.aptitude_test` | assessment | `assessment_test` |
| `/assessment/history/` | `assessment.views.assessment_history` | assessment | `assessment_history` |
| `/careers/` | `careers.views.career_list` | careers | `career_list` |
| `/careers/<int:career_id>/` | `careers.views.career_detail` | careers | `career_detail` |
| `/careers/recommend/` | `careers.views.recommend_career` | careers | `recommend_career` |
| `/careers/download-report/` | `careers.views.download_report` | careers | `download_report` |
| `/admin/` | Django admin site | Django | — |
| `/admin-dashboard/` | `adminpanel.views.admin_dashboard` | adminpanel | `admin_dashboard` |

---

**End of Documentation**

*This document was prepared based on the actual source code of the AI-Powered Career Guidance System project. All code examples, model definitions, URL patterns, and workflow descriptions reflect the real implementation. Any features not present in the codebase are clearly marked as future enhancements.*
