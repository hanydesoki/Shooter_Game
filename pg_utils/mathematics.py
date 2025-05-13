import math
from typing import Callable, Generator


def distance_between_two_points(p1: tuple, p2: tuple) -> float:
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def clamp_values(b1: float, b2: float, value: float) -> float:
    boundaries = sorted((b1, b2))

    return max(boundaries[0], min(boundaries[1], value))


class Mapper:
    
    def __init__(self, input_start: float, input_end: float, output_start: float, output_end: float):
        self.input_start = input_start
        self.input_end = input_end

        if output_start == output_end:
            raise ValueError("output_start and output_end cannot be the same values.")

        self.output_start = output_start
        self.output_end = output_end

    def __call__(self, input_value: float, clamp: bool = False) -> float:
        ratio_input = (input_value - self.input_start) / (self.input_end - self.input_start)

        result = self.output_start + ratio_input * (self.output_end - self.output_start)

        if clamp:
            return clamp_values(self.output_start, self.output_end, result)

        return result
    

def iterate(start: float, condition: Callable, increment: Callable) -> Generator:
    current_value = start
    while condition(current_value):
        yield current_value
        current_value = increment(current_value)


if __name__ == "__main__":
    dist_speed_mapper = Mapper(10, 4, 15, 40)

    for dist in iterate(10, lambda i: i >= 4, lambda i: i - 0.02):
        print(f"dist: {dist} -> {dist_speed_mapper(dist)}")