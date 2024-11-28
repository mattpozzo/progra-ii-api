from preconfig_user_tests import pregonfig
from requests import get
import pprint

headersJson = pregonfig()

response_get = get('http://127.0.0.1:5000/exercises/', headers=headersJson)
pprint.pprint(response_get.json(), sort_dicts=False)

response_get = get('http://127.0.0.1:5000/exercises/',
                   headers=headersJson,
                   params={'muscle': 1})
pprint.pprint(response_get.json(), sort_dicts=False)

response_get = get('http://127.0.0.1:5000/exercises/',
                   headers=headersJson,
                   params={'muscle': 9})
pprint.pprint(response_get.json(), sort_dicts=False)
