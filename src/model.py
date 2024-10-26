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
    def get(self, time: datetime.datetime):
        """Get the price at a given time."""


class FixedPowerPrice(PowerPrice):
    """Class to get a fixed price for electricity."""
    def __init__(self, price: float):
        super().__init__()
        self.price = price

    def get(self, time: datetime.datetime):
        return self.price


class Wasserwerk:
    """Ein Standort."""

    def __init__(
            self,
            tank_size: float, tank_min: float,
            pump_kwh: float, pump_lh: float,
            e_price: PowerPrice,
            pv_max: float = None, pv_location: Location = None,
            generator_kwh: float = None
    ):
        pass
