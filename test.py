from requests import put, get

task_local = {f"task{i}": f"BBB{i}" for i in range(3)}
# print("Registro actual")
# print(get("http://127.0.0.1:5000/task1").json())

for key, value in task_local.items():
    url = f"http://127.0.0.1:5000/{key}"
    response = put(url, data={"task_id": value})
    print(response.json())
    print(response.status_code)

for key in task_local.keys():
    url = f"http://127.0.0.1:5000/{key}"
    response = get(url)
    print(response.json())
    print(response.status_code)

print(get("http://127.0.0.1:5000/4"))
