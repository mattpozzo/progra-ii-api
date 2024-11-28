from requests import get, post, patch, delete
import pprint


from preconfig_user_tests import pregonfig  

def pregonfig():
    return {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3MzI4MjIxNDZ9.SxTvN2AIdr_QeNfQnTq7ig73IQGJYFDv_xSBgq4PY7M"
    }



headersJson = pregonfig()

# Test POST: Crear una nueva receta
print('Test POST: Crear una nueva receta')
response_post = post('http://127.0.0.1:5000/recipes/',
                     headers=headersJson,
                     json={
                         "title": "Milanesa",
                         "description": "Milanesa y papas fritas",
                         "body": "Instrucciones detalladas",
                         "created_by": 1,
                         "ingredients": [
                             {"ingredient_id": 1, "quantity": "200g"},
                             {"ingredient_id": 2, "quantity": "50g"}
                         ]
                     })
pprint.pprint(response_post.json(), sort_dicts=False)

# Test GET: Obtener todas las recetas
print('Test GET: Obtener todas las recetas')
response_get = get('http://127.0.0.1:5000/recipes/', headers=headersJson)
pprint.pprint(response_get.json(), sort_dicts=False)

# Test GET: Obtener una receta por ID
print('Test GET: Obtener receta con ID 2')
response_get = get('http://127.0.0.1:5000/recipes/1', headers=headersJson)
pprint.pprint(response_get.json(), sort_dicts=False)

# Test PATCH: Modificar una receta con ID1
print('Test PATCH: Modificar receta con ID 1')
response_patch = patch('http://127.0.0.1:5000/recipes/1',
                       headers=headersJson,
                       json={
                           "title": "Milanesa Napolitana",
                           "description": "Milanesa con jamón y queso",
                           "body": "Instrucciones nuevas",
                           "ingredients": [{"id": 1, "quantity": "250g"}]
                       })
pprint.pprint(response_patch.json(), sort_dicts=False)

# Test POST: Agregar un ingrediente a una receta
print('Test POST: Agregar ingrediente a receta con ID 1')
response_add_ingredient = post('http://127.0.0.1:5000/recipes/1/ingredients',
                                headers=headersJson,
                                json={
                                    "ingredient_id": 3,
                                    "quantity": "100g"
                                })
pprint.pprint(response_add_ingredient.json(), sort_dicts=False)

# Test DELETE: Eliminar una receta con ID 5
print('Test DELETE: Eliminar receta con ID 2')
response_delete = delete('http://127.0.0.1:5000/recipes/2', headers=headersJson)
pprint.pprint(response_delete.json(), sort_dicts=False)

