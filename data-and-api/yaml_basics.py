import yaml

with open("server.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)

print(config["environment"])
for server in config["servers"]:
    state = "включён" if server["active"] else "выключен"
    print(f'{server["name"]}: {server["ip"]} ({state})')

# Изменяем и записываем обратно
config["servers"].append({"name": "cache-01", "ip": "10.0.0.13", "ports": [6379], "active": True})

with open("servers_new.yaml", "w", encoding="utf-8") as f:
    yaml.safe_dump(config, f, allow_unicode=True, sort_keys=False)