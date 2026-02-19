import pandas as pd
import json

data = []

with open('data/mbdump/release-group', 'r') as f:
    for line in f:
        rg = json.loads(line)

        id = rg["id"]
        title = rg["title"]
        artists = " | ".join([a["artist"]["name"] for a in rg["artist-credit"]])
        genres = " | ".join([g["name"] for g in rg["genres"]])
        release_date = rg["first-release-date"]
        primary_type = rg["primary-type"]

        if primary_type != "Album":
            continue
        print(id)
        data.append([
            id, 
            primary_type,
            title,
            artists,
            release_date,
            genres
        ])

df = pd.DataFrame(data, columns=["id", "primary_type", "title", "artists", "release_date", "genres"])
df.to_parquet("../data/clean/release_group.parquet")