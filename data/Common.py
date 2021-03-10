from dataclasses import dataclass


@dataclass
class Vector2:
    x: float
    y: float

    @staticmethod
    def from_tuple(t: (float, float)):
        return Vector2(t[0], t[1])

    def to_tuple(self) -> (float, float):
        return self.x, self.y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)
        else:
            raise ValueError("Multiplication with type {} not supported".format(type(other)))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector2(self.x / other, self.y / other)
        else:
            raise ValueError("Division with type {} not supported".format(type(other)))

    def __iter__(self):
        return iter([self.x, self.y])


@dataclass
class Dimensions:
    width: float
    height: float

    def to_vector(self) -> Vector2:
        return Vector2(self.width, self.height)


@dataclass
class Interval:
    min: float
    max: float
