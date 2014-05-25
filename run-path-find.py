#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import argparse
import sys

import networkx as nx
import numpy as np
import PySide.QtGui as QtGui
from qpath_find.gui.app import TableWindow


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', default=True,
                        action='store_true')
    parser.add_argument('-a', '--algorithm', choices=['dijkstra', 'a*'],
                        required=True)
    parser.add_argument('-i', '--mapfile', default='simpleMap-1-20x20.txt')
    parser.add_argument('-s', '--start', default='0,10')
    parser.add_argument('-t', '--target', default='15,1')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    _map = np.loadtxt(args.mapfile, dtype=int)
    map_rot270 = np.rot90(_map, 3)

    g = nx.grid_2d_graph(*map_rot270.shape)
    g.remove_nodes_from(list(tuple(e) for e in
                             np.transpose(np.nonzero(map_rot270))))
    start_node = tuple(map(int, args.start.split(',')))
    target_node = tuple(map(int, args.target.split(',')))
    print start_node, target_node

    if args.algorithm == 'dijkstra':
        from qpath_find.utils import networkx_dikstra
        path = networkx_dikstra(_map)
        logging.debug('dijkstra algorithm found path: %s', repr(path))
    elif args.algorithm == 'a*':
        raise NotImplemented
    else:
        sys.exit('Invalid algorithm')

    qt_app = QtGui.QApplication(sys.argv)

    widget = TableWindow(_map=_map, path=path)
    
    widget.show()
    widget.raise_()
    sys.exit(qt_app.exec_())
