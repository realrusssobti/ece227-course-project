"""
Downloads the Higgs Twitter dataset from SNAP into data/.
https://snap.stanford.edu/data/higgs-twitter.html
"""

import os
import urllib.request
import gzip
import shutil

BASE_URL = "https://snap.stanford.edu/data/"
FILES = [
    "higgs-social_network.edgelist.gz",
    "higgs-retweet_network.edgelist.gz",
    "higgs-reply_network.edgelist.gz",
    "higgs-mention_network.edgelist.gz",
    "higgs-activity_time.txt.gz",
]
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def download_and_extract(filename: str) -> None:
    url = BASE_URL + filename
    gz_path = os.path.join(DATA_DIR, filename)
    out_path = os.path.join(DATA_DIR, filename[:-3])  # strip .gz

    if os.path.exists(out_path):
        print(f"  already exists, skipping: {out_path}")
        return

    print(f"  downloading {filename} ...")
    urllib.request.urlretrieve(url, gz_path)

    print(f"  extracting -> {out_path}")
    with gzip.open(gz_path, "rb") as f_in, open(out_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

    os.remove(gz_path)


def main() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    for filename in FILES:
        download_and_extract(filename)
    print("Done. Files are in", DATA_DIR)


if __name__ == "__main__":
    main()
