from preconfig_user_tests import pregonfig
from requests import get, post, patch, delete
import pprint

headersJson = pregonfig()
print('Test GET')
response_get = get('http://127.0.0.1:5000/routine/', headers=headersJson)
pprint.pprint(response_get.json(), sort_dicts=False)


print('Test POST')
response_post = post('http://127.0.0.1:5000/routine/create/',
                     headers=headersJson,
                     json={"name": "rutina1",
                           "description": "quiero hacer pecho y tener las tetas como The Rock"})

pprint.pprint(response_post.json(), sort_dicts=False)

response_post = post('http://127.0.0.1:5000/routine/create/',
                     headers=headersJson,
                     json={"name": "rutina2",
                           "description": "quiero hacer piernas y tenerlas como Messi"})

pprint.pprint(response_post.json(), sort_dicts=False)

print('Test GET 2')
response_get = get('http://127.0.0.1:5000/routine/', headers=headersJson)
pprint.pprint(response_get.json(), sort_dicts=False)

print('Test GET por ID')
response_get = get('http://127.0.0.1:5000/routine/1', headers=headersJson)
pprint.pprint(response_get.json(), sort_dicts=False)

print('Test PATCH por ID')
response_get = patch('http://127.0.0.1:5000/routine/1',
                     headers=headersJson,
                     json={"name": "rutinaGOD",
                           "description": "funciona joya el patch"})
pprint.pprint(response_get.json(), sort_dicts=False)

print('Test GET por ID')
response_get = get('http://127.0.0.1:5000/routine/1', headers=headersJson)
pprint.pprint(response_get.json(), sort_dicts=False)

print('Test DELETE por ID')
response_get = delete('http://127.0.0.1:5000/routine/2', headers=headersJson)
pprint.pprint(response_get.json(), sort_dicts=False)

print('Test GET por ID')
response_get = get('http://127.0.0.1:5000/routine/2', headers=headersJson)
pprint.pprint(response_get.json(), sort_dicts=False)

print('Test GET')
response_get = get('http://127.0.0.1:5000/routine/', headers=headersJson)
pprint.pprint(response_get.json(), sort_dicts=False)


