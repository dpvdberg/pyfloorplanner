import random

from algorithm.SimulatedAnnealing import SimulatedAnnealing
from data.Floorplan import Floorplan
from data.TreeBuilder import TreeBuilder
from parsers.YALParser import YALParser

y = YALParser()
modules = y.parse(open('datasets/MCNC/ami33.yal', 'r').read())

sa = SimulatedAnnealing(modules)
totalArea = sum(i.dimensions.width*i.dimensions.height for i in modules)

best = sa.sa(totalArea, 40, 2, 0.99, 0.0001, plot=True)