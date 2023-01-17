from pathlib import Path
from urllib.request import Request, urlopen

CACHE_FOLDER = Path(".inputs")
COOKIE_TOKEN = Path(".token")


def download_input(day: int, year: int = 2021) -> Path:
    CACHE_FOLDER.mkdir(parents=True, exist_ok=True)
    filename = CACHE_FOLDER / Path(f"{day:02}.txt")

    if filename.exists():
        print(f"Using cached input {filename}")
        return filename

    with open(COOKIE_TOKEN) as f:
        token = f.read()

    url = f"https://adventofcode.com/{year}/day/{day}/input"

    req = Request(url)
    req.add_header("Cookie", token)
    content = urlopen(req).read()

    with open(filename, "wb") as f:
        f.write(content)

    return filename
