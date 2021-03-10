from dataclasses import dataclass


@dataclass
class Dimensions:
    width: float
    height: float


@dataclass
class Vector2:
    x: float
    y: float

    @staticmethod
    def from_tuple(t: (float, float)):
        return Vector2(t[0], t[1])


@dataclass
class Interval:
    min: float
    max: float
