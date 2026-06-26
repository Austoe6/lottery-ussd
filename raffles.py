"""Raffle catalogue for the LuckyDraw USSD lottery."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Raffle:
    id: str
    name: str
    prize: str
    price_kes: int
    draw_date: str


CATEGORIES = {
    "1": {
        "title": "Cash Prizes",
        "raffles": [
            Raffle("cash-daily", "Daily Cash", "KES 10,000", 50, "2026-06-30"),
            Raffle("cash-weekly", "Weekly Cash", "KES 50,000", 100, "2026-07-06"),
            Raffle("cash-mega", "Mega Cash", "KES 500,000", 500, "2026-07-31"),
        ],
    },
    "2": {
        "title": "Motorbike Raffle",
        "raffles": [
            Raffle("bike-honda", "Honda Dream", "Honda Dream 150cc", 200, "2026-07-15"),
            Raffle("bike-yamaha", "Yamaha FZ", "Yamaha FZ-S", 500, "2026-07-31"),
        ],
    },
    "3": {
        "title": "Car Raffle",
        "raffles": [
            Raffle("car-vitz", "Toyota Vitz", "Toyota Vitz 2018", 1000, "2026-08-01"),
            Raffle("car-prado", "Toyota Prado", "Toyota Prado TX", 5000, "2026-08-31"),
        ],
    },
    "4": {
        "title": "Household Items",
        "raffles": [
            Raffle("home-tv", "Smart TV", '55" Smart TV', 150, "2026-07-10"),
            Raffle("home-fridge", "Fridge", "Double-door Fridge", 200, "2026-07-20"),
            Raffle("home-washer", "Washing Machine", "Front-load Washer", 250, "2026-07-25"),
        ],
    },
}


def get_raffle(category_key: str, raffle_index: int) -> Raffle | None:
    category = CATEGORIES.get(category_key)
    if not category:
        return None
    raffles = category["raffles"]
    if raffle_index < 1 or raffle_index > len(raffles):
        return None
    return raffles[raffle_index - 1]
