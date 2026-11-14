import argparse
import json
import sys

import requests
import yaml


def fetch_repo(repo: str) -> dict:
    url = f"https://api.github.com/repos/{repo}"
    r = requests.get(url, headers={"Accept": "application/vnd.github+json"}, timeout=10)
    r.raise_for_status()
    return r.json()


def extract(raw: dict) -> dict:
    license_info = raw.get("license") or {}
    return {
        "name": raw["full_name"],
        "description": raw.get("description"),
        "language": raw.get("language"),
        "stars": raw["stargazers_count"],
        "forks": raw["forks_count"],
        "open_issues": raw["open_issues_count"],
        "license": license_info.get("spdx_id"),
        "topics": raw.get("topics", []),
        "updated_at": raw["updated_at"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Информация о репозитории GitHub")
    parser.add_argument("repo", help="например, python/cpython")
    args = parser.parse_args()

    try:
        info = extract(fetch_repo(args.repo))
    except requests.HTTPError as exc:
        print(f"GitHub вернул ошибку: {exc}")
        return 1
    except requests.RequestException as exc:
        print(f"Сетевая ошибка: {exc}")
        return 1

    with open("repo_info.json", "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2, ensure_ascii=False)
    with open("repo_info.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(info, f, allow_unicode=True, sort_keys=False)

    with open("repo_info.json", encoding="utf-8") as f:
        from_json = json.load(f)
    with open("repo_info.yaml", encoding="utf-8") as f:
        from_yaml = yaml.safe_load(f)

    print("JSON и YAML совпадают:", from_json == from_yaml)
    print(f'{info["name"]}: {info["stars"]} звёзд, язык {info["language"]}')
    return 0


if __name__ == "__main__":
    sys.exit(main())