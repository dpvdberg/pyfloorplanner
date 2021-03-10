import sys
from enum import Enum
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


class ModuleType(Enum):
    HARD = 1
    SOFT = 2
    PREPLACED = 3
    RECTILINEAR = 4


class Module:
    def __init__(self, name: str, module_type: ModuleType, dimensions: Dimensions, position: Vector2):
        self.name = name
        self.module_type = module_type
        self.dimensions = dimensions
        self.position = position

    def __str__(self):
        return "Module: " \
               f"(t={ModuleType(self.module_type).name} x={self.position.x} y={self.position.y} w={self.dimensions.width} h={self.dimensions.height})"


class Floorplan:
    def __init__(self, modules: list[Module]):
        self.modules: list[Module] = modules
        self.aspect_ratio: Interval = self.compute_aspect_ratio_interval()

    def compute_aspect_ratio_interval(self) -> Interval:
        min_ar = sys.float_info.max
        max_ar = sys.float_info.min
        for module in self.modules:
            ar = module.dimensions.height / module.dimensions.width
            min_ar = min(min_ar, ar)
            max_ar = max(max_ar, ar)

        return Interval(min_ar, max_ar)

    def __str__(self):
        return "Floorplan: \n" + "\n".join([str(m) for m in self.modules])