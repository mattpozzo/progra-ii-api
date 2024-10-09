from flask_restx import Api
from apis.login import api as log

api = Api(title='My Title', version='1.0', description='A description')

api.add_namespace(log)
