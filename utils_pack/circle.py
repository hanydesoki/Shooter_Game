if __name__ == "__main__":
    from descriptor import NumberAttribute
else:
    from .descriptor import NumberAttribute


class Circle:

    x = NumberAttribute()
    y = NumberAttribute()
    radius = NumberAttribute(extra_checks=[[lambda x: x >= 0, "should be positive"]])

    def __init__(self, x: float, y: float, radius: float):
        self._x = x
        self._y = y
        self._radius = radius

    def collide_point(self, point: tuple[float, float]) -> bool:
        return self.squared_distance(self.center, point) <= self.radius ** 2
    
    def collide_circle(self, other: "Circle") -> bool:
        return self.squared_distance(self.center, other.center) <= (self.radius + other.radius) ** 2

    @property
    def center(self) -> tuple[float, float]:
        return self.x, self.y
    
    @center.setter
    def center(self, position: tuple[float, float]) -> None:
        self.x, self.y = position

    @staticmethod
    def squared_distance(point1: tuple[int, int], point2: tuple[int, int]) -> float:
        return (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2

    def __repr__(self):
        return f"Circle(x={self.x}, y={self.y}, radius={self.radius})"


if __name__ == "__main__":

    c1 = Circle(x=12, y=20, radius=10)
    c2 = Circle(x=0, y=0, radius=40)
    
    c1.center = (7, 1)
    c1.radius = 5

    print(c1, c2)
    print(c1.x)

    print(c1.collide_point((15, 16)))
    print(c1.collide_circle(c2))