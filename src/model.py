"""Model of everything."""
import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Location:
    """Lat and Long."""
    lat: float
    lng: float


class PowerPrice(ABC):
    """Abstract class to get the price of electricity."""
    @abstractmethod
    def get(self, time: datetime.datetime) -> float:
        """Get the price at a given time."""


class FixedPowerPrice(PowerPrice):
    """Class to get a fixed price for electricity."""

    def __init__(self, price: float):
        super().__init__()
        self.price = price

    def get(self, time: datetime.datetime):
        return self.price


class Liter:
    """Unit: Liter"""

    def __init__(self, l: float):
        self.l = l

    def __add__(self, other: "Liter"):
        return Liter(self.l + other.l)

    def __sub__(self, other: "Liter"):
        return Liter(self.l - other.l)


class LiterPerSecond:
    """Unit: L/s"""

    def __init__(self, lps: float):
        self.lps = lps


class KW:
    """Unit: KW"""

    def __init__(self, kw: float):
        self.kw = kw


class PV(ABC):
    """Abstact class for a PV."""
    @abstractmethod
    def get(self, time: datetime.datetime, duration: datetime.timedelta) -> KW:
        """Get the produced power at a given time and duration."""


class Generator:
    """Turbine that generates power as it flows out of the tank."""

    def __init__(self, power_per_liter: KW):
        self.ppl = power_per_liter

    def get(self, liters: Liter) -> KW:
        """Get the power generated."""
        return KW(self.ppl * liters.l)


class Pump(ABC):
    """Abstract pump."""
    @abstractmethod
    def want(self, power_percentage: float):
        """Change the "wanted" state of the pump."""

    @abstractmethod
    def step(self, duration: datetime.timedelta) -> tuple[KW, Liter]:
        """Get the power used and volume pumped during a given duration."""


class Decider(ABC):
    """Abstract decider."""
    @abstractmethod
    def decide(self, tank: "Tank") -> float:
        """Decide what to do with the pump."""


class Tank:
    """A single container."""

    def __init__(
            self,
            start_time: datetime.datetime,
            tank_max: Liter, tank_min: Liter, tank_start: Liter,
            pump: Pump, energy_price: PowerPrice, decider: Decider,
            pv: PV = None, generator: Generator = None
    ):
        self.time = start_time
        self.tank_max = tank_max
        self.tank_min = tank_min
        self.tank = tank_start
        self.pump = pump
        self.energy_price = energy_price
        self.decider = decider
        self.pv = pv
        self.generator = generator
        self.cost = 0.0

    def step(self, duration: datetime.timedelta, drain: LiterPerSecond):
        """Step through time."""
        second = datetime.timedelta(seconds=1)
        for _ in range(duration.seconds):
            self.time += second
            self.tank -= Liter(drain.lps)

            self.pump.want(self.decider.decide(self))
            kw, l = self.pump.step(second)
            self.cost += kw.kw * self.energy_price.get(self.time)
            self.tank += l
