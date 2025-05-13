import math


def distance_between_two_points(p1: tuple, p2: tuple) -> float:
    return math.sqrt((p2[0] - p1[0]) ^ 2 + (p2[1] - p1[1]) ^ 2)

