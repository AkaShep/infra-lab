import json

# Из строки в объект и обратно
text = '{"name": "web-01", "ports": [80, 443], "active": true, "owner": null}'
data = json.loads(text)
print(data["ports"][0])      # 80
print(type(data["active"]))  # <class 'bool'>

data["ports"].append(8080)
print(json.dumps(data, indent=2, ensure_ascii=False))

# Запись в файл и чтение из файла
with open("server.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

with open("server.json", encoding="utf-8") as f:
    loaded = json.load(f)

print(loaded == data)  # True