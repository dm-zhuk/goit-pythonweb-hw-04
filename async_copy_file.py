#!/usr/bin/python
# type: ignore

from aiopath import AsyncPath
from time import time
import asyncio
import aiofiles
import argparse
import logging
import sys


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# no changes for asyncronous code
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


async def copy_file(file_path: AsyncPath, dest_path: AsyncPath):
    """Copy file to subfolder based on extension"""
    try:
        extension = file_path.suffix.lower() or ".no_extension"
        ext_dir = dest_path / extension[1:]  # Remove dot from ext in dir name
        await ext_dir.mkdir(parents=True, exist_ok=True)
        dest_file = ext_dir / file_path.name

        # Used 'aiofiles' for async file reading and writing, which is faster for IO-bound tasks like file copying
        async with aiofiles.open(file_path, "rb") as src:
            content = await src.read()
        async with aiofiles.open(dest_file, "wb") as dst:
            await dst.write(content)

    except IOError as e:
        logger.error(f"Error copying {file_path}: {e}")


async def read_folder(source_path: AsyncPath, dest_path: AsyncPath):
    """Read and process all files recursively in the source folder"""
    try:
        async for item in source_path.iterdir():
            if await item.is_dir():
                await read_folder(item, dest_path)
            elif await item.is_file():
                await copy_file(item, dest_path)
    except PermissionError:
        logger.error(f"Permission denied: {source_path}")
    except IOError as e:
        logger.error(f"Error processing {source_path}: {e}")


async def main():
    """Main function to run the async file copying process"""
    start_time = time()

    args = parse_arguments()
    source = AsyncPath(args.source)
    destination = AsyncPath(args.destination)

    if not await source.exists() or not await source.is_dir():
        logger.error(f"Error: {source} does not exist or is not a directory.")
        sys.exit(
            1
        )  # If the directory is invalid, log an error and stop: '1' means error

    await destination.mkdir(parents=True, exist_ok=True)
    await read_folder(source, destination)

    execution_time = time() - start_time
    logger.info(f"Completed in {execution_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())

# eval $(poetry env activate)
# pip install --upgrade -r requirements.txt

# Example usage:

# 1- HW task with asyncronous code:
# python async_copy_file.py "/Users/macbook/Documents/Travel/Peru" "/Users/macbook/Documents/Travel/Peru01"

# 2- from previous HW without asyncronous code:
# python copy_file.py "/Users/macbook/Documents/Travel/Peru" "/Users/macbook/Documents/Travel/Peru02"

# 1- 2025-05-21 16:12:28,040 - INFO - Completed in 0.04 seconds
# 2- 2025-05-21 16:12:21,141 - INFO - Completed in 0.11 seconds
