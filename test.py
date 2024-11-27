from requests import put, get, delete, post

headersJson = {'Content-Type': 'application/json'}

#probando que el token es necesario
print('Probando que el token es necesario')
get_users_test1 = get('http://127.0.0.1:5000/users/')
print(get_users_test1.json())

registro = post('http://127.0.0.1:5000/users/register',
                headers=headersJson,
                json={"first_name": "Marcelo", 
                      "last_name": "Ulrich", 
                      "email": "mulrich@estudiantes.unsam.edu.ar", 
                      "password": "pass123", 
                      "certified": False})

print('\n\nProbando registro...')
if registro.status_code == 201:
    print('Registro exitoso')
else:
    print('ERROR en registro: '+registro.json()['message'])

print('\n\nPrueba error login')
login_failed = post('http://127.0.0.1:5000/users/login',headers=headersJson,json={"email": "laura.martinez@example.com", "password": "securepassword123"})
print(login_failed.json())

print('\n\nPrueba login exitoso')
login_success = post('http://127.0.0.1:5000/users/login',headers=headersJson,json={"email": "mulrich@estudiantes.unsam.edu.ar", "password": "pass123"})
print(login_success.json())
token = login_success.json()['token']

headersJson['Authorization'] = 'Bearer '+token
print('Ahora que tenemos token, pruebo acceder a todos los usuarios')
users = get('http://127.0.0.1:5000/users/',headers=headersJson)
print(users.json())

print('\n\nPrueba Gimnasios')
gyms = get('http://127.0.0.1:5000/gyms/',headers=headersJson)
print(gyms.json())

print('\n\nAñado Gym')
new_gym = post('http://127.0.0.1:5000/gyms/add',headers=headersJson,json={'name':'HerculesGym','location':'Villa del Parque'})
print(new_gym.json())

print('\n\nPrueba Gimnasios Otra Vez')
gyms = get('http://127.0.0.1:5000/gyms/',headers=headersJson)
print(gyms.json())


print('\n\nPrueba UserType')
gyms = get('http://127.0.0.1:5000/user_types/',headers=headersJson)
print(gyms.json())

print('\n\nAñado UserType')
new_gym = post('http://127.0.0.1:5000/user_types/add',headers=headersJson,json={'name':'Premium'})
print(new_gym.json())

print('\n\nPrueba UserType Otra Vez')
gyms = get('http://127.0.0.1:5000/user_types/',headers=headersJson)
print(gyms.json())


print('\n\nPrueba UserTypeGym')
gyms = get('http://127.0.0.1:5000/user_type_gyms/',headers=headersJson)
print(gyms.json())

print('\n\nAñado UserType')
new_gym = post('http://127.0.0.1:5000/user_type_gyms/assign',headers=headersJson,json={
    'user_id':'1',
    'gym_id':'1',
    'user_type_id':'1'})
print(new_gym.json())

print('\n\nPrueba UserType Otra Vez')
gyms = get('http://127.0.0.1:5000/user_type_gyms/',headers=headersJson)
print(gyms.json())

print('\n\nPrueba de creacion de ingredientes')
new_ingredient = post(
    'http://127.0.0.1:5000/ingredients/',
    headers=headersJson,
    json={"name": "Tomate"}
)
print(new_ingredient.json())
print("resultado correcto por elemento duplicado")


print('\n\nPrueba de obtener todos los ingredientes')


response = get('http://127.0.0.1:5000/ingredients/', headers=headersJson)

print(response.json())


if response.status_code == 200:
    print('Ingredientes obtenidos exitosamente.')
    if len(response.json()) == 0:
        print('La lista de ingredientes está vacia.')
    else:
        print(f'Se encontraron {len(response.json())} ingredientes.')
else:
    print(f'Error al obtener ingredientes: {response.status_code}, {response.json()}')

