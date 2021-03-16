import math
import random
from typing import List

from data.Contour import Contour
from data.Module import Module
from data.Tree import Tree


class SimulatedAnnealing:
    def __init__(self, modules: list[Module]):
        self.tree = Tree.build(modules)

    def sa(self, t: int, iterations: int, initial_temp: int, r: int):
        #TODO: removeSoft is not supported
        operations = [self.tree.rotate, self.tree.move, self.tree.swap]

        current_area = self.calc_area(self.tree)

        best_tree = self.tree.clone()
        best_area = current_area

        temp = initial_temp

        # Loop until threshold is met
        while self.calc_area(self.tree) >= t:
            for i in range(iterations):
                # Perform a random operation
                random.choice(operations)()

                if self.feasible(self.tree):
                    new_area = self.calc_area(self.tree)

                    # If the operation generated a better area, keep this as our current solution
                    if new_area <= current_area:
                        current_area = new_area

                    else:
                        # Else, keep the solution with probability p
                        p = math.e ** (-(new_area - current_area) / initial_temp)
                        if random.uniform(0, 1) < p:
                            current_area = new_area
                        else:
                            self.revertLast(self.tree)

                # If this operation is the best we have seen so far, save it
                if current_area < best_area:
                    best_tree = self.tree.clone()
                    best_area = current_area

            # After iterations, reduce temp and continue
            temp = r * temp
            return best_tree



