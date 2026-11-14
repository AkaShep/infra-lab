import requests

# 1. Простой GET
r = requests.get("https://httpbin.org/get", timeout=10)
print(r.status_code)      # 200
print(r.headers["Content-Type"])
print(r.json()["url"])

# 2. Параметры запроса (?name=value) и заголовки
r = requests.get(
    "https://httpbin.org/get",
    params={"q": "devops", "page": 1},
    headers={"User-Agent": "infra-lab/1.0"},
    timeout=10,
)
print(r.url)  # https://httpbin.org/get?q=devops&page=1

# 3. POST с JSON-телом
r = requests.post("https://httpbin.org/post", json={"name": "web-01", "active": True}, timeout=10)
print(r.json()["json"])

# 4. Проверка ошибок
r = requests.get("https://httpbin.org/status/404", timeout=10)
try:
    r.raise_for_status()
except requests.HTTPError as exc:
    print("Ошибка HTTP:", exc)