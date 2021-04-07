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
    def __init__(self, tree: Tree):
        self.tree = tree
        self.modules: List[Module] = [x.value for x in self.tree.root.nodes_in_subtree()]

    def max_dimension(self) -> Dimensions:
        return Dimensions(self.tree.hor_cont.get_max_x(), self.tree.hor_cont.get_max_y())

    def plot(self, fig=None, highlight_empty_space=False, draw_names=False, name_size=6, draw_tree=False,
             tree_edge_color='k', tree_node_color='#1f78b4', tree_node_size=150, tree_label_font_size=10,
             tree_line_width=1.0, draw_contour=False, draw_contour_marker=True, contour_marker_color='cyan',
             contour_style='r', contour_width=3, plot_order=None):
        if fig is None:
            f = plt.figure()
            ax = f.add_subplot(111)
        else:
            f = fig
            ax = plt.gca()
            ax.clear()

        ax.set_aspect('equal')
        patches = []

        for i, n in enumerate(self.tree.nodes):
            m = n.value
            if n.rotated:
                r = Rectangle(m.position.to_tuple(), m.dimensions.height, m.dimensions.width)
            else:
                r = Rectangle(m.position.to_tuple(), m.dimensions.width, m.dimensions.height)
            patches.append(r)

            if draw_names:
                ax.annotate(m.name, m.position + 0.5 * m.dimensions.to_vector(), color='w', weight='bold',
                            fontsize=name_size, ha='center', va='center')

        if draw_contour:
            contour = self.tree.hor_cont
            contour_x = [p.x for p in list(contour)[:-1]]
            contour_y = [p.y for p in list(contour)[:-1]]
            plt.plot(contour_x, contour_y, contour_style, linewidth=contour_width,
                     marker=('o' if draw_contour_marker else ''), markerfacecolor=contour_marker_color)

        if draw_tree:
            network, positions = self.tree.to_networkx()
            nx.draw_networkx(network, positions, arrows=True,
                             edge_color=tree_edge_color, node_color=tree_node_color,
                             font_size=tree_label_font_size,
                             node_size=tree_node_size, linewidths=tree_line_width)

        md = self.max_dimension()
        if not draw_contour:
            plt.xlim([0, md.width])
            plt.ylim([0, md.height])
        else:
            plt.xlim([-2 * contour_width, md.width + 2 * contour_width])
            plt.ylim([-2 * contour_width, md.height + 2 * contour_width])

        pc = PatchCollection(patches, edgecolor='black')

        if highlight_empty_space:
            ax.set_facecolor((1.0, 0.47, 0.42))
        else:
            pc.set_cmap(cm.get_cmap('viridis'))
            # assign random values for cmap coloring
            if plot_order is None:
                plot_order = np.random.random(len(self.modules))
            pc.set_array(plot_order)

        ax.add_collection(pc)

        if fig is None:
            f.show()
        else:
            f.canvas.draw()

    def align_horizontally(self):
        x = 0
        for m in self.modules:
            m.position.x = x
            x += m.dimensions.width

    def __str__(self):
        return "Floorplan: \n" + "\n".join([str(m) for m in self.modules])
