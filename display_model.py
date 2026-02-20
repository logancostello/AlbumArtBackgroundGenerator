import tkinter as tk
from PIL import Image, ImageTk
import os
import random
import pandas as pd

from models.Random import RandomModel
from models.Average import AverageModel
from models.MostCommon import MostCommonModel
from models.QuantizedMostCommon import QuantizedMostCommon


def get_already_downloaded(output_dir):
    return [
        f.replace('.jpg', '')
        for f in os.listdir(output_dir)
        if f.endswith('.jpg')
    ]


def get_bg_color(image_path, model):
    bg = model.predict(image_path)
    r, g, b = [int(x * 255) if x <= 1.0 else int(x) for x in bg]
    return f"#{r:02x}{g:02x}{b:02x}"


def load_cover(index, current_model):
    cover_id = covers[index]
    path = f"data/covers/{cover_id}.jpg"
    bg = get_bg_color(path, current_model)

    root.configure(bg=bg)
    img = Image.open(path)
    photo = ImageTk.PhotoImage(img)
    label.configure(image=photo, bg=bg)
    label.image = photo
    model_label.configure(text=current_model.name, bg=bg)

    # look up metadata
    row = cover_metadata[cover_metadata["id"] == cover_id]
    if not row.empty:
        title = row.iloc[0]["title"]
        artists = row.iloc[0]["artists"]
        year = str(row.iloc[0]["release_date"])[:4]
        info_label.configure(text=f"{title}\n{artists}\n{year}", bg=bg)
    else:
        info_label.configure(text="", bg=bg)

    root.title(f"{cover_id}  ({index + 1}/{len(covers)})")


def on_key(event):
    global current_cover
    global current_model
    if event.keysym == "Right":
        current_cover = (current_cover + 1) % len(covers)
    elif event.keysym == "Left":
        current_cover = (current_cover - 1) % len(covers)
    elif event.keysym == "Up":
        current_model = (current_model + 1) % len(models)
    elif event.keysym == "Down":
        current_model = (current_model - 1) % len(models)
    else:
        return
    load_cover(current_cover, models[current_model])


if __name__ == "__main__":

    cover_metadata = pd.read_parquet("data/clean/release_group.parquet", columns=["id", "title", "artists", "release_date"])
    cover_metadata["id"] = cover_metadata["id"].astype(str)

    covers = get_already_downloaded("data/covers")
    random.shuffle(covers)
    current_cover = 0

    models = [
        RandomModel(),
        AverageModel(),
        MostCommonModel(),
        QuantizedMostCommon(4),
        QuantizedMostCommon(8),
        QuantizedMostCommon(16)
        ]
    current_model = 0

    root = tk.Tk()
    root.geometry("400x400")
    root.bind("<KeyPress>", on_key)

    model_label = tk.Label(root, font=("Helvetica", 20, "bold"), fg="white")
    model_label.pack(pady=(15, 0))

    label = tk.Label(root)
    label.pack(pady=(10, 0))

    info_label = tk.Label(root, font=("Helvetica", 20), fg="white", justify="center")
    info_label.pack(pady=(8, 15))

    load_cover(current_cover, models[current_model])
    root.mainloop()