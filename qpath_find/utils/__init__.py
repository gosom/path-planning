# -*- coding: utf-8 -*-
import logging
from collections import deque
from heapq import heappush, heappop

import networkx as nx


INF = float('inf')
logger = logging.getLogger('utils')


def shortest_path(g, s, t, algorithm='dijkstra'):
    assert algorithm in ('dijkstra', 'a_star')
    f = a_star if algorithm == 'a_star' else dijkstra
    parents = f(g, s, t)
    path = deque([])
    while t in parents:
        path.appendleft(t)
        t = parents[t]
    if algorithm == 'dijkstra':
        path.appendleft(s)
    return path


def dijkstra(g, s, t):
    logger.debug('Starting dijkstra...')
    fringe, closed = [(0, s)], set()
    distances, parents = {s: 0}, {}
    while fringe:
        _, u = heappop(fringe)
        if u not in closed:
            closed.add(u)
            if u == t: break
            for v in nx.all_neighbors(g, u):
                d = distances.get(u, INF) + 1
                if d < distances.get(v, INF):
                    distances[v] = d
                    parents[v] = u
                heappush(fringe, (distances[v], v))
    return parents


def euclidean_distance(a, b):
    x1, y1 = a
    x2, y2 = b
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def a_star(g, s, t, h=euclidean_distance):
    logger.debug('Starting a_star...')
    fringe = [(h(s, t), s, None)]
    parents = {}
    while fringe:
        d, u, p = heappop(fringe)
        if u not in parents:
            parents[u] = p
            if u == t: break
            for v in nx.all_neighbors(g, u):
                if v in parents:continue
                d =  d + h(v, t)
                heappush(fringe, (d, v, u))
    return parents