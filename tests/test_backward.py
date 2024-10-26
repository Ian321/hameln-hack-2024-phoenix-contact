"""Test the backward method."""
import copy
import datetime
import unittest

import pandas as pd

from src import model
from src.deciders.cheap import CheapDecider
from src.pumps.simple import SimplePump

start_time = datetime.datetime.fromisoformat("2024-04-02T23:45Z")
prices = pd.read_csv("./data/price.csv")
max_price = prices["fix [ct/kWh]"][0]
drain = pd.read_csv("./data/drain.csv")

prices["datetime"] = prices["Tag"] + "T" + prices["Uhrzeit"]
prices["datetime"] = pd.to_datetime(prices["datetime"].str.split(" ").str[0])
price = model.DynamicPowerPrice(
    prices["datetime"].to_list(), (prices["flexibel [ct/kWh]"] / 100).to_list())


class TestCheapCase(unittest.TestCase):
    """Test the cheap case."""

    def test_1(self):
        """Test Tank1"""
        pump = SimplePump(model.KW(20), model.LiterPerSecond(
            16.5), datetime.timedelta(minutes=15))
        decider = CheapDecider(max_price.item() / 100)
        tank = model.Tank(
            start_time,
            model.Liter(540_000), model.Liter(
                540_000*0.1), model.Liter(540_000*0.5),
            pump, price, decider
        )

        for volume in reversed(drain["Tank1"]):
            clone = copy.deepcopy(tank)
            try:
                tank.backward(datetime.timedelta(minutes=15),
                              model.LiterPerSecond(volume),
                              [0.0]*(15*60))
            except ValueError:
                tank = clone
                tank.backward(datetime.timedelta(minutes=15),
                              model.LiterPerSecond(volume),
                              [1.0]*(15*60))


if __name__ == "__main__":
    unittest.main()
