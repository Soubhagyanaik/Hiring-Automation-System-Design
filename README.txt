AI Hiring Automation System

----------------------------------------
Project Overview:
----------------------------------------
This is an AI-powered Hiring Automation System built using Django.
It automates resume screening using Machine Learning and manages the complete hiring workflow.

----------------------------------------
Features:
----------------------------------------
- Secure Login Authentication
- Resume Upload (PDF)
- AI Resume Screening using TF-IDF & Cosine Similarity
- Automatic Shortlisting Based on AI Score
- Email Automation (Interview / Rejection)
- Interview Stage Tracking (Round 1, Round 2, HR, Selected)
- Recruiter Feedback & Rating System
- Analytics Dashboard (Charts + Statistics)
- Monthly Hiring Graph
- CSV Export of Candidates

----------------------------------------
Tech Stack:
----------------------------------------
Backend: Django
Database: SQLite
Machine Learning: Scikit-learn
PDF Processing: PyPDF2
Frontend: HTML, CSS, Chart.js

----------------------------------------
How To Run:
----------------------------------------
1. Create Virtual Environment
2. Install Requirements:
   pip install -r requirements.txt
3. Run Migrations:
   python manage.py migrate
4. Create Superuser:
   python manage.py createsuperuser
5. Run Server:
   python manage.py runserver

----------------------------------------
Developed By:
----------------------------------------
Soubhagya Naik