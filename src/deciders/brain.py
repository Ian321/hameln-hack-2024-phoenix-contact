"""Brain decider."""
import json
import math
import random

from src import model


def relu(x: float) -> float:
    """ReLU"""
    if x <= 0.0:
        return 0.0
    return x


def softmax(x: list[float]) -> list[float]:
    """SOFTMAX"""
    tmp = [math.exp(v) for v in x]
    total = sum(tmp)
    return [t / total for t in tmp]


def scale(x, i_min, i_max):
    """Scale a number to between 0 and 1."""
    return (x - i_min) / i_max


def clamp(x: float):
    """Clamp between -1 and 1"""
    if x < -1.0:
        return -1.0
    if x > 1.0:
        return 1.0
    return x


class BrainDecider(model.Decider):
    """Use a NN to make the decision."""

    def __init__(self, sizes: list[int] = None):
        if not sizes and sizes != []:
            sizes = [5, 5]
        self.sizes = sizes + [2]
        self.weights: list[list[float]] = []
        self.biases: list[list[float]] = []
        for size in self.sizes:
            self.weights.append([
                random.uniform(-1.0, 1.0) for _ in range(size)
            ])
            self.biases.append([
                random.uniform(-1.0, 1.0) for _ in range(size)
            ])

    def mutate(self, m: float):
        """Some random mutation."""
        other = BrainDecider([])
        other.sizes = self.sizes
        other.weights = []
        other.biases = []

        for weights in self.weights:
            other.weights.append([
                clamp(w + random.uniform(-m, m))
                for w in weights
            ])
        for biases in self.biases:
            other.biases.append([
                clamp(b + random.uniform(-m, m))
                for b in biases
            ])
        return other

    def decide(self, tank):
        current = [
            scale(tank.tank.l, 0, tank.tank_max.l),
            tank.energy_price.get(tank.time)
        ]
        for layer in range(len(self.sizes)):
            next_layer = []
            for weight, bias in zip(self.weights[layer], self.biases[layer]):
                summation = bias
                for before in current:
                    summation += weight * before
                next_layer.append(relu(summation))
            current = next_layer

        last = softmax(current)
        if last[0] > 0.5:
            return 1.0
        return 0.0

    @staticmethod
    def from_file(path: str) -> "BrainDecider":
        """Load the brain from a file."""
        x = BrainDecider([])
        with open(path, "r", encoding="utf8") as fp:
            data = json.load(fp)
        x.weights = data["weights"]
        x.biases = data["biases"]

        ws = [len(w) for w in x.weights]
        bs = [len(b) for b in x.biases]
        for w, b in zip(ws, bs):
            assert w == b

        x.sizes = ws
        return x
