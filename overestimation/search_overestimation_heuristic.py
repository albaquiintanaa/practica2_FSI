"""Search (Chapters 3-4)

The way to use this code is to subclass Problem to create a class of problems,
then create problem instances and solve them with calls to the various search
functions."""


import itertools
from utils import *
import random
import sys
import heapq
import time

# ______________________________________________________________________________


class Problem:
    """The abstract class for a formal problem.  You should subclass this and
    implement the method successor, and possibly __init__, goal_test, and
    path_cost. Then you will create instances of your subclass and solve them
    with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def successor(self, state):
        """Given a state, return a sequence of (action, state) pairs reachable
        from this state. If there are many successors, consider an iterator
        that yields the successors one at a time, rather than building them
        all at once. Iterators will work fine within the framework."""
        pass

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Implement this
        method if checking against a single self.goal is not enough."""
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

# ______________________________________________________________________________

class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state.  Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node.  Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        update(self, state=state, parent=parent, action=action,
               path_cost=path_cost, depth=0)
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node %s>" % (self.state,)

    def path(self):
        """Create a list of nodes from the root to this node."""
        x, result = self, [self]
        while x.parent:
            result.append(x.parent)
            x = x.parent
        return result

    def expand(self, problem):
        """Return a list of nodes reachable from this node. [Fig. 3.8]"""
        return [Node(next, self, act,
                     problem.path_cost(self.path_cost, self.state, act, next))
                for (act, next) in problem.successor(self.state)]


# ______________________________________________________________________________
## Uninformed Search algorithms

def graph_search(problem, opened):
    start_time = time.perf_counter()
    """Search through the successors of a problem to find a goal.
    The argument opened should be an empty queue.
    If two paths reach a state, only use the best one. [Fig. 3.18]"""
    closed = []

    generated, visited = 0,0

    opened.append(Node(problem.initial))
    generated += 1 #la raiz cuenta 

    while opened:
        node = opened.pop()
        visited += 1
        if problem.goal_test(node.state):
            total_time = time.perf_counter() - start_time
            return node, generated, visited, node.path_cost, total_time
        if node.state not in closed:
            closed.append(node.state)
            succ = node.expand(problem)
            generated += len(succ)
            opened.extend(succ)
    
    total_time = time.perf_counter() - start_time
    return None, generated, visited, node.path_cost, total_time

def breadth_first_graph_search(problem):
    """Search the shallowest nodes in the search tree first. [p 74]"""
    return graph_search(problem, FIFOQueue())  # FIFOQueue -> opened


def depth_first_graph_search(problem):
    """Search the deepest nodes in the search tree first. [p 74]"""
    return graph_search(problem, Stack())

def branch_and_bound_graph_search(problem):
    """Search the nodes with the lowest path cost first."""
    return graph_search(problem, PriorityQueue())

def branch_and_bound_with_overestimation_graph_search(problem):
    """Search nodes with a bad heuristic"""
    return graph_search(problem, PriorityQueueH(problem))



# _____________________________________________________________________________
# The remainder of this file implements examples for the search algorithms.

# ______________________________________________________________________________
# Graphs and Graph Problems

class Graph:
    """A graph connects nodes (vertices) by edges (links).  Each edge can also
    have a length associated with it.  The constructor call is something like:
        g = Graph({'A': {'B': 1, 'C': 2})
    this makes a graph with 3 nodes, A, B, and C, with an edge of length 1 from
    A to B,  and an edge of length 2 from A to C.  You can also do:
        g = Graph({'A': {'B': 1, 'C': 2}, directed=False)
    This makes an undirected graph, so inverse links are also added. The graph
    stays undirected; if you add more links with g.connect('B', 'C', 3), then
    inverse link is also added.  You can use g.nodes() to get a list of nodes,
    g.get('A') to get a dict of links out of A, and g.get('A', 'B') to get the
    length of the link from A to B.  'Lengths' can actually be any object at
    all, and nodes can be any hashable object."""

    def __init__(self, dict=None, directed=True):
        self.dict = dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()

    def make_undirected(self):
        """Make a digraph into an undirected graph by adding symmetric edges."""
        for a in list(self.dict.keys()):
            for (b, distance) in list(self.dict[a].items()):
                self.connect1(b, a, distance)

    def connect(self, A, B, distance=1):
        """Add a link from A and B of given distance, and also add the inverse
        link if the graph is undirected."""
        self.connect1(A, B, distance)
        if not self.directed: self.connect1(B, A, distance)

    def connect1(self, A, B, distance):
        """Add a link from A to B of given distance, in one direction only."""
        self.dict.setdefault(A, {})[B] = distance

    def get(self, a, b=None):
        """Return a link distance or a dict of {node: distance} entries.
        .get(a,b) returns the distance or None;
        .get(a) returns a dict of {node: distance} entries, possibly {}."""
        links = self.dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    def nodes(self):
        """Return a list of nodes in the graph."""
        return list(self.dict.keys())


def UndirectedGraph(dict=None):
    """Build a Graph where every edge (including future ones) goes both ways."""
    return Graph(dict=dict, directed=False)


def RandomGraph(nodes=list(range(10)), min_links=2, width=400, height=300,
                curvature=lambda: random.uniform(1.1, 1.5)):
    """Construct a random graph, with the specified nodes, and random links.
    The nodes are laid out PESOrandomly on a (width x height) rectangle.
    Then each node is connected to the min_links nearest neighbors.
    Because inverse links are added, some nodes will have more connections.
    The distance between nodes is the hypotenuse times curvature(),
    where curvature() defaults to a random number between 1.1 and 1.5."""
    g = UndirectedGraph()
    g.locations = {}
    ## Build the cities
    for node in nodes:
        g.locations[node] = (random.randrange(width), random.randrange(height))
    ## Build roads from each city to at least min_links nearest neighbors.
    for i in range(min_links):
        for node in nodes:
            if len(g.get(node)) < min_links:
                here = g.locations[node]

                def distance_to_node(n):
                    if n is node or g.get(node, n): return infinity
                    return distance(g.locations[n], here)

                neighbor = argmin(nodes, distance_to_node)
                d = distance(g.locations[neighbor], here) * curvature()
                g.connect(node, neighbor, int(d))
    return g


romania = UndirectedGraph(Dict(
    A=Dict(Z=75, S=140, T=118),
    B=Dict(U=85, P=101, G=90, F=211),
    C=Dict(D=120, R=146, P=138),
    D=Dict(M=75),
    E=Dict(H=86),
    F=Dict(S=99),
    H=Dict(U=98),
    I=Dict(V=92, N=87),
    L=Dict(T=111, M=70),
    O=Dict(Z=71, S=151),
    P=Dict(R=97),
    R=Dict(S=80),
    U=Dict(V=142)))
romania.locations = Dict(
    A=(91, 492), B=(400, 327), C=(253, 288), D=(165, 299),
    E=(562, 293), F=(305, 449), G=(375, 270), H=(534, 350),
    I=(473, 506), L=(165, 379), M=(168, 339), N=(406, 537),
    O=(131, 571), P=(320, 368), R=(233, 410), S=(207, 457),
    T=(94, 410), U=(456, 350), V=(509, 444), Z=(108, 531))

australia = UndirectedGraph(Dict(
    T=Dict(),
    SA=Dict(WA=1, NT=1, Q=1, NSW=1, V=1),
    NT=Dict(WA=1, Q=1),
    NSW=Dict(Q=1, V=1)))
australia.locations = Dict(WA=(120, 24), NT=(135, 20), SA=(135, 30),
                           Q=(145, 20), NSW=(145, 32), T=(145, 42), V=(145, 37))


class GPSProblem(Problem):
    """The problem of searching in a graph from one node to another."""

    def __init__(self, initial, goal, graph):
        Problem.__init__(self, initial, goal)
        self.graph = graph

    def successor(self, A):
        """Return a list of (action, result) pairs."""
        return [(B, B) for B in list(self.graph.get(A).keys())]

    def path_cost(self, cost_so_far, A, action, B):
        return cost_so_far + (self.graph.get(A, B) or infinity)

    def h(self, node):
        """Heuristic function based on an overestimation of the straight-line distance
        to the goal. This heuristic is not admissible and does not guarantee
        optimal solutions.
        """
        if isinstance(node, str):
            state_name = node
        else:
            state_name = node.state
        
        locs = getattr(self.graph, 'locations', None)
        if locs:
            return 4 * int((distance(locs[state_name], locs[self.goal])))
        else:
            return infinity


# =============================================================================
# Data structures for Branching and Bounding

class PriorityQueue:
    """Priority queue ordered by path cost g(n)."""

    def __init__(self):
        """Create an empty priority queue.

        Initializes the internal heap structure and a counter to
        ensure a deterministic order when two elements have the same
        priority.
        """
        self.data = []
        self.counter = itertools.count()

    def append(self, node):
        """Insert a node into the priority queue.

        The node is ordered according to its path cost g(n).

        Args:
            node (Node): The node to be inserted.
        """
        heapq.heappush(self.data, (node.path_cost, next(self.counter), node))

    def pop(self):
        """Remove and return the node with the lowest path cost.
        
        Returns:
            Node: The node with the smallest path cost.
        """

        return heapq.heappop(self.data)[2]

    def extend(self, nodes):
        """Insert a list of nodes into the priority queue.
        
        Args:
            nodes (list[Node]): The nodes to be added.
        """
        for node in nodes:
            self.append(node)

    def __len__(self):
        """Return the number of elements in the priority queue."""
        return len(self.data)


class PriorityQueueH:
    """Priority queue ordered by estimated total cost f(n) = g(n) + h(n)."""

    def __init__(self, problem):
        """Create an empty heuristic-based priority queue.

        Args:
            problem (Problem): The problem instance providing the heuristic
                function h(n).
        """
        self.data = []
        self.problem = problem
        self.counter = itertools.count()

    def append(self, node):
        """Insert a node into the priority queue using f(n).

        The priority is computed as:
            f(n) = g(n) + h(n)

        Args:
            node (Node): The node to be inserted.
        """
        f = node.path_cost + self.problem.h(node)
        heapq.heappush(self.data, (f, next(self.counter), node))

    def pop(self):
        """Remove and return the node with the smallest f(n).

        Returns:
            Node: The node with the smallest estimated total cost.
        """
        return heapq.heappop(self.data)[2]

    def extend(self, nodes):
        """Insert a list of nodes into the priority queue.
        
        Args:
            nodes (list[Node]): The nodes to be added.
        """
        for node in nodes:
            self.append(node)

    def __len__(self):
        """Return the number of elements in the priority queue."""
        return len(self.data)
    
# =============================================================================

