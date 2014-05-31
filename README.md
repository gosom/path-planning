path-planning
=============

Dijkstra and A* implementation to compute shortest paths.

For representing the graphs it is used the networkx library.

### Dependencies

python

networkx

numpy

pyside


### How to run

Run `python run-path-find.py -h` to see help

Example:

`python run-path-find.py dijkstra -i simpleMap-1-20x20.txt -s '0,10' -t '15,1'`


`python run-path-find.py a_star -i simpleMap-1-20x20.txt -s '0,10' -t '15,1'`


If you want to run the networkx implementation for an algorithm use the --nx option.

