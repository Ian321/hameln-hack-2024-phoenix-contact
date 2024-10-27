"""Run the brain case."""
import datetime
import json

import pandas as pd

from src import model
from src.deciders.brain import BrainDecider
from src.pumps.simple import SimplePump


start_time = datetime.datetime.fromisoformat("2024-04-01T00:00Z")
prices = pd.read_csv("./data/price.csv")
drain = pd.read_csv("./data/drain.csv")

prices["datetime"] = prices["Tag"] + "T" + prices["Uhrzeit"]
prices["datetime"] = pd.to_datetime(prices["datetime"].str.split(" ").str[0])
price = model.DynamicPowerPrice(
    prices["datetime"].to_list(), (prices["flexibel [ct/kWh]"] / 100).to_list())

pump = SimplePump(model.KW(20), model.LiterPerSecond(16.5),
                  datetime.timedelta(minutes=15))
decider = BrainDecider.from_file("./data/model1.json")
tank = model.Tank(
    start_time,
    model.Liter(540_000), model.Liter(
        540_000*0.1), model.Liter(540_000*0.5),
    pump, price, decider
)

times = [tank.time]
volumes = [tank.tank.l]
powers = [tank.pump.current() * pump.power.kw]
costs = [tank.cost]

for volume in drain["Tank1"]:
    tank.foreward(datetime.timedelta(minutes=15),
                  model.LiterPerSecond(volume))
    times.append(tank.time)
    volumes.append(tank.tank.l)
    powers.append(powers[-1] + (tank.pump.current() * pump.power.kw))
    costs.append(tank.cost)

print(json.dumps({
    "time": [x.isoformat() for x in times],
    "volume": volumes,
    "power": powers,
    "cost": costs
}))
