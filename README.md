# Developer Productivity REST API

A RESTful backend API for managing users, projects, and tasks, built using **FastAPI** and **Python**.

This project was developed as part of my **Full Stack Development Internship at Innovation Hacks**, focusing on backend development, REST API design, input validation, error handling, and API documentation.

---

## 🚀 Features

### User Management
- Create users
- Retrieve all users
- Email uniqueness validation
- Input validation using Pydantic

### Project Management
- Create projects
- Retrieve all projects
- Validate project ownership
- Handle invalid user references

### Task Management
- Create tasks
- Retrieve all tasks
- Retrieve a task by ID
- Update task details
- Update task status
- Delete tasks
- Validate project references

### Task Status

Tasks support three statuses:

- `todo`
- `in-progress`
- `done`

---

## 🛠️ Tech Stack

- **Python**
- **FastAPI**
- **Pydantic**
- **Uvicorn**
- **python-dotenv**
- **REST API**
- **Swagger / OpenAPI**

---

## 📁 Project Structure

```text
task2-api/
│
├── .gitignore
├── .env
├── main.py
├── README.md
└── .venv/
## Future Improvements
...

## Learning Outcomes
...

## Author
Shalini

## Internship
Innovation Hacks – Full Stack Development Internship

## License

This project is developed for educational and internship purposes as part of the Innovation Hacks Full Stack Development Internship.

© 2026 Shalini. All rights reserved.