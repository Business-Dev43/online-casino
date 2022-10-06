import random
from typing import Tuple


def generate_roll_values(block: int, choices: Tuple) -> Tuple:
    return tuple(random.choice(choices) for _ in range(block))


def re_roll_probability_30() -> int:
    return random.choice([1, 1, 1, 0, 0, 0, 0, 0, 0, 0])


def re_roll_probability_60() -> int:
    return random.choice([1, 1, 1, 1, 1, 1, 0, 0, 0, 0])
