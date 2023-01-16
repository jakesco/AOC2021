import urllib
from pathlib import Path

CACHE_FOLDER = Path("./.inputs")


def download_input(day: int, year: int = 2021) -> Path:
    CACHE_FOLDER.mkdir(parents=True, exist_ok=True)
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    filename = CACHE_FOLDER / Path(f"{day:02}.txt")
    filename.touch()
    return filename
