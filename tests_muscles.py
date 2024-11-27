from preconfig_user_tests import pregonfig
from requests import get
import pprint

headersJson = pregonfig()

response_get = get('http://127.0.0.1:5000/muscles/', headers=headersJson)
pprint.pprint(response_get.json(), sort_dicts=False)
