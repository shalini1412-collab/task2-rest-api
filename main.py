from typing import Literal
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field


load_dotenv()


app = FastAPI(
    title=os.getenv("APP_NAME", "Developer Productivity API"),
    description="REST API for managing users, projects, and tasks.",
    version=os.getenv("APP_VERSION", "1.0.0"),
)


# -------------------------
# Data Models
# -------------------------

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: str = Field(min_length=5, max_length=100)


class User(UserCreate):
    id: int


class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=5, max_length=500)
    owner_id: int


class Project(ProjectCreate):
    id: int


class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=5, max_length=500)
    project_id: int
    status: Literal["todo", "in-progress", "done"] = "todo"


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, min_length=5, max_length=500)
    status: Literal["todo", "in-progress", "done"] | None = None


class Task(TaskCreate):
    id: int


# -------------------------
# Temporary In-Memory Data
# -------------------------

users: list[User] = []
next_user_id = 1

projects: list[Project] = []
next_project_id = 1

tasks: list[Task] = []
next_task_id = 1


# -------------------------
# Basic Endpoints
# -------------------------

@app.get("/")
def root():
    return {
        "message": "Developer Productivity API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# -------------------------
# User Management
# -------------------------

@app.post(
    "/users",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
)
def create_user(user_data: UserCreate):
    global next_user_id

    for user in users:
        if user.email.lower() == user_data.email.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    new_user = User(
        id=next_user_id,
        name=user_data.name,
        email=user_data.email,
    )

    users.append(new_user)
    next_user_id += 1

    return new_user


@app.get(
    "/users",
    response_model=list[User],
    tags=["Users"],
)
def get_users():
    return users


# -------------------------
# Project Management
# -------------------------

@app.post(
    "/projects",
    response_model=Project,
    status_code=status.HTTP_201_CREATED,
    tags=["Projects"],
)
def create_project(project_data: ProjectCreate):
    global next_project_id

    owner_exists = any(
        user.id == project_data.owner_id
        for user in users
    )

    if not owner_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Owner user not found",
        )

    new_project = Project(
        id=next_project_id,
        name=project_data.name,
        description=project_data.description,
        owner_id=project_data.owner_id,
    )

    projects.append(new_project)
    next_project_id += 1

    return new_project


@app.get(
    "/projects",
    response_model=list[Project],
    tags=["Projects"],
)
def get_projects():
    return projects


# -------------------------
# Task Management
# -------------------------

@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
)
def create_task(task_data: TaskCreate):
    global next_task_id

    project_exists = any(
        project.id == task_data.project_id
        for project in projects
    )

    if not project_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    new_task = Task(
        id=next_task_id,
        title=task_data.title,
        description=task_data.description,
        project_id=task_data.project_id,
        status=task_data.status,
    )

    tasks.append(new_task)
    next_task_id += 1

    return new_task


@app.get(
    "/tasks",
    response_model=list[Task],
    tags=["Tasks"],
)
def get_tasks():
    return tasks


@app.get(
    "/tasks/{task_id}",
    response_model=Task,
    tags=["Tasks"],
)
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found",
    )


@app.put(
    "/tasks/{task_id}",
    response_model=Task,
    tags=["Tasks"],
)
def update_task(task_id: int, task_data: TaskUpdate):
    for task in tasks:
        if task.id == task_id:

            if task_data.title is not None:
                task.title = task_data.title

            if task_data.description is not None:
                task.description = task_data.description

            if task_data.status is not None:
                task.status = task_data.status

            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found",
    )


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tasks"],
)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found",
    )