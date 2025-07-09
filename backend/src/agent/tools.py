import random
from typing import List


def roll_dice(number_of_dice: int, sides: int) -> List[int]:
    """
    Rolls a specified number of dice, each with a given number of sides.
    For example, to roll "2d6", you would call this with number_of_dice=2 and sides=6.
    """
    if number_of_dice < 1 or sides < 1:
        return []
    return [random.randint(1, sides) for _ in range(number_of_dice)]
