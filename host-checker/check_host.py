import argparse
import json
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import yaml


def check_host(host, timeout):
    started = time.perf_counter()
    try:
        with socket.create_connection((host["address"], host["port"]), timeout=timeout):
            ok, error = True, None
    except OSError as exc:
        ok, error = False, str(exc)
    elapsed_ms = round((time.perf_counter() - started) * 1000, 1)
    return {
        "name": host["name"],
        "address": host["address"],
        "port": host["port"],
        "up": ok,
        "response_ms": elapsed_ms,
        "error": error,
    }


def main():
    parser = argparse.ArgumentParser(description="Проверка доступности хостов")
    parser.add_argument("--config", default="host.yaml")
    parser.add_argument("--output", default="report.json")
    parser.add_argument("--timeout", type=float, default=2.0)
    args = parser.parse_args()

    with open(args.config, encoding="utf-8") as f:
        hosts = yaml.safe_load(f)["hosts"]

    with ThreadPoolExecutor(max_workers=10) as pool:
        results = list(pool.map(lambda h: check_host(h, args.timeout), hosts))

    up = sum(1 for r in results if r["up"])
    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "summary": {"total": len(results), "up": up, "down": len(results) - up},
        "results": results,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"Доступно {up} из {len(results)}. Отчёт: {args.output}")
    sys.exit(0 if up == len(results) else 1)


if __name__ == "__main__":
    main()