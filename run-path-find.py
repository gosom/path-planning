# -*- coding: utf-8 -*-
import argparse
import logging
import sys
from copy import deepcopy

import numpy as np
import networkx as nx
import PySide.QtGui as QtGui

from qpath_find.gui.app import TableWindow
from qpath_find.utils import shortest_path, euclidean_distance


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', default=False,
                        action='store_true', help='Use for more verbose output'
                        ' DEFAULT disabled')
    parser.add_argument('algorithm', choices=['dijkstra', 'a_star'],
                        help='Choose the algorithm to use'
                        '(dijkstra or a_star)')
    parser.add_argument('-i', '--mapfile', default='simpleMap-1-20x20.txt',
                        help='Specify the filename for input DEFAULT simpleMap-1-20x20.txt')
    parser.add_argument('-s', '--source', default='0,10', help='Give the start node as a'
                        ' a string "x,y" DEFAULT "0,10"')
    parser.add_argument('-t', '--target', default='15,1', help='Give the target node as a'
                        ' a string "x, y" DEFAULT "15,1"')
    parser.add_argument('-r', '--rotated', default=1, type=int, help='Give 0 if you do not '
                        'want to rotate the input narray but modify the coordinates '
                        'DEFAULT 1')
    parser.add_argument('--nx', action='store_true', default=False, help='Use in order to '
                        ' to utilize the networkx implementation of the algorithms DEFAULT False')

    return parser.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    src_nodes = np.loadtxt(args.mapfile, dtype=int)
    rotated = bool(args.rotated)
    if rotated:
        working_array = np.rot90(src_nodes, 3)
    else:
        working_array = deepcopy(src_nodes)

    wall_nodes = map(lambda e: tuple(e),
                     np.transpose(np.nonzero(working_array)))

    lattice_width, lattice_height = src_nodes.shape

    lattice = nx.grid_2d_graph(lattice_width, lattice_height)
    lattice.remove_nodes_from(wall_nodes)
    assert len(lattice.nodes()) == (lattice_width * lattice_height - len(wall_nodes))

    input_source_node = tuple(map(int, args.source.split(',')))
    input_target_node = tuple(map(int, args.target.split(',')))

    #source_node, target_node = input_source_node, input_target_node
    if not rotated:
        source_node = (lattice_height - 1 - input_source_node[1], input_source_node[0])
        target_node = (lattice_height -1 - input_target_node[1], input_target_node[0])
    else:
        source_node, target_node = input_source_node, input_target_node
    
    if not args.nx:
        path = shortest_path(lattice, source_node, target_node, args.algorithm)
    else:
        if args.algorithm == 'dijkstra':
            print 'eee'
            path = nx.dijkstra_path(lattice, source_node, target_node)
        else:
            path = nx.astar_path(lattice, source_node, target_node, euclidean_distance)

    logging.debug('path found: %s', repr(path))

    qt_app = QtGui.QApplication(sys.argv)

    widget = TableWindow(_map=src_nodes, path=path,
        rotated=args.rotated)
    
    widget.show()
    widget.raise_()
    sys.exit(qt_app.exec_())


if __name__ == '__main__':
    main()