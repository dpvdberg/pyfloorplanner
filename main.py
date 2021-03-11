import random

from data.Floorplan import Floorplan
from data.TreeBuilder import TreeBuilder
from parsers.YALParser import YALParser

y = YALParser()
modules = y.parse(open('datasets/MCNC/ami33.yal', 'r').read())

TreeBuilder.from_modules(modules, seed=42).print()

fp = Floorplan(modules)

fp.align_horizontally()
fp.plot(draw_names=True)
fp.plot(highlight_empty_space=True)
