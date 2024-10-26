"""Model of everything."""
import datetime
from dataclasses import dataclass
from abc import ABC, abstractmethod


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


class KWH:
    """Unit: KWH"""

    def __init__(self, kwh: float):
        self.kwh = kwh


class PV(ABC):
    """Abstact class for a PV."""
    @abstractmethod
    def get(self, time: datetime.datetime, duration: datetime.timedelta) -> KWH:
        """Get the produced power at a given time and duration."""


class Generator:
    """Turbine that generates power as it flows out of the tank."""

    def __init__(self, power_per_liter: KWH):
        self.ppl = power_per_liter

    def get(self, liters: Liter) -> KWH:
        """Get the power generated."""
        return KWH(self.ppl * liters.l)


class Wasserwerk:
    """Ein Standort."""

    def __init__(
            self,
            tank_size: Liter, tank_min: Liter, tank_start: Liter,
            pump_power: KWH, pump_volume: Liter, pump_min: datetime.timedelta,
            e_price: PowerPrice,
            pv: PV = None, generator: Generator = None
    ):
        pass
