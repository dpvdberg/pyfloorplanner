import math

import matplotlib
import numpy as np
import networkx as nx
from matplotlib.collections import PatchCollection
from typing import List

from data.Module import *
from matplotlib import pyplot as plt, cm
from matplotlib.patches import Rectangle

from data.Tree import Tree


class Floorplan:
    def __init__(self, arg):
        if isinstance(arg, list):
            self.tree = None
            self.modules: List[Module] = arg
        elif isinstance(arg, Tree):
            self.tree = arg
            self.modules: List[Module] = [x.value for x in self.tree.root.nodes_in_subtree()]

    def max_dimension(self) -> Dimensions:
        max_x, max_y = 0, 0
        for m in self.modules:
            max_x = max(max_x, m.position.x + m.dimensions.width)
            max_y = max(max_y, m.position.y + m.dimensions.height)

        return Dimensions(max_x, max_y)

    def plot(self, highlight_empty_space=False, draw_names=False, name_size=6,
             draw_tree=False, tree_edge_color='k', tree_node_color='#1f78b4', tree_node_size=300, tree_line_width=1.0,
             draw_contour=False, contour_style='r', contour_width=3):
        fig = plt.figure()
        ax = fig.add_subplot(111, aspect='equal')
        patches = []
        for i, m in enumerate(self.modules):
            r = Rectangle(m.position.to_tuple(), m.dimensions.width, m.dimensions.height)
            patches.append(r)

            if draw_names:
                ax.annotate(m.name, m.position + 0.5 * m.dimensions.to_vector(), color='w', weight='bold',
                            fontsize=name_size, ha='center', va='center')

        if self.tree:
            if draw_contour:
                contour = self.tree.hor_cont
                contour_x = [p.x for p in list(contour)[:-1]]
                contour_y = [p.y for p in list(contour)[:-1]]
                plt.plot(contour_x, contour_y, contour_style, linewidth=contour_width)

            if draw_tree:
                network, positions = self.tree.to_networkx()
                nx.draw_networkx(network, positions, arrows=True,
                                 edge_color=tree_edge_color, node_color=tree_node_color,
                                 node_size=tree_node_size, linewidths=tree_line_width)


        md = self.max_dimension()
        if not draw_contour:
            plt.xlim([0, md.width])
            plt.ylim([0, md.height])
        else:
            plt.xlim([-contour_width, md.width+contour_width])
            plt.ylim([-contour_width, md.height+contour_width])

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
