from fastapi import APIRouter,HTTPException,status,Depends
from Backend.schemas import Task,createTask
from typing import List
from Backend.database.database import get_db
from Backend.database.models import  DBTask
from sqlalchemy.orm import Session
from sqlalchemy import select

router = APIRouter(prefix="/api/v1")

## routes
@router.get("/home")
def home():
    return{"message":"server works.."}

@router.get("/Tasks",response_model=List[Task])
def get_all_tasks(db:Session = Depends(get_db)):

    return db.scalars(select(DBTask)).all()

@router.get("/Task/{id}",response_model=Task)
def get_one_task(id:int,db:Session=Depends(get_db)):

    task = db.get(DBTask,id)

    if task is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Task not found")

    return task

@router.delete("/Task/{id}",status_code=status.HTTP_200_OK)
def delete_task(id:int,db:Session=Depends(get_db)):

    task = db.get(DBTask,id)

    if task is None:
        raise HTTPException(status_code = 404, detail = "Task not found")
    db.delete(task)
    db.commit()
    

@router.post("/Tasks",status_code=status.HTTP_200_OK)
def add_task(task:createTask,db:Session = Depends(get_db)):
    new_task = DBTask(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return task

@router.put("/Task/{id}",status_code=status.HTTP_201_CREATED,response_model=createTask)
def update_task(id:int,task:createTask,db:Session = Depends(get_db)):
    updated_task = db.get(DBTask,id)

    if updated_task is None:
        raise HTTPException(status_code = 404, detail = "Task not found")

    updated_task.name = task.name
    updated_task.description = task.description
    updated_task.is_completed = task.is_completed

    db.commit()
    db.refresh(updated_task)

    return updated_task