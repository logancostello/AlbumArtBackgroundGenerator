from PIL import Image
from collections import Counter

class QuantizedMostCommon:

    def __init__(self, n_colors=16):
        self.name = f"Most Common Quantized Color ({n_colors})"
        self.n_colors = n_colors

    def train(self):
        pass

    def predict(self, path):
        img = Image.open(path).quantize(colors=self.n_colors).convert("RGB")
        pixels = list(img.getdata())
        return Counter(pixels).most_common(1)[0][0]  