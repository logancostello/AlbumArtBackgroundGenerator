from PIL import Image
from collections import Counter

class MostCommonModel:

    def __init__(self):
        self.name = "Most Common Color"

    def train(self):
        pass

    def predict(self, path):
        img = Image.open(path)
        pixels = list(img.getdata())
        return Counter(pixels).most_common(1)[0][0]  