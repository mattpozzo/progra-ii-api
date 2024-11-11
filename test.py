from requests import put, get, delete, post

#probando que el token es necesario
print('Probando que el token es necesario')
get_users_test1 = get('http://127.0.0.1:5000/users/')
print(get_users_test1.json())

registro = post('http://127.0.0.1:5000/users/register',
                headers={'Content-Type': 'application/json'},
                json={"first_name": "Marcelo", 
                      "last_name": "Ulrich", 
                      "email": "mulrich@estudiantes.unsam.edu.ar", 
                      "password": "pass123", 
                      "certified": False})

print('Probando registro...')
if registro.status_code == 201:
    print('Registro exitoso')
else:
    print('ERROR en registro: '+registro.json()['message'])



