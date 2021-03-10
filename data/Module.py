import sys
from enum import Enum
from dataclasses import dataclass

from data.Common import *


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
