"""It's evolution baby!!!"""
import datetime
import json
import multiprocessing
import multiprocessing.pool

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

TANKS = 20


def run_tank(args: tuple[int, model.Tank]):
    """Simulate in another thread."""
    index, tank = args
    for volume in tqdm(drain["Tank1"], disable=index):
        if tank.cost > 4_000:
            break

        tank.foreward(datetime.timedelta(minutes=15),
                      model.LiterPerSecond(volume))
        if (tank.tank < tank.tank_min or
                tank.tank > tank.tank_max):
            tank.cost += 4_004

    off_by = abs(tank.tank.l - (tank.tank_max.l / 2))
    tank.cost += (off_by / tank.tank_max.l) * 2000
    return tank


class Evolution:
    """Use some genetic algorithm to find the best decider."""

    def __init__(self, brains: list[BrainDecider] = None):
        if not brains:
            brains = [
                BrainDecider() for _ in range(TANKS)
            ]

        self.tanks = [model.Tank(
            start_time,
            model.Liter(540_000), model.Liter(
                540_000*0.1), model.Liter(540_000*0.5),
            pump, price, decider
        ) for decider in brains]

    def run(self, pool: multiprocessing.pool.Pool) -> list[BrainDecider]:
        """Run one epoch."""
        self.tanks = pool.map(run_tank, enumerate(self.tanks))
        self.tanks.sort(key=lambda tank: tank.cost)
        print(
            f"cost: {self.tanks[0].cost:.2f}, volume: {self.tanks[0].tank.l:.2f}")
        return [self.tanks[i].decider for i in range(3)]


def main():
    """Run it"""
    with multiprocessing.Pool() as pool:
        e = Evolution()
        best = e.run(pool)

        for i in range(16):
            brains = []
            brains.extend([x.mutate(0.0) for x in best])
            brains.extend([x.mutate(0.125) for x in best])
            brains.extend([x.mutate(0.25) for x in best])
            brains.extend([x.mutate(0.5) for x in best])
            brains.extend([x.mutate(0.9**(i*2)) for x in best*2])
            while len(brains) < TANKS:
                brains.append(BrainDecider())
            assert len(brains) == TANKS
            e = Evolution(brains)
            best = e.run(pool)

        pool.close()
        pool.join()
    print(json.dumps({
        "weights": best[0].weights,
        "biases": best[0].biases
    }))


if __name__ == "__main__":
    main()
