import math

import matplotlib
import numpy as np
from matplotlib.collections import PatchCollection

from data.Module import *
from matplotlib import pyplot as plt, cm
from matplotlib.patches import Rectangle


class Floorplan:
    def __init__(self, modules: list[Module]):
        self.modules: list[Module] = modules
        self.aspect_ratio: Interval = self.compute_aspect_ratio_interval()

    def compute_aspect_ratio_interval(self) -> Interval:
        min_ar = math.inf
        max_ar = -math.inf
        for module in self.modules:
            ar = module.dimensions.height / module.dimensions.width
            min_ar = min(min_ar, ar)
            max_ar = max(max_ar, ar)

        return Interval(min_ar, max_ar)

    def max_dimension(self):
        max_dimension = 0
        for m in self.modules:
            max_dimension = max(max_dimension, m.position.x + m.dimensions.width)
            max_dimension = max(max_dimension, m.position.y + m.dimensions.height)

        return max_dimension

    def plot(self, draw_names=False, name_size=6):
        fig = plt.figure()
        ax = fig.add_subplot(111, aspect='equal')
        patches = []
        for i, m in enumerate(self.modules):
            r = Rectangle(m.position.to_tuple(), m.dimensions.width, m.dimensions.height)
            patches.append(r)

            if draw_names:
                ax.annotate(m.name, m.position + 0.5 * m.dimensions.to_vector(), color='w', weight='bold',
                            fontsize=name_size, ha='center', va='center')

        max_dimension = self.max_dimension()
        plt.xlim([0, max_dimension])
        plt.ylim([0, max_dimension])

        pc = PatchCollection(patches, cmap=cm.get_cmap('viridis'), edgecolor='black')
        # assign random values for cmap coloring
        pc.set_array(np.random.random(len(self.modules)))

        ax.add_collection(pc)
        plt.show()

    def align_horizontally(self):
        x = 0
        for m in self.modules:
            m.position.x = x
            x += m.dimensions.width

    def __str__(self):
        return "Floorplan: \n" + "\n".join([str(m) for m in self.modules])
