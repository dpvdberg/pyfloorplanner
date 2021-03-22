import random

from algorithm.SimulatedAnnealing import SimulatedAnnealing
from data.Floorplan import Floorplan
from data.TreeBuilder import TreeBuilder
from parsers.YALParser import YALParser
from data.Module import ModuleType

y = YALParser()
modules = y.parse(open('datasets/MCNC/ami49.yal', 'r').read())
modules = [module for module in modules if module.module_type is not ModuleType.SOFT]

sa = SimulatedAnnealing(modules)
totalArea = sum(i.dimensions.width*i.dimensions.height for i in modules)

best = sa.sa(totalArea, 400, 1, 0.9, 0.1, plot_intermediate=True)

best.print()
fp = Floorplan(best)
print(best.calc_area())
fp.plot(draw_tree=True, draw_contour=True)