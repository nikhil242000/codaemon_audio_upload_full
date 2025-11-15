# AI Developer Technical Test – Django Full-Stack Application

## Project Overview
This project is a full-stack Django application designed as part of the AI Developer technical test for Codaemon Softwares.  
The application allows:  
- Fetching user details via a REST API endpoint  
- Uploading audio files for a user  
- Playing and updating audio files  

The project uses Django as the backend framework and includes both API endpoints and a simple frontend interface for demonstration.

---

## Features
1. **User Details API** – Retrieve user information via REST API.  
2. **Audio Upload** – Upload audio files associated with a user.  
3. **Audio Playback** – Play uploaded audio directly from the frontend.  
4. **Audio Update** – Replace or update an existing audio file.  

---

## Technologies Used
- **Backend:** Django 5.x, Django REST Framework  
- **Database:** SQLite (default; can be replaced with PostgreSQL/MySQL)  
- **Frontend:** HTML, CSS, JavaScript (basic UI for demo)  
- **Other:** Python 3.11+, Git, GitHub  

---

## Installation & Setup

1. **Clone the repository:**
```bash
git clone https://github.com/nikhil242000/codaemon_audio_upload_full.git
cd codaemon_audio_upload_full

2. Create and activate a virtual environment:
   # Windows:
   python -m venv venv
   venv\Scripts\activate
   # Mac/Linux:
   python -m venv venv
   source venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

4. Apply database migrations:
   python manage.py migrate

5. Run the development server:
   python manage.py runserver

6. Access the application:
   - Frontend demo: http://127.0.0.1:8000/
   - REST API endpoints: http://127.0.0.1:8000/api/users/
