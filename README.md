# AI-Powered Career Guidance System

An AI-powered web application that provides personalized career guidance based on a student's educational background, skills, interests, and career preferences.

## 📌 About the Project

Choosing the right career can be difficult because of the rapid growth of technology and the large number of career opportunities available today. Students often struggle to identify careers that match their abilities, interests, and future goals.

The **AI-Powered Career Guidance System** addresses this problem by using Artificial Intelligence to analyze student profiles and provide personalized career recommendations.

The system can recommend career categories and job roles, generate role-specific aptitude tests, evaluate performance, and produce a detailed career report with recommendations and a learning roadmap.

## ✨ Key Features

* 👤 Student registration and login
* 📝 Student profile management
* 🎓 Educational background and specialization collection
* 💡 AI-powered career category recommendations
* 💼 AI-generated job role recommendations
* 🧠 Role-specific AI-generated aptitude tests
* 📊 Aptitude test evaluation
* 📄 Personalized career reports
* 💪 Strength and improvement analysis
* 📚 Recommended certifications and learning resources
* 🛠️ Project ideas for skill development
* 💰 Career salary insights
* 🗺️ Step-by-step career learning roadmap
* 📜 Assessment history
* 👨‍💼 Admin dashboard

## 🤖 Artificial Intelligence

The AI component uses **Ollama** with the **Llama 3.2 Large Language Model (LLM)**.

AI is used for:

* Career category generation
* Job role recommendations
* Aptitude question generation
* Career suitability analysis
* Personalized career recommendations
* Learning roadmap generation
* Career report generation

## 🛠️ Technology Stack

### Backend

* Python
* Django

### Frontend

* HTML
* CSS
* Bootstrap
* JavaScript

### Database

* MySQL

### AI

* Ollama
* Llama 3.2 LLM

### Version Control

* Git
* GitHub

## 📂 Project Structure

```text
AI_Career_Guidance/
│
├── accounts/             # User authentication
├── adminpanel/           # Admin functionality
├── ai_engine/            # AI and Ollama integration
├── assessment/           # Aptitude tests and assessments
├── career_guidance/      # Main Django project configuration
├── careers/              # Career recommendations and reports
├── reports/              # Report-related functionality
├── students/             # Student profiles
│
├── templates/            # HTML templates
├── static/               # CSS and static files
│
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .gitignore             # Files excluded from Git
└── README.md              # Project documentation
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/bluestar24167-max/AI-Career-Guidance-System.git
cd AI-Career-Guidance-System
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

Add the required configuration:

```text
DJANGO_SECRET_KEY=your-secret-key
DB_NAME=career_guidance
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_HOST=localhost
DB_PORT=3306
```

**Do not upload the `.env` file to GitHub.**

### 5. Configure MySQL

Create a MySQL database named:

```text
career_guidance
```

Make sure the database credentials in `.env` match your local MySQL configuration.

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Start Ollama

Install and configure Ollama separately, then make sure the required Llama model is available locally.

The AI functionality of this project depends on the Ollama service.

### 8. Run the Django server

```bash
python manage.py runserver
```

Then open the local development address shown by Django in your browser.

## 🔄 System Workflow

```text
Student
   ↓
Registration / Login
   ↓
Student Profile
   ↓
AI Career Category Recommendation
   ↓
Select Career Category
   ↓
AI Job Role Recommendation
   ↓
Select Job Role
   ↓
AI-Generated Aptitude Test
   ↓
Submit Assessment
   ↓
AI Analysis
   ↓
Personalized Career Report
   ↓
Learning Roadmap & Recommendations
```

## 🎯 Project Objectives

* Help students make informed career decisions.
* Provide personalized rather than generic career guidance.
* Identify suitable career paths based on individual profiles.
* Evaluate knowledge through role-specific aptitude tests.
* Provide actionable learning recommendations.
* Encourage continuous skill development.

## 🔮 Future Enhancements

Possible future improvements include:

* Resume analysis
* Internship recommendations
* Real-time job market trends
* Multilingual support
* Cloud deployment
* Integration with online learning platforms
* Job vacancy recommendations
* Advanced career analytics

## 👨‍💻 Project Type

**Academic / Educational Project**

Developed as an AI-powered career guidance web application using Python and Django.

## 📄 License

This project is intended primarily for educational and academic purposes.
