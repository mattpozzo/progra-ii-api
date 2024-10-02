from requests import put, get, delete

task_local = {f"task{i}": f"BBB{i}" for i in range(3)}
# print("Registro actual")
# print(get("http://127.0.0.1:5000/task1").json())

print("Probando POST")
for key, value in task_local.items():
    url = f"http://127.0.0.1:5000/{key}"
    response = put(url, data={"name": value, "realizado": True})
    print(response.json())
    print(response.status_code)

print("Probando GET")
for key in task_local.keys():
    url = f"http://127.0.0.1:5000/{key}"
    response = get(url)
    print(response)
    print(response.json())
    print(response.status_code)

print("Probando DELETE")

url1 = "http://127.0.0.1:5000/task2"
url2 = "http://127.0.0.1:5000/task3"

res1 = delete(url1)
print("Eliminando task2")
print(res1)
print(res1.json())
res2 = delete(url2)
print("Elimnando task3 inexistente, no rompe")
print(res2)
print(res2.json())
print("Chequeo que task2 este eliminado")
print(get(url1).json())
