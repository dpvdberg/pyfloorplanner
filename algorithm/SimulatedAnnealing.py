import math
import random
from typing import List

from data.Contour import Contour
from data.Floorplan import Floorplan
from data.Module import Module
from data.Tree import Tree
from data.TreeBuilder import TreeBuilder
from matplotlib import pyplot as plt
import statistics


class SimulatedAnnealing:
    def __init__(self, modules: List[Module], seed=None):
        self.tree = TreeBuilder.random_tree(modules, seed=seed)
        #self.tree = TreeBuilder.notrandom_tree(modules)
        random.seed(seed)

    def sa(self, iterations: int, initial_temp: float, stop_temp: float, stop_area: int, plot_intermediate=False):
        # TODO: removeSoft is not supported
        operations = [self.tree.rotate, self.tree.move, self.tree.swap]

        current_area = self.tree.calc_area()
        norm_area = self.calc_average_area(self.tree, operations)
        #norm_area = 1;
        current_cost = current_area/norm_area

        best_tree = self.tree.clone()
        best_area = current_cost*norm_area

        itr = iterations * len(self.tree.nodes)

        temp = 0.00001 / math.log(0.9)
        actual_temp = initial_temp

        estimate_avg = 0.08 / 150
        count = 0

        fig = None
        if plot_intermediate:
            fig = plt.figure()
            fig.show()

        # Loop until threshold is met
        while current_area >= stop_area and actual_temp >= stop_temp:
            # print("New loop!")
            count += 1
            deltas = []
            for i in range(itr):
                # Perform a random operation
                save_tree = self.tree.clone()
                if 0.3 > random.uniform(0, 1):
                    self.tree.rotate()
                elif 0.5 > random.uniform(0, 1):
                    self.tree.swap()
                else:
                    self.tree.move()
                    #Floorplan(self.tree).plot(fig=fig, draw_tree=True)

                if self.tree.feasible():
                    new_area = self.tree.calc_area()
                    new_cost = new_area/norm_area

                    delta = new_cost - current_cost
                    deltas.append(delta)

                    # If the operation generated a better area, keep this as our current solution
                    if new_cost <= current_cost:
                        current_area = new_area
                        current_cost = new_cost

                    else:
                        # Else, keep the solution with probability p
                        p = math.e ** (delta / temp)
                        #print('delta =  ', delta, 'p = ', p)
                        if random.uniform(0, 1) < p:
                            current_area = new_area
                            current_cost = new_cost
                        else:
                            # self.tree.revertLast()
                            self.tree = save_tree

                # If this operation is the best we have seen so far, save it
                if current_cost*norm_area < best_area:
                    best_tree = self.tree.clone()
                    best_area = current_cost*norm_area
                    print(best_area)

                    if plot_intermediate:
                        Floorplan(self.tree).plot(fig=fig, draw_tree=True)

            # After iterations, reduce temp and continue
            std_var = statistics.stdev(deltas)
            ratio = math.e ** (1.3 * temp / std_var)
            temp = ratio * temp
            # print(temp)

            if count == 7:
                temp = estimate_avg / math.log(0.9)
                temp *= pow(0.9, 7)
                actual_temp = math.e ** (estimate_avg / temp)

            if count > 7:
                actual_temp = math.e ** (estimate_avg / temp)

            print(actual_temp)

        if actual_temp < stop_temp:
            print("Stopped due to temperature")
        if self.tree.calc_area() < stop_area:
            print("Stopped due to tree")

        best_tree.calc_area()
        return best_tree

    def calc_average_area(self, tree, operations):
        sum = 0
        for i in range(0,10):
            random.choice(operations)()
            sum += tree.calc_area()
        return sum/10

