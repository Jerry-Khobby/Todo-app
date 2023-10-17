#making the necessary importation
from fastapi import FastAPI,status 
from sqlalchemy import create_engine,Column,Integer,String,func,DateTime
from sqlalchemy.ext.declarative import declarative_base




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


# Create the database
Base.metadata.create_all(engine)


#i want initialize the fast api 
app = FastAPI()

@app.get("/")
def root():
    #I will be adding my template file over , over here will take my index.html 
    return "todooo"


@app.post("/todo",status_code=status.HTTP_201_CREATED)
def create_todo():
    return "create todo item"

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
