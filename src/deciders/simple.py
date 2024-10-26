"""Simple decider."""
import src.model as model

class SimpleDecider(model.Decider):
    """All or nothing if under 50%."""
    def decide(self, tank):
        if tank.tank.l < (tank.tank_max.l / 2):
            return 1.0
        return 0.0
