"""It's evolution baby!!!"""
import datetime

import pandas as pd
from tqdm import tqdm

from src import model
from src.deciders.brain import BrainDecider
from src.pumps.simple import SimplePump

start_time = datetime.datetime.fromisoformat("2024-04-01T00:00Z")
pump = SimplePump(model.KW(20), model.LiterPerSecond(
    16.5), datetime.timedelta(minutes=15))
drain = pd.read_csv("./data/drain.csv")

prices = pd.read_csv("./data/price.csv")
prices["datetime"] = prices["Tag"] + "T" + prices["Uhrzeit"]
prices["datetime"] = pd.to_datetime(prices["datetime"].str.split(" ").str[0])
price = model.DynamicPowerPrice(
    prices["datetime"].to_list(), (prices["flexibel [ct/kWh]"] / 100).to_list())


class Evolution:
    """Use some genetic algorithm to find the best decider."""

    def __init__(self, brains: list[BrainDecider] = None):
        if not brains:
            brains = [
                BrainDecider(5, 5) for _ in range(10)
            ]

        self.tanks = [model.Tank(
            start_time,
            model.Liter(540_000), model.Liter(
                540_000*0.1), model.Liter(540_000*0.5),
            pump, price, decider
        ) for decider in brains]

    def run(self) -> list[BrainDecider]:
        """Run one epoch."""
        number = len(drain)
        for index, volume in enumerate(tqdm(drain["Tank1"])):
            for tank in self.tanks:
                if tank.cost > 1_000:
                    continue

                tank.foreward(datetime.timedelta(minutes=15),
                              model.LiterPerSecond(volume))
                if (tank.tank < tank.tank_min or
                        tank.tank > tank.tank_max):
                    tank.cost += 1_001 * (number - index)

        # for tank in self.tanks:
        #     tank.cost += abs(tank.tank.l - (tank.tank_max.l / 2)) * 2

        self.tanks.sort(key=lambda tank: tank.cost)
        print(self.tanks[0].cost)
        return [self.tanks[i].decider for i in range(3)]


def main():
    """Run it"""
    e = Evolution()
    best = e.run()

    for _ in range(10):
        brains = []
        brains.extend([x.mutate(0.0) for x in best])
        brains.extend([x.mutate(0.25) for x in best])
        brains.extend([x.mutate(0.5) for x in best])
        brains.append(BrainDecider(5, 5))
        assert len(brains) == 10
        e = Evolution(brains)
        best = e.run()


if __name__ == "__main__":
    main()
