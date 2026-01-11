import os
from dotenv import load_dotenv
load_dotenv()

import psycopg2
from psycopg2 import OperationalError

from models.request_models import User, Task, FetchTask, UpdateTask, ToggleSubtask

###########################################################################

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode" : "require"},
    pool_pre_ping = True)

SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

#############################################################################

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

class Database:

    db = None

    def connect(self):
        print("Connecting to database ...")
        try:
            self.db = psycopg2.connect(
                dbname = db_name,
                user = db_user,
                password = db_password,
                host = db_host,
                port = db_port
            )
            print("Connection successful!")
        except OperationalError as e:
            print(f"Error while connecting to db: {e}")


    def insertUser(self,user : User):
        print("Inserting user to database ...")
        try:
            cursor = self.db.cursor()
            query = "INSERT INTO users (name,email,password) VALUES (%s, %s, %s)"
            values = (user.user_name, user.email, user.password)
            cursor.execute(query, values)
            self.db.commit()
            print("Insertion successful")
            self.db.close()
        except OperationalError as e:
            print(f"Error while inserting user into db: {e}")

    async def insertTask(self,task : Task):
        print("Inserting task to database ...")
        try:
            cursor = self.db.cursor()
            query = "INSERT INTO tasks (user_id,description,task,date,priority) VALUES (%s, %s, %s, %s, %s)"
            values = (task.user_id,task.description, task.title, task.dueDate, task.priority)
            cursor.execute(query, values)
            self.db.commit()
            print("Insertion successful")
            self.db.close()
            return {"message" : "Task inserted into database", "status" : 200}
        except OperationalError as e:
            print(f"Error while inserting task into db: {e}")
            return {"error" : "Error while inserting into DB", "status" : 404}


    def searchUser(self,user : User):
        print("Searching user in database")
        try:
            cursor = self.db.cursor()
            query = "SELECT id FROM users WHERE email = %s AND password = %s"
            values = (user.email, user.password)
            result = cursor.execute(query, values)
            if result:
                print("Search successful")
                cursor.close()
                self.db.close()
                return result
            else:
                print("Search unsuccessful. No user found !")
                cursor.close()
                self.db.close()
                return -1
        except OperationalError as e:
            print(f"Error while searching user into db: {e}")


    def searchUserTasks(self,userID : int):
        print("Fetching all tasks for specific user")
        try:
            cursor = self.db.cursor()
            query = "SELECT * FROM tasks WHERE user_id = %s"
            values = (userID,)
            cursor.execute(query, values)
            result = cursor.fetchall()
            cursor.close()
            self.db.close()
            if result:
                print("Search successful")
                return result
        except OperationalError as e:
            print(f"Error while searching user into db: {e}")

    
    def deleteTask(self, task_id : int):
        print(f"Deleting task {task_id} from DB")
        try:
            cursor = self.db.cursor()
            query = "DELETE FROM tasks where id = %s"
            values = (task_id,)
            cursor.execute(query,values)
            self.db.commit()
            cursor.close()
            self.db.close()
            return {"message" : "Task deleted successfully"}
        except OperationalError as e:
            print(f"Error while deleting task from db: {e}")

    def searchTask(self,taskID : int):
        print("Fetching all tasks for specific user")
        try:
            cursor = self.db.cursor()
            query = "SELECT * FROM tasks WHERE id = %s"
            values = (taskID,)
            cursor.execute(query, values)
            result = cursor.fetchall()
            cursor.close()
            self.db.close()
            if result:
                print("Search successful")
                return result
        except OperationalError as e:
            print(f"Error while searching task from db: {e}")

    def updateTask(self,task : UpdateTask):
        print("Updating task to database ...")
        try:
            cursor = self.db.cursor()
            query = """
            UPDATE tasks
            SET
                task = COALESCE(%s, task),
                description = COALESCE(%s, description),
                date = COALESCE(%s, date),
                priority = COALESCE(%s, priority)
            WHERE id = %s
            """

            values = (
                task.title,
                task.description,
                task.dueDate,
                task.priority,
                task.task_id
            )

            cursor.execute(query,values)
            self.db.commit()
            print("Update successful")
            self.db.close()
            return {"message" : "Task updated into database", "status" : 200}
        except OperationalError as e:
            print(f"Error while inserting task into db: {e}")
            return {"error" : "Error while updating into DB", "status" : 404}
        

    def toggleTask(self,task : UpdateTask):
        print("Toggling task status ...")
        try:
            cursor = self.db.cursor()
            query = """
            UPDATE tasks
            SET done = NOT done
            WHERE id = %s
            """

            values = (task.task_id,)

            cursor.execute(query,values)
            self.db.commit()
            print("Toggle successful")
            self.db.close()
            return {"message" : "Task status toggled", "status" : 200}
        except OperationalError as e:
            print(f"Error while toggling task into db: {e}")
            return {"error" : "Error while toggling into DB", "status" : 404}
        
    def toggleSubtask(self,task : ToggleSubtask):
        print("Toggling task status ...")
        try:
            cursor = self.db.cursor()
            query = """
            UPDATE subtasks
            SET completed = NOT completed
            WHERE id = %s
            """

            values = (task.id,)

            cursor.execute(query,values)
            self.db.commit()
            print("Toggle successful")
            self.db.close()
            return {"message" : "SubTask status toggled", "status" : 200}
        except OperationalError as e:
            print(f"Error while toggling subtask into db: {e}")
            return {"error" : "Error while toggling subtask into DB", "status" : 404}
        

    def deleteSubtask(self, task_id : int):
        print(f"Deleting task {task_id} from DB")
        try:
            cursor = self.db.cursor()
            query = "DELETE FROM subtasks where id = %s"
            values = (task_id,)
            cursor.execute(query,values)
            self.db.commit()
            cursor.close()
            self.db.close()
            return {"message" : "Subtask deleted successfully"}
        except OperationalError as e:
            print(f"Error while deleting task from db: {e}")




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    





    
