#making the necessary importation
from fastapi import FastAPI,status 
from sqlalchemy import create_engine,Column,Integer,String,func,DateTime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from datetime import datetime




#create ToDoRequest Base Model 

class ToDoRequest(BaseModel):
    task:str
    another_task:str
    createdAt:datetime

# Create a sqlite engine instance
engine = create_engine("sqlite:///todooo.db")

# Create a DeclarativeMeta instance
Base = declarative_base()

#I want to create the various field for the database 
class Todo(Base):
    __tablename__="todos"
    id= Column(Integer,primary_key=True)
    task=Column(String(256))
    createdAt=Column(DateTime(timezone=True),default=func.now())
    another_task=Column(String(256))


# Create the database
Base.metadata.create_all(engine)
# Create the database




#i want initialize the fast api 
app = FastAPI()

@app.get("/")
def root():
    #I will be adding my template file over , over here will take my index.html 
    return "todooo"

@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(todo: ToDoRequest):
    try:
        # create a new database session
        session = Session(bind=engine, expire_on_commit=False)

        # create an instance of the ToDo database model
        tododb = Todo(task=todo.task, another_task=todo.another_task,createdAt=todo.createdAt)

        # add it to the session and commit it
        session.add(tododb)
        session.commit()

        # grab the id, createdAt, and another_task values from the database object
        id = tododb.id
        created_at = tododb.createdAt
        another_task = tododb.another_task

        # close the session
        session.close()

        # return the id, createdAt, and another_task values in the response
        return {"id": id, "task": todo.task, "createdAt": created_at, "another_task": another_task}

    except Exception as e:
        # Handle exceptions and rollback the transaction if there's an error
        session.rollback()
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    finally:
        # Close the session
        session.close()





@app.get("/todo/{id}")
def read_todo(id: int):
    return "read todo item with id {id}"









@app.put("/todo/{id}")
def update_todo(id: int):
    return "update todo item with id {id}"







@app.delete("/todo/{id}")
def delete_todo(id: int):
    return "delete todo item with id {id}"





@app.get("/todo")
def read_todo_list():
    return "read todo list"
