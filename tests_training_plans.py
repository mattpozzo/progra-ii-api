from preconfig_user_tests import pregonfig
from requests import get, post
import pprint

headersJson = pregonfig()

response_get = get('http://127.0.0.1:5000/training_plan/', headers=headersJson)
pprint.pprint(response_get.json(), sort_dicts=False)

# creo rutina
response_post = post('http://127.0.0.1:5000/routine/create/',
                     headers=headersJson,
                     json={"name": "rutina1",
                           "description": "quiero hacer pecho y tener las tetas como The Rock"})

pprint.pprint(response_post.json(), sort_dicts=False)
routine = response_post.json()

routine_schedule = {"routine_id": routine['id'],
                    "weekday": 0,
                    "hour": '18:30'}


response_post = post('http://127.0.0.1:5000/training_plan/create/',
                     headers=headersJson,
                     json={"name": "TRP1",
                           'description': 'tr1 áááaáaa',
                           'routine_schedules': [routine_schedule]})

pprint.pprint(response_post.json(), sort_dicts=False)

response_get = get('http://127.0.0.1:5000/routine/',
                   headers=headersJson,
                   params={"training_plan_id": 1})
pprint.pprint(response_post.json(), sort_dicts=False)

response_post = post('http://127.0.0.1:5000/routine/create/',
                     headers=headersJson,
                     json={"name": "rutinaTestTemplate",
                           "description": "quiero hacer pecho y tener las tetas como The Rock"})

response_get = get('http://127.0.0.1:5000/routine/templates/',
                   headers=headersJson)

pprint.pprint(response_get.json(), sort_dicts=False)