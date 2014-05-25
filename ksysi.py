# -*- coding: utf-8 -*-
import argparse
import logging
import sys

import numpy as np
import networkx as nx
import PySide.QtGui as QtGui

from qpath_find.gui.app import TableWindow
from qpath_find.utils import shortest_path, euclidean_distance


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', default=False,
                        action='store_true')
    parser.add_argument('-a', '--algorithm', choices=['dijkstra', 'a_star'],
                        required=True)
    parser.add_argument('-i', '--mapfile', default='simpleMap-1-20x20.txt')
    parser.add_argument('-s', '--source', default='0,10')
    parser.add_argument('-t', '--target', default='15,1')

    return parser.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    src_nodes = np.loadtxt(args.mapfile, dtype=int)
    wall_nodes = map(lambda e: tuple(e),
                     np.transpose(np.nonzero(src_nodes)))

    lattice_width, lattice_height = src_nodes.shape

    lattice = nx.grid_2d_graph(lattice_width, lattice_height)
    lattice.remove_nodes_from(wall_nodes)
    assert len(lattice.nodes()) == (lattice_width * lattice_height - len(wall_nodes))

    source_node = tuple(map(int, args.source.split(',')))
    target_node = tuple(map(int, args.target.split(',')))
    
    path = shortest_path(lattice, source_node, target_node, args.algorithm)
    #print len(path)
    #print path

    #path = nx.astar_path(lattice, source_node, target_node, euclidean_distance)
    #path = nx.dijkstra_path(lattice, source_node, target_node)#, euclidean_distance)
    #print len(path)
    #print 'rrr'
    #print "astar path: ", d_path

    #assert tuple(path) == tuple(d_path)


    logging.debug('path found: %s', repr(path))

    qt_app = QtGui.QApplication(sys.argv)

    widget = TableWindow(_map=src_nodes, path=path)
    
    widget.show()
    widget.raise_()
    sys.exit(qt_app.exec_())


if __name__ == '__main__':
    main()