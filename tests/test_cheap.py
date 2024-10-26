"""Test the cheap case."""
import datetime
import unittest

import pandas as pd

from src import model
from src.deciders.cheap import CheapDecider
from src.pumps.simple import SimplePump

start_time = datetime.datetime.fromisoformat("2024-04-01T00:00Z")
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
        found = False
        for over in range(200):
            pump = SimplePump(model.KW(20), model.LiterPerSecond(
                16.5), datetime.timedelta(minutes=15))
            decider = CheapDecider((max_price.item() / 100) + (over / 100))
            tank = model.Tank(
                start_time,
                model.Liter(540_000), model.Liter(
                    540_000*0.1), model.Liter(540_000*0.5),
                pump, price, decider
            )

            try:
                for volume in drain["Tank1"]:
                    tank.step(datetime.timedelta(minutes=15),
                              model.LiterPerSecond(volume))
                found = True
                break
            except ValueError:
                continue

        self.assertTrue(found)


if __name__ == "__main__":
    unittest.main()
