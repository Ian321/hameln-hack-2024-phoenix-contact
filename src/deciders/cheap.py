"""Cheap decider."""
import datetime
from src import model


class CheapDecider(model.Decider):
    """Only buy if under X."""

    def __init__(self, max_price: float):
        self.max = max_price
        super().__init__()

    def decide(self, tank):
        if tank.tank < tank.tank_min:
            raise ValueError("Tank got too low.")
        if tank.energy_price.get(tank.time) > self.max:
            return 0.0
        if tank.safe_pump(datetime.timedelta(minutes=15)):
            return 1.0
        if tank.safe_pump(datetime.timedelta(minutes=1)) and tank.pump.current() > 0.0:
            return 1.0
        return 0.0
