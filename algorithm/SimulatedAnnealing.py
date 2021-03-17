import math
import random
from typing import List

from data.Contour import Contour
from data.Module import Module
from data.Tree import Tree
from data.TreeBuilder import TreeBuilder


class SimulatedAnnealing:
    def __init__(self, modules: List[Module], seed=None):
        self.tree = TreeBuilder.random_tree(modules, seed=seed)
        random.seed(seed)

    def sa(self, t: int, iterations: int, initial_temp: float, r: float, temp_t: float):
        # TODO: removeSoft is not supported
        operations = [self.tree.rotate, self.tree.move, self.tree.swap]

        current_area = self.tree.calc_area()

        best_tree = self.tree.clone()
        best_area = current_area

        temp = initial_temp

        # Loop until threshold is met

        while self.tree.calc_area() >= t and temp >= temp_t:
            for i in range(iterations):
                # Perform a random operation
                random.choice(operations)()

                if self.tree.feasible():
                    # TODO: use normalized area instead of total area
                    new_area = self.tree.calc_area()

                    # If the operation generated a better area, keep this as our current solution
                    if new_area <= current_area:
                        current_area = new_area

                    else:
                        # Else, keep the solution with probability p
                        p = math.e ** (-(new_area - current_area) / initial_temp)
                        if random.uniform(0, 1) < p:
                            current_area = new_area
                        else:
                            self.tree.revertLast()

                # If this operation is the best we have seen so far, save it
                if current_area < best_area:
                    best_tree = self.tree.clone()
                    best_area = current_area

            # After iterations, reduce temp and continue
            temp = r * temp
            return best_tree
