import math


def get_direction(from_pos: tuple[float, float], to_pos: tuple[float, float]) -> tuple[float]:
    
    x_diff = to_pos[0] - from_pos[0]
    y_diff = to_pos[1] - from_pos[1]

    norm = math.sqrt(pow(x_diff, 2) + pow(y_diff, 2))

    if norm == 0:
        return 0, 0

    x = x_diff / norm
    y = y_diff / norm

    return x, y