from preconfig_user_tests import pregonfig
from requests import get, post, patch
import pprint


headersJson = pregonfig()

# Armo rutina de Pecho y Triceps, 1 y 1
# Los IDs son 4 y 2 respectivamente

response_get = get('http://127.0.0.1:5000/exercises/',
                   headers=headersJson,
                   params={'muscle': 4})

ejercicio_pecho = response_get.json()[0]

pprint.pprint(ejercicio_pecho)

response_get = get('http://127.0.0.1:5000/exercises/',
                   headers=headersJson,
                   params={'muscle': 2})

ejercicio_tricep_og = response_get.json()[0]

pprint.pprint(ejercicio_tricep_og)

#Armo los routine exercises

ejercicio_pecho = {"exercise_id": ejercicio_pecho["id"],
                   'sets': 3,
                   'reps': 12,
                   'weight': 20,
                   'notes': "Hacer hasta fallo!"}

ejercicio_tricep = {"exercise_id": ejercicio_tricep_og["id"],
                    'sets': 3,
                    'reps': 12,
                    'weight': 10}


response_post = post('http://127.0.0.1:5000/routine/create/',
                     headers=headersJson,
                     json={"name": "rutina1",
                           "description": "quiero hacer pecho y tener las tetas como The Rock",
                           "routine_exercises": [ejercicio_pecho, ejercicio_tricep]})

pprint.pprint(response_post.json(), sort_dicts=False)

response_get = get('http://127.0.0.1:5000/routine/1/exercises/',
                   headers=headersJson)


pprint.pprint(response_get.json())


ejercicio_tricep = {"exercise_id": ejercicio_tricep_og["id"],
                    'sets': 4,
                    'reps': 8,
                    'weight': 12}

response_post = patch('http://127.0.0.1:5000/routine/1/',
                      headers=headersJson,
                      json={"name": "rutina1GOD",
                            "routine_exercises": [ejercicio_tricep]})

pprint.pprint(response_post.json(), sort_dicts=False)

response_get = get('http://127.0.0.1:5000/routine/1/exercises/',
                   headers=headersJson)


pprint.pprint(response_get.json())