import random

class RandomModel:

    def __init__(self):
        self.name = "Random"

    def train(self):
        pass

    def predict(self, cover):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        return (r, g, b)