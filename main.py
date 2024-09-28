from flask import Flask, request
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

task_parser = reqparse.RequestParser()
task_parser.add_argument("task_id", type=int,
                         help="ID number for task", 
                         required=True)  # No sabemos como usarlo
todo = dict()


class ToDoList(Resource):
    def get(self, task_id: str):
        return {task_id: todo[task_id]}

    def put(self, task_id: int):
        args = task_parser.parse_args()
        task_id = args["task_id"]
        todo[task_id] = request.form[task_id]
        return {task_id: todo[task_id]}


api.add_resource(ToDoList, "/<string:task_id>")


if __name__ == "__main__":
    app.run()
