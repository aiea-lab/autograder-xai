# Style -1 
# Style -1 
# Style -1 
# Style -1 
# Style -1 

"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util.queue import Queue

# Called by search.depthFirstSearch.
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    """

    problem._numExpanded = 100000
    return []

# Called by search.breadthFirstSearch.
def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    problem._numExpanded = 100000
    return ['Stop'] + graphSearch(problem, Queue())

# Called by search.uniformCostSearch.
def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    problem._numExpanded = 100000
    return []

# Called by search.aStarSearch.
def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    problem._numExpanded = 100000
    return []

class Node(object):
    """
    AIMA: A node in a search tree.
    Contains a pointer
    to the parent (the node that this is a successor of)
    and to the actual state for this node. Note that if
    a state is arrived at by two paths, then there are
    two nodes with the same state.  Also includes the
    action that got us to this state, and the total
    path_cost (also known as g) to reach the node.
    Other functions may add an f and h value; see
    best_first_graph_search and astar_search for an
    explanation of how the f and h values are handled.
    You will not need to subclass this class.
    """

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """
        Create a search tree Node, derived from a parent by an action.
        """

        self.state = state
        self.parent = parent
        self.action = action

        if parent:
            self.path_cost = parent.path_cost + path_cost
            self.depth = parent.depth + 1
        else:
            self.path_cost = path_cost
            self.depth = 0

    def __repr__(self):
        return "<Node %s>" % (self.state,)

    def __lt__(self, other):
        """
        Arbitrarily resolve ties using the state.
        """

        return self.state < other.state

    def nodePath(self):
        """
        Create a list of nodes from the root to this node.
        """

        x, result = self, [self]
        while x.parent:
            result.append(x.parent)
            x = x.parent
        result.reverse()
        return result

    def path(self):
        """
        Create a path of actions from the start to the current state
        """

        actions = []
        currnode = self
        while currnode.parent:
            actions.append(currnode.action)
            currnode = currnode.parent
        actions.reverse()
        return actions

    def expand(self, problem):
        """
        Return a list of nodes reachable from this node. [Fig. 3.8]
        """

        return [Node(next, self, act, cost)
                for (next, act, cost) in problem.successorStates(self.state)]

def graphSearch(problem, fringe, reversePush = False):
    """
    Search through the successors of a problem to find a goal.
    The argument fringe should be an empty queue. [Fig. 3.18]
    """

    startstate = problem.startingState()
    fringe.push(Node(problem.startingState()))

    try:
        startstate.__hash__()
        visited = set()
    except Exception:
        visited = list()

    while not fringe.isEmpty():
        node = fringe.pop()
        if problem.isGoal(node.state):
            return node.path()

        try:
            inVisited = node.state in visited
        except Exception:
            visited = list(visited)
            inVisited = node.state in visited

        if not inVisited:
            if isinstance(visited, list):
                visited.append(node.state)
            else:
                visited.add(node.state)

            nextNodes = node.expand(problem)
            if reversePush:
                nextNodes.reverse()

            for nextnode in nextNodes:
                fringe.push(nextnode)

    return None
