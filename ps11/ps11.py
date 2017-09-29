# 6.00 Problem Set 11
# Graph optimization
# Finding shortest paths through MIT buildings
# Denis Savenkov
# ps11.py


import string
import pylab
from graph import *

#
# Problem 2: Building up the Campus Map
#
# Write a couple of sentences describing how you will model the
# problem as a graph)
#
# The graph represents a campus map. Nodes are the buildings, Edges are
# the routes between the buildings. Edges are weighted to represent
# overall distance between buildings and distance spent outside.

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    # MY CODE
    print "Loading map from file..."

    campusMap = WeightedDigraph()
    
    f = open(mapFilename, 'r')
    for line in f:
        l = line.split()
        node1 = Node(l[0])
        node2 = Node(l[1])
        weight = (int(l[2]), int(l[3]))
        
        try:
            campusMap.addNode(node1)
        except ValueError:
            for node in campusMap.nodes:
                if node1 == node:
                    node1 = node

        try:
            campusMap.addNode(node2)
        except ValueError:
            for node in campusMap.nodes:
                if node2 == node:
                    node2 = node

        
        campusMap.addEdge(WeightedEdge(node1, node2, weight))
        
    return campusMap
        
#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and the constraints
#
# Objective function is minimum distance from "start" building to "end"
# building. Constraints -  maximum total distance traveled and maximum
# distance traveled outdoors.

def findNode(graph, name):
    for node in graph.nodes:
        if node.getName() == name:
            return node

def minWeightPath(graph, start, end, maxTotalDist, maxDistOutdoors, path = None, edge = None):
    if not (graph.hasNode(start) and graph.hasNode(end)):
        raise ValueError('Start or end not in graph.')
    if path == None:
        path = Path(start)
    else:
        path = path + edge
    if start == end:
        return path
    shortest = None
    for edge in graph.edgesOf(start):
        if not path.contains(edge.getDestination()):
            newPath = minWeightPath(graph, edge.getDestination(),
                                    end, maxTotalDist, maxDistOutdoors, path, edge)
            if newPath != None:
                if shortest == None or newPath.getWeight()[0] < shortest.getWeight()[0]:
                    if newPath.getWeight()[0] <= maxTotalDist and\
                       newPath.getWeight()[1] <= maxDistOutdoors:
                        shortest = newPath
    return shortest

def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    # MY CODE
    startNode = findNode(digraph, start)
    endNode = findNode(digraph, end)
    path = minWeightPath(digraph, startNode, endNode, maxTotalDist, maxDistOutdoors)
    if path == None:
        raise ValueError('Exceeds constraints')
    distance = path.getWeight()
    if distance[0] <= maxTotalDist and distance[1] <= maxDistOutdoors:
        return path.getList()
    else:
        raise ValueError('Exceeds constraints')

    
#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
# TODO
def opMinWeightPath(graph, start, end, maxTotalDist, maxDistOutdoors, path = None, edge = None, memo = {}):
    if not (graph.hasNode(start) and graph.hasNode(end)):
        raise ValueError('Start or end not in graph.')
    if path == None:
        path = Path(start)
    else:
        path = path + edge
    if start == end:
        return path
    shortest = None
    for edge in graph.edgesOf(start):
        if not path.contains(edge.getDestination()):
            try:
                newPath = memo[edge.getDestination(), end]
            except:
                newPath = opMinWeightPath(graph, edge.getDestination(), end,
                                          maxTotalDist, maxDistOutdoors, path, edge, memo)
            if newPath != None:
                if shortest == None or newPath.getWeight()[0] < shortest.getWeight()[0]:
                    if newPath.getWeight()[0] <= maxTotalDist and\
                       newPath.getWeight()[1] <= maxDistOutdoors:
                        shortest = newPath
                        memo[edge.getDestination(), end] = newPath
    return shortest

def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    #TODO 
    startNode = findNode(digraph, start)
    endNode = findNode(digraph, end)
    path = opMinWeightPath(digraph, startNode, endNode, maxTotalDist, maxDistOutdoors)
    if path == None:
        return "exceeds constraints"
        #raise ValueError('Exceeds constraints')
    distance = path.getWeight()
    if distance[0] <= maxTotalDist and distance[1] <= maxDistOutdoors:
        return path.getList()
    else:
        return "exceeds constraints"
        #raise ValueError('Exceeds constraints')




