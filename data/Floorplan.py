import math

import matplotlib
import numpy as np
from matplotlib.collections import PatchCollection
from typing import List

from data.Module import *
from matplotlib import pyplot as plt, cm
from matplotlib.patches import Rectangle


class Floorplan:
    def __init__(self, modules: List[Module]):
        self.modules: List[Module] = modules
        self.aspect_ratio: Interval = self.compute_aspect_ratio_interval()

    def compute_aspect_ratio_interval(self) -> Interval:
        min_ar = math.inf
        max_ar = -math.inf
        for module in self.modules:
            ar = module.dimensions.height / module.dimensions.width
            min_ar = min(min_ar, ar)
            max_ar = max(max_ar, ar)

        return Interval(min_ar, max_ar)

    def max_dimension(self) -> Dimensions:
        max_x, max_y = 0, 0
        for m in self.modules:
            max_x = max(max_x, m.position.x + m.dimensions.width)
            max_y = max(max_y, m.position.y + m.dimensions.height)

        return Dimensions(max_x, max_y)

    def plot(self, highlight_empty_space=False, draw_names=False, name_size=6):
        fig = plt.figure()
        ax = fig.add_subplot(111, aspect='equal')
        patches = []
        for i, m in enumerate(self.modules):
            r = Rectangle(m.position.to_tuple(), m.dimensions.width, m.dimensions.height)
            patches.append(r)

            if draw_names:
                ax.annotate(m.name, m.position + 0.5 * m.dimensions.to_vector(), color='w', weight='bold',
                            fontsize=name_size, ha='center', va='center')

        md = self.max_dimension()
        plt.xlim([0, md.width])
        plt.ylim([0, md.height])

        pc = PatchCollection(patches, edgecolor='black')

        if highlight_empty_space:
            ax.set_facecolor((1.0, 0.47, 0.42))
        else:
            pc.set_cmap(cm.get_cmap('viridis'))
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
