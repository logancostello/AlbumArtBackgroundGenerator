import pandas as pd
import requests
from PIL import Image
import io
import os
import sys
import time

def get_already_downloaded(output_dir):
    return set(
        f.replace('.jpg', '') 
        for f in os.listdir(output_dir) 
        if f.endswith('.jpg')
    )

def get_failed(failed_file):
    if not os.path.exists(failed_file):
        return set()
    with open(failed_file, 'r') as f:
        return set(line.strip() for line in f if line.strip())

def save_failed(mbid, status_code, failed_file):
    with open(failed_file, 'a') as f:
        f.write(f"{mbid}\n")
    print(f"  ✗ {mbid} — HTTP {status_code}")

def get_cover_art(mbid):
    url = f"https://coverartarchive.org/release-group/{mbid}/front-250"
    try:
        r = requests.get(url, allow_redirects=True, timeout=10)
        if r.status_code == 200:
            img = Image.open(io.BytesIO(r.content))
            img.save(f"data/covers/{mbid}.jpg")
            return True, r.status_code, False  # success, status, is_transient
        return False, r.status_code, False
    except Exception as e:
        print(f"  ✗ {mbid} — Exception: {e}")
        return False, None, True  # transient, don't blacklist


if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("usage: fetch_art.py total_desired [min_year]")
        sys.exit()

    FAILED_FILE = "data/failed_mbids.txt"
    OUTPUT_DIR = "data/covers"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total_desired = int(sys.argv[1])
    min_year = int(sys.argv[2]) if len(sys.argv) == 3 else None

    print(f"Fetching until {total_desired} covers saved")
    if min_year:
        print(f"Filtering to releases after {min_year}")

    already_downloaded = get_already_downloaded(OUTPUT_DIR)
    failed = get_failed(FAILED_FILE)
    all_mbids = pd.read_parquet("data/clean/release_group.parquet", columns=["id", "release_date"])

    if min_year:
        year = pd.to_numeric(all_mbids["release_date"].str[:4], errors='coerce')
        all_mbids = all_mbids[year >= min_year]

    excluded = already_downloaded | failed
    candidates = all_mbids[~all_mbids["id"].isin(excluded)]["id"].tolist()

    num_downloaded = len(already_downloaded)
    print(f"Already downloaded: {num_downloaded}")
    print(f"Already failed:     {len(failed)}")
    print(f"Candidates:         {len(candidates)}")
    print(f"Need:               {total_desired - num_downloaded} more")

    status_counts = {}

    for mbid in candidates:
        if num_downloaded >= total_desired:
            break

        success, status_code, is_transient = get_cover_art(mbid)
        status_counts[status_code] = status_counts.get(status_code, 0) + 1

        if success:
            num_downloaded += 1
            print(f"  ✓ {mbid} — {num_downloaded}/{total_desired}")
        elif is_transient:
            print(f"  ~ {mbid} — transient error, skipping")
            time.sleep(2)
        else:
            save_failed(mbid, status_code, FAILED_FILE)

        time.sleep(0.1)

    print(f"\nDone. {num_downloaded} total saved.")
    print(f"Status code breakdown: {status_counts}")