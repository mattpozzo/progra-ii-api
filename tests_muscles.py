from preconfig_user_tests import pregonfig
from requests import put, get, delete, post

headersJson = pregonfig()

response_get = get('http://127.0.0.1:5000/muscles/', headers=headersJson)
print(response_get.json())
