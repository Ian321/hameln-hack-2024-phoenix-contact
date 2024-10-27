"""Run the brain case."""
import datetime
import json

import pandas as pd

from src import model
from src.deciders.brain import BrainDecider
from src.pumps.simple import SimplePump


start_time = datetime.datetime.fromisoformat("2024-07-01T00:00Z")
end_time = datetime.datetime.fromisoformat("2024-07-08T00:00Z")

data = pd.read_csv("./data/extended.csv")
data["datetime"] = pd.to_datetime(data["datetime"], utc=True)
data = data[data["datetime"] >= start_time]
data = data[data["datetime"] < end_time]
price = model.DynamicPowerPrice(
    data["datetime"].to_list(), (data["electricity_price"] / 100).to_list())

pump = SimplePump(model.KW(20), model.LiterPerSecond(16.5),
                  datetime.timedelta(minutes=15))
decider = BrainDecider.from_file("./data/modele.json")
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

for volume in data["drain"]:
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
