"""Calculate the the price from the data."""
import pandas as pd


def main(col: str, kwh: float, lps: float):
    """Returns the price in EUR"""
    drain = pd.read_csv("./data/drain.csv")
    price = pd.read_csv("./data/price.csv")
    price = price["fix [ct/kWh]"][0]

    volume = drain[col].sum() * 15 * 60
    geld = (price / 100) * kwh * ((volume / lps) / 3600)
    return geld.item()


if __name__ == "__main__":
    t1 = main("Tank1", 20, 16.5)
    t2 = main("Tank2", 15, 11.2)
    print(f"{t1:.2f}€")
    print(f"{t2:.2f}€")
