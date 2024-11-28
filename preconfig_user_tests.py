from requests import put, get, delete, post


def pregonfig(verbose=False):

    headersJson = {'Content-Type': 'application/json'}

    registro = post('http://127.0.0.1:5000/users/register',
                    headers=headersJson,
                    json={"first_name": "Marcelo",
                          "last_name": "Ulrich",
                          "email": "mulrich@estudiantes.unsam.edu.ar",
                          "password": "pass123",
                          "certified": False})

    if verbose:
        print('\n\nProbando registro...')
    if registro.status_code == 201:
        if verbose:
            print('Registro exitoso')
    else:
        if verbose:
            print('ERROR en registro: '+registro.json()['message'])

    if verbose:
        print('\n\nPrueba login exitoso')
    login_success = post('http://127.0.0.1:5000/users/login',
                         headers=headersJson,
                         json={"email": "mulrich@estudiantes.unsam.edu.ar",
                               "password": "pass123"})
    if verbose:
        print(login_success.json())
    token = login_success.json()['token']

    headersJson['Authorization'] = 'Bearer '+token

    return headersJson
