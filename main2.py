from flask import Flask
from apis import api
from apis.login import Login

app = Flask(__name__)
api.init_app(app)

api.add_resource(Login, '/login/<int:id>')

app.run(debug=True)

