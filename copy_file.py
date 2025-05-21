#!/usr/bin/python
# -*- coding: utf-8 -*-


from pathlib import Path
from time import time
import shutil
import argparse
import logging
import sys


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse arguments for source and destination folders"""
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=str, help="Path to source directory")
    parser.add_argument(
        "destination",
        type=str,
        nargs="?",
        default="dist",
        help="Path to destination directory (default './dist')",
    )
    return parser.parse_args()


def read_folder(source_path: Path, dest_path: Path):
    """Read and process all files recursively in the source folder"""
    try:
        for item in source_path.iterdir():
            if item.is_dir():
                read_folder(item, dest_path)
            elif item.is_file():
                extension = item.suffix.lower()  # .txt, .jpg etc.
                if not extension:
                    extension = ".no_extension"
                ext_dir = dest_path / extension[1:]
                ext_dir.mkdir(parents=True, exist_ok=True)
                dest_file = ext_dir / item.name
                try:
                    shutil.copy2(item, dest_file)
                    logger.info(f"Скопійовано: {item} -> {dest_file}")
                except IOError as e:
                    logger.info(f"Помилка копіювання {item}: {e}")

    except PermissionError:
        logger.info(f"Помилка доступу до {source_path}")
    except OSError as e:
        logger.info(f"Помилка обробки {source_path}: {e}")


def main():
    start_time = time()

    args = parse_arguments()
    source = Path(args.source)
    destination = Path(args.destination)

    if not source.exists() or not source.is_dir():
        logger.error(f"Error: {source} does not exist or is not a directory.")
        sys.exit(1)

    destination.mkdir(parents=True, exist_ok=True)

    read_folder(source, destination)
    logger.info("Готово!")

    execution_time = time() - start_time
    logger.info(f"Completed in {execution_time:.2f} seconds")


if __name__ == "__main__":
    main()
