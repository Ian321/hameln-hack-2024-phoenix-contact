"""Test the base case."""
import datetime
import unittest

import pandas as pd

from src import model
from src.deciders.simple import SimpleDecider
from src.pumps.simple import SimplePump

start_time = datetime.datetime.fromisoformat("2024-04-01T00:00Z")
price = pd.read_csv("./data/price.csv")
price = price["fix [ct/kWh]"][0]
price = model.FixedPowerPrice(price.item() / 100)
decider = SimpleDecider()
drain = pd.read_csv("./data/drain.csv")


class TestBaseCase(unittest.TestCase):
    """Test the base case."""

    def test_1(self):
        """Test Tank1"""
        pump = SimplePump(model.KW(20), model.LiterPerSecond(
            16.5), datetime.timedelta(minutes=15))
        tank = model.Tank(
            start_time,
            model.Liter(540), model.Liter(540*0.1), model.Liter(540*0.5),
            pump, price, decider
        )
        for volume in drain["Tank1"]:
            tank.step(datetime.timedelta(minutes=15),
                      model.LiterPerSecond(volume))

        self.assertEqual(round(tank.cost, 2), 101.56)
        self.assertEqual(round(tank.tank.l, 2) - 9.0, tank.tank_max.l / 2)

    def test_2(self):
        """Test Tank2"""
        pump = SimplePump(model.KW(15), model.LiterPerSecond(
            11.2), datetime.timedelta(minutes=15))
        tank = model.Tank(
            start_time,
            model.Liter(154), model.Liter(154*0.1), model.Liter(154*0.5),
            pump, price, decider
        )
        for volume in drain["Tank2"]:
            tank.step(datetime.timedelta(minutes=15),
                      model.LiterPerSecond(volume))

        self.assertEqual(round(tank.cost, 2), 70.13)
        self.assertEqual(round(tank.tank.l, 2) - 10, tank.tank_max.l / 2)


if __name__ == "__main__":
    unittest.main()
