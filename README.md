TodoFlow — To-Do List App using FastAPI
Introduction
TodoFlow is a modern, full-stack To-Do List application built using FastAPI.
The project was created as a practical learning project to understand how a real-world FastAPI application is structured, how a backend communicates with a database, how authentication works, and how frontend pages interact with backend APIs.
Users can create an account, securely log in, manage their tasks, set due times and reminders, and track completed tasks through a responsive dark-themed interface.
_________________________________________
Features
•	🔐 User registration and login
•	🔑 Password hashing using bcrypt
•	👤 User-specific task management
•	➕ Create new tasks
•	✏️ Edit existing tasks
•	🗑️ Delete tasks
•	✅ Mark tasks as completed or incomplete
•	📝 Add optional task descriptions
•	⏰ Set task due times
•	📱 Responsive design
•	🗄️ SQLite database
•	🧩 SQLAlchemy ORM
•	✔️ Pydantic data validation
•	🚀 FastAPI backend
•	🧪 Pytest-based testing structure
________________________________________
Tech Stack
Backend
•	Python
•	FastAPI
•	Uvicorn
•	SQLAlchemy
•	SQLite
•	Pydantic
Authentication & Security
•	Passlib
•	bcrypt
•	Cookie-based authentication
Frontend
•	HTML5
•	CSS3
•	JavaScript
•	Jinja2 Templates
Development & Tools
•	Git
•	GitHub
•	uv
•	Pytest
•	HTTPX
•	VS Code
________________________________________
Installation
1. Clone the repository
git clone https://github.com/Paranthaman654A/TodoFlow---fastapi.git
2. Navigate into the project
cd TodoFlow---fastapi
3. Create a virtual environment
If you are using uv:
uv venv
Activate the environment on Windows:
.venv\Scripts\activate
4. Install dependencies
Using uv:
uv sync
Or using the generated requirements.txt:
pip install -r requirements.txt
________________________________________
How to Run
Start the FastAPI server
Using uv:
uv run uvicorn app.main:app --reload
Or, after activating the virtual environment:
uvicorn app.main:app --reload
The application will start locally at:
http://127.0.0.1:8000
Open the URL in your browser.
________________________________________
API Documentation
FastAPI automatically provides interactive API documentation.
Swagger UI
http://127.0.0.1:8000/docs
ReDoc
http://127.0.0.1:8000/redoc
These interfaces can be used to explore and test the application's API endpoints.
________________________________________
Learning Objectives
This project was developed to gain practical experience with:
•	Understanding REST API concepts
•	Building applications with FastAPI
•	Creating FastAPI routers
•	Understanding dependency injection
•	Working with SQLAlchemy ORM
•	Connecting FastAPI with SQLite
•	Designing database models
•	Using Pydantic schemas
•	Implementing CRUD operations
•	Understanding authentication workflows
•	Hashing passwords with bcrypt
•	Working with cookies
•	Using Jinja2 templates
•	Connecting frontend and backend
•	Handling HTML forms
•	Working with JavaScript and browser notifications
•	Structuring a real-world FastAPI project
•	Writing automated tests with Pytest
•	Managing Python dependencies with uv
•	Using Git and GitHub
•	Deploying a FastAPI application
________________________________________
Author
Paranthaman
AI/ML Enthusiast
This project was created as part of my journey to learn backend development and build practical software projects using Python and FastAPI.


🌐 Live Demo
🚀 TodoFlow is Live!
Try the application directly from your browser:
🔗 Launch TodoFlow → https://todoflow-fwiu.onrender.com/

