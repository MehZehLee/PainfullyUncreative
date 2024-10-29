from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import Session, sessionmaker
from pydantic import BaseModel
from data_model import Task, Base
from typing import Optional
from datetime import datetime

app = FastAPI()

# Set up local database connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create the tables
Base.metadata.create_all(bind=engine)

# Create a session to use the ORM
Session = sessionmaker(bind=engine)
session = Session()

# Pydantic model for creating a task
class TaskCreate(BaseModel):
    user_id: int
    title: str
    description: Optional[str] = None
    status: str = "Open"
    due_date: Optional[datetime] = None

# Pydantic model for updating a task
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None

# Create task
# /createtask
@app.post("/createtask")
async def create_task(task: TaskCreate):
    try: 
        new_task = Task(
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            status=task.status,
            due_date=task.due_date
        )
        session.add(new_task)
        session.commit()
        return {"message": "Task created successfully", "task_id": new_task.task_id}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Update task
# /updatetask/{task_id}
@app.patch("/updatetask/{task_id}")
async def update_task(task: TaskUpdate, task_id: int):
    try:
        task_to_update = session.query(Task).filter(Task.task_id == task_id).first()
        if not task_to_update:
            raise HTTPException(status_code=404, detail="Task not found")
        
        if task.title is not None:
            task_to_update.title = task.title
        if task.description is not None:
            task_to_update.description = task.description
        if task.status is not None:
            task_to_update.status = task.status
        if task.due_date is not None:
            task_to_update.due_date = task.due_date
        
        session.commit()
        return {"message": "Task updated successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Delete task
# /deletetask/{task_id}
@app.delete("/deletetask/{task_id}")
async def delete_task(task_id: int):
    try:
        task = session.query(Task).filter(Task.task_id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        session.delete(task)
        session.commit()
        return {"message": "Task deleted successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Get all tasks
# /gettasks
@app.get("/gettasks")
async def get_all_tasks():
    try:
        tasks = session.query(Task).all()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# Get tasks for a user
# /gettasks/{user_id}
@app.get("/gettasks/{user_id}")
async def get_tasks(user_id: int):
    tasks = session.query(Task).filter(Task.user_id == user_id).all()
    return tasks