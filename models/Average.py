from PIL import Image
import numpy as np

class AverageModel:

    def __init__(self):
        self.name = "Average Color"

    def train(self):
        pass

    def predict(self, path):
        img = Image.open(path)
        pixels = np.array(img)
        avg_color = pixels.mean(axis=0)
        return avg_color.flatten()[:3]