from flask_restx import Namespace, Resource

api = Namespace('auth', description='Authentication, authorizaiion')

# cat = api.model('Cat', {
#     'id': fields.String(required=True, description='The cat identifier'),
#     'name': fields.String(required=True, description='The cat name'),
# })


@api.route("/login/<id>")
class Login(Resource):
    """Es un log in"""
    @api.doc("Log In")
    def post(self, id):
        return f"Hola id {id}"


@api.route("/logout<id>")
class Logout(Resource):
    """Es un log out"""
    @api.doc("Log Out")
    def post(self, id):
        return f"Chau id {id}"


# @api.route('/login')
# class CatList(Resource):
#     @api.doc('list_cats')
#     @api.marshal_list_with(cat)
#     def get(self):
#         '''List all cats'''
#         return CATS

# @api.route('/<id>')
# @api.param('id', 'The cat identifier')
# @api.response(404, 'Cat not found')
# class Cat(Resource):
#     @api.doc('get_cat')
#     @api.marshal_with(cat)
#     def get(self, id):
#         '''Fetch a cat given its identifier'''
#         for cat in CATS:
#             if cat['id'] == id:
#                 return cat
#         api.abort(404)
