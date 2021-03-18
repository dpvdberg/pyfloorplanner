import math
import random
from typing import List

from data.Contour import Contour
from data.Floorplan import Floorplan
from data.Module import Module
from data.Tree import Tree
from data.TreeBuilder import TreeBuilder
from matplotlib import pyplot as plt


class SimulatedAnnealing:
    def __init__(self, modules: List[Module], seed=None):
        self.tree = TreeBuilder.random_tree(modules, seed=seed)
        random.seed(seed)

    def sa(self, t: int, iterations: int, initial_temp: float, r: float, temp_t: float, plot=False):
        # TODO: removeSoft is not supported
        operations = [self.tree.rotate, self.tree.move, self.tree.swap]

        norm_area = self.calc_average_area(self.tree, operations)
        current_cost = self.tree.calc_area()/norm_area

        best_tree = self.tree.clone()
        best_area = current_cost*norm_area

        temp = initial_temp

        fig = None
        if plot:
            fig = plt.figure()
            fig.show()

        # Loop until threshold is met
        while self.tree.calc_area() >= t and temp >= temp_t:
            # print("New loop!")
            for i in range(iterations):
                # Perform a random operation
                random.choice(operations)()

                if self.tree.feasible():
                    # TODO: use normalized area instead of total area
                    new_cost = self.tree.calc_area()/norm_area

                    # If the operation generated a better area, keep this as our current solution
                    if new_cost <= current_cost:
                        current_cost = new_cost

                    else:
                        # Else, keep the solution with probability p
                        p = math.e ** (-(new_cost - current_cost) / temp)
                        if random.uniform(0, 1) < p:
                            current_cost = new_cost
                        else:
                            self.tree.revertLast()

                # If this operation is the best we have seen so far, save it
                if current_cost*norm_area < best_area:
                    best_tree = self.tree.clone()
                    best_area = current_cost*norm_area

                    if plot:
                        best_tree.calc_area()
                        Floorplan(best_tree).plot(fig=fig, draw_tree=True)

            # After iterations, reduce temp and continue
            temp = r * temp
        if temp < temp_t:
            print("Stopped due to temperature")
        if self.tree.calc_area() < t:
            print("Stopped due to tree")

        best_tree.calc_area()
        return best_tree

    def calc_average_area(self, tree, operations):
        sum = 0
        for i in range(0,10):
            random.choice(operations)()
            sum += tree.calc_area()
        return sum/10

