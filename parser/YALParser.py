from dataclasses import dataclass
from lark import Lark
from lark import Transformer
from data.Module import *


# Intermediate module specification class
@dataclass
class ModuleSpec:
    moduleType: ModuleType
    dimensions: Dimensions


class YALTransformer(Transformer):
    def yal(self, yal):
        return Floorplan(yal)

    def module(self, module_elements):
        # Filter none values
        module_elements = [i for i in module_elements if i is not None]
        name = str(module_elements[0])
        spec: ModuleSpec = module_elements[1]
        return Module(name, spec.moduleType, spec.dimensions, Vector2(0, 0))

    def modulespec(self, spec):
        return ModuleSpec(spec[0], spec[1])

    def type(self, _type):
        t = str(_type[0])
        if t == "STANDARD" or t == "GENERAL" or t == "PAD":
            return ModuleType.HARD
        elif t == "PARENT":
            return ModuleType.SOFT

    def dimensions(self, data):
        # Filter none values
        data = [i for i in data if i is not None]
        # Zip into coordinates
        pairs = list(zip(data[::2], data[1::2]))
        vectors = [Vector2.from_tuple(t) for t in pairs]

        if len(vectors) != 4:
            raise Exception("Rectilinear modules not yet supported!")

        return Dimensions(abs(vectors[0].x - vectors[2].x), abs(vectors[0].y - vectors[2].y))

    def SIGNED_NUMBER(self, n):
        return float(n)

    def TERMINATOR(self, t):
        return None


class YALParser:
    def __init__(self):
        self.yal_raw = open('parser/grammar/yal.lark', 'r').read()
        self.yal = Lark(self.yal_raw, start='yal')

    def parse(self, yal):
        return YALTransformer().transform(self.yal.parse(yal))
