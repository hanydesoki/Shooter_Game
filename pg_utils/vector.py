from typing import Union, Iterable
import math


class V2:

    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0):    
        self._values = [x, y]
        self.x = x
        self.y = y

    @property
    def x(self) -> Union[int, float]:
        return self._values[0]
    
    @x.setter
    def x(self, new_value: Union[int, float]):
        if not isinstance(new_value, (int, float)):
            raise TypeError(f"x value should be int or float. Got {new_value} ({type(new_value).__name__}) instead")
        
        self._values[0] = new_value
        
    @property
    def y(self) -> Union[int, float]:
        return self._values[1]
    
    @y.setter
    def y(self, new_value: Union[int, float]):
        if not isinstance(new_value, (int, float)):
            raise TypeError(f"y value should be int or float. Got {new_value} ({type(new_value).__name__}) instead")
        
        self._values[1] = new_value

    def distance(self, other: "V2") -> float:
        if not isinstance(other, V2):
            raise TypeError(f"Cannot compute distance with an object that is not a V2 object. Got {other} instead.")
        
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def dot_product(self, other: "V2") -> float:
        if not isinstance(other, V2):
            raise TypeError(f"V2 object can only do the dot product with an other V2 object. Got {other} instead.")
        
        return self.x * other.x + self.y * other.y
    
    def angle(self, other: "V2") -> float:
        if not isinstance(other, V2):
            raise TypeError(f"V2 object can only compute angle with an other V2 object. Got {other} instead.")
        
        return math.acos(self.dot_product(other) / (self.magnitude * other.magnitude))
    
    @property
    def unit(self) -> "V2":
        return self / self.magnitude

    def _operate(self, other: Iterable, operator: str) -> "V2":
        if isinstance(other, (int, float)):
            return eval(f"V2({self.x} {operator} {other}, {self.y} {operator} {other})")
        
        other = list(other)

        if len(other) != 2:
            raise ValueError("Cannot operate on a V2 object with an iterable of len != 2")
        
        if not all(map(lambda v: isinstance(v, (int, float)), other)):
            raise TypeError("Cannot operate on a V2 object with an iterable values that are not int or float")
        
        return eval(f"V2({self.x} {operator} {other[0]}, {self.y} {operator} {other[1]})")

    def __add__(self, other: Iterable) -> "V2":
        return self._operate(other, "+")
    
    def __sub__(self, other: Iterable) -> "V2":
        return self._operate(other, "-")
    
    def __truediv__(self, other: Iterable) -> "V2":
        return self._operate(other, "/")
    
    def __floordiv__(self, other: Iterable) -> "V2":
        return self._operate(other, "//")
    
    def __mul__(self, other: Iterable) -> "V2":
        return self._operate(other, "*")

    def __iter__(self) -> Iterable:
        yield self.x
        yield self.y

    def __getitem__(self, index: int) -> Union[int, float]:
        return self._values[index]
    
    def __setitem__(self, index: int, new_value: Union[int, float]) -> None:
        if index not in [0, 1]:
            raise IndexError(f"Index should be 0 or 1. Got {index} instead.")
        
        if index == 0:
            self.x = new_value
        else:
            self.y = new_value
        
        
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.x}, {self.y})"
    

if __name__ == "__main__":
    pos1 = V2(1, 2)
    pos2 = V2(5, 8)

    print(pos1)
    pos1.x += 4
    print(pos1 + 1)
    print(pos1 - (2, 5))
    print(pos1 / 2)
    print(pos1 // 2)
    print(pos1 * pos2)
    print(pos1.distance(pos2))
    print(pos1.angle(pos2))
    print(pos2.unit)
    print(list(pos1), tuple(pos1))
    