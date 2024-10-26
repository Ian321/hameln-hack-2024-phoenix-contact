"""Simple pump."""
import datetime

from src.model import KW, Liter, LiterPerSecond, Pump


class SimplePump(Pump):
    """Pump without windup."""

    def __init__(self, power: KW, volume: LiterPerSecond, min_duration: datetime.timedelta):
        super().__init__()
        self.power = power
        self.volume = volume
        self.min_duration = min_duration
        self.percentage = 0.0

    def want(self, power_percentage):
        self.percentage = power_percentage

    def step(self, duration):
        return (
            KW(self.percentage * self.power.kw * duration.seconds / 3600),
            Liter(self.percentage * self.volume.lps * duration.seconds)
        )
