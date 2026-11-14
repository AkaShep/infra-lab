import argparse
import logging
import shutil
import sys
from datetime import datetime
from pathlib import Path


def make_backup(src: Path, dst: Path, prefix: str) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tmp_base = dst / f".tmp_{prefix}_{stamp}"
    final = dst / f"{prefix}_{stamp}.zip"
    # Архив сначала пишется во временный файл, чтобы не остался битый "готовый" бэкап
    tmp_archive = Path(shutil.make_archive(str(tmp_base), "zip", root_dir=src))
    tmp_archive.replace(final)
    return final


def rotate(dst: Path, prefix: str, keep: int) -> list:
    archives = sorted(dst.glob(f"{prefix}_*.zip"))
    removed = archives[:-keep] if len(archives) > keep else []
    for old in removed:
        old.unlink()
    return removed


def main() -> int:
    parser = argparse.ArgumentParser(description="Бэкап каталога с ротацией")
    parser.add_argument("--source", required=True, help="что копировать")
    parser.add_argument("--dest", required=True, help="куда складывать архивы")
    parser.add_argument("--keep", type=int, default=7, help="сколько копий хранить")
    parser.add_argument("--name", default="backup", help="префикс имени архива")
    args = parser.parse_args()

    src = Path(args.source).resolve()
    dst = Path(args.dest).resolve()

    if args.keep < 1:
        print("Параметр --keep должен быть не меньше 1")
        return 2
    if not src.is_dir():
        print(f"Каталог не найден: {src}")
        return 2
    if dst == src or src in dst.parents:
        print("Папка бэкапов не должна находиться внутри копируемого каталога")
        return 2

    dst.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(dst / "backup.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    try:
        archive = make_backup(src, dst, args.name)
        size_mb = archive.stat().st_size / 1024 / 1024
        logging.info("Создан %s (%.1f МБ)", archive.name, size_mb)
        for old in rotate(dst, args.name, args.keep):
            logging.info("Удалён старый архив %s", old.name)
    except Exception:
        logging.exception("Бэкап не удался")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())