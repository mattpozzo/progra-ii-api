from flask import Flask, request
from flask_restful import Api, Resource
import sqlite3

app = Flask(__name__)
api = Api(app)

todo = dict()

connect = sqlite3.connect('database.db')
connect.execute("CREATE TABLE IF NOT EXISTS TODOLIST (id INT NOT NULL PRIMARY \
                KEY, name TEXT, realizado BOOLEAN)")


class ToDoList(Resource):
    def get(self, task_id: str):
        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            cursor.execute("SELECT * FROM TODOLIST WHERE id = ?", (task_id))
            response = cursor.fetchall()

        return response

    def put(self, task_id: int):
        data = request.form
        id = task_id
        name = data["name"]
        real = data["realizado"] == "True"

        response = {"id": id,
                    "name": name,
                    "realizado": real}

        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            try:
                cursor.execute("INSERT INTO TODOLIST (id,name,realizado) \
                               VALUES (?,?,?)", (id, name, real))
            except sqlite3.IntegrityError:
                cursor.execute("UPDATE TODOLIST SET name = ?, realizado = ? \
                               WHERE id = ?", (name, real, id))
            finally:
                users.commit()

        return response

    def delete(self, task_id: int):
        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            cursor.execute("DELETE FROM TODOLIST WHERE id = ?", (task_id))
            users.commit()
        return {"message": "Todo ok"}


api.add_resource(ToDoList, "/task<task_id>")


if __name__ == "__main__":
    app.run(debug=True)
