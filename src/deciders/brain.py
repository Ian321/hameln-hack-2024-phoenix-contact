"""Brain decider."""
import random
import math

from src import model


def leaky_relu(x: float, a=0.0) -> float:
    """LeakyReLU"""
    if x < 0.0:
        return x * a
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

    def __init__(self, l1: int, l2: int):
        self.l1w = l1
        self.l2w = l2
        self.w1 = [random.uniform(-1.0, 1.0) for _ in range(l1)]
        self.b1 = [random.uniform(-1.0, 1.0) for _ in range(l1)]
        self.w2 = [random.uniform(-1.0, 1.0) for _ in range(l2)]
        self.b2 = [random.uniform(-1.0, 1.0) for _ in range(l2)]
        self.w3 = [random.uniform(-1.0, 1.0) for _ in range(2)]
        self.b3 = [random.uniform(-1.0, 1.0) for _ in range(2)]

    def mutate(self, m: float):
        """Some random mutation."""
        other = BrainDecider(self.l1w, self.l2w)
        other.w1 = [clamp(before + random.uniform(-m, m))
                    for before in self.w1]
        other.b1 = [clamp(before + random.uniform(-m, m))
                    for before in self.b1]
        other.w2 = [clamp(before + random.uniform(-m, m))
                    for before in self.w2]
        other.b2 = [clamp(before + random.uniform(-m, m))
                    for before in self.b2]
        other.w3 = [clamp(before + random.uniform(-m, m))
                    for before in self.w3]
        other.b3 = [clamp(before + random.uniform(-m, m))
                    for before in self.b3]
        return other

    def decide(self, tank):
        time = (tank.time.second +
                tank.time.minute * 60 +
                tank.time.hour * 60 * 60)
        l0 = [
            scale(time, 0, 24 * 60 * 60),
            scale(tank.tank.l, 0, tank.tank_max.l),
            tank.energy_price.get(tank.time)
        ]
        l1 = [
            leaky_relu(sum(w0 * w1 for w0 in l0) + b1)
            for w1, b1 in zip(self.w1, self.b1)
        ]
        l2 = [
            leaky_relu(sum(w1 * w2 for w1 in l1) + b2)
            for w2, b2 in zip(self.w2, self.b2)
        ]
        l3 = [
            leaky_relu(sum(w2 * w3 for w2 in l2) + b3)
            for w3, b3 in zip(self.w3, self.b3)
        ]
        l4 = softmax(l3)
        if l4[0] > 0.5:
            return 1.0
        return 0.0
