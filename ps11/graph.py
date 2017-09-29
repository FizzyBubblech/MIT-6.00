# 6.00 Problem Set 11
# A set of data structures to represent graphs
# Denis Savenkov
# graph.py


import pylab

# Problem 1
class Node(object):
   def __init__(self, name):
       self.name = str(name)
       
   def getName(self):
       return self.name
      
   def __str__(self):
       return self.name
      
   def __repr__(self):
      return self.name
   
   def __eq__(self, other):
      return self.name == other.name
   
   def __ne__(self, other):
      return not self.__eq__(other)

class Edge(object):
   def __init__(self, src, dest):
       self.src = src
       self.dest = dest
       
   def getSource(self):
       return self.src
      
   def getDestination(self):
       return self.dest
      
   def __str__(self):
       return str(self.src) + ' -> ' + str(self.dest)

# MY CODE
class WeightedEdge(Edge):
   def __init__(self, src, dest, weight = 1):
      Edge.__init__(self, src, dest)
      self.weight = weight
      
   def getWeight(self):
      return self.weight
   
   def __str__(self):
      return str(self.src) + '->' + str(self.dest)\
             + '(' + str(self.weight) + ')'

class Digraph(object):
   """
   A directed graph
   """
   def __init__(self):
       self.nodes = []
       self.edges = {}
       
   def addNode(self, node):
       if node in self.nodes:
           raise ValueError('Duplicate node')
       else:
           self.nodes.append(node)
           self.edges[node] = []
           
   def addEdge(self, edge):
       src = edge.getSource()
       dest = edge.getDestination()
       if not(src in self.nodes and dest in self.nodes):
           raise ValueError('Node not in graph')
       self.edges[src].append(dest)
       
   def childrenOf(self, node):
       return self.edges[node]
      
   def hasNode(self, node):
       return node in self.nodes
      
   def __str__(self):
       res = ''
       for k in self.edges:
           for d in self.edges[k]:
               res = res + str(k) + ' -> ' + str(d) + '\n'
       return res[:-1]

# MY CODE
class WeightedDigraph(Digraph):
   def __init__(self):
      Digraph.__init__(self)

   def addEdge(self, edge):
      src = edge.getSource()
      dest = edge.getDestination()
      if not(src in self.nodes and dest in self.nodes):
         raise ValueError('Node not in graph')
      self.edges[src].append(edge)
      
   def numNodes(self):
      return len(self.nodes)

   def childrenOf(self, node):
      result = []
      for e in self.edges[node]:
         if not e.getDestination() in result:
            result.append(e.getDestination())
      return result

   def edgesOf(self, node):
      result = []
      for e in self.edges[node]:
         result.append(e)
      return result

   def getWeight(self, src, dest):
      return self.weights[(src, dest)]
      
   def __str__(self):
      res = ''
      for k in self.edges:
        for e in self.edges[k]:
           res = res + str(e) + '\n'
      
      return res[:-1]

class Path(object):
   def __init__(self, start):
      assert type(start) == Node
      self.val = [(start, (0.0, 0.0))]

   def addStep(self, edge):
      if self.val[-1][0] != edge.getSource():
         raise ValueError('Not a continuation of path')
      self.val.append((edge.getDestination(), edge.getWeight()))

   def getStart(self):
      return self.val[0][0]

   def getWeight(self):
      result = pylab.array((0.0, 0.0))
      for step in self.val:
         result += pylab.array(step[1])
      return tuple(result)

   def getLength(self):
      return len(self.val) - 1

   def getList(self):
      result = []
      for item in self.val:
         result.append(item[0].getName())
      return result

   def addPath(self, other):
      result = Path(self.getStart())
      for elem in self.val[1:]:
         result.val.append(elem)
      result.val.extend(other.val)
      return result

   def __add__(self, edge):
      result = Path(self.getStart())
      for elem in self.val[1:]:
         result.val.append(elem)
      result.val.append((edge.getDestination(), edge.getWeight()))
      return result

   def contains(self, node):
      for step in self.val:
         if step[0] == node:
            return True
      return False

   def __str__(self):
      result = ''
      for step in self.val:
         result = result + '->' + str(step[0])
      return result[2:]
