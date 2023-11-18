"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util.priorityQueue import PriorityQueueWithFunction
from pacai.util.queue import Queue
from pacai.util.stack import Stack

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    ```
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    ```
    """

    return _generalTreeSearch(problem, Stack())

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    return _generalTreeSearch(problem, Queue())

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    priorityFunction = lambda node: node[2]
    return _generalTreeSearch(problem, PriorityQueueWithFunction(priorityFunction))

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    priorityFunction = lambda node: node[2] + heuristic(node[0], problem)
    return _generalTreeSearch(problem, PriorityQueueWithFunction(priorityFunction))

def _generalTreeSearch(problem, fringe):
    seenNodes = set()

    startState = problem.startingState()

    fringe.push((startState, [], 0))
    seenNodes.add(startState)

    while (not fringe.isEmpty()):
        state, path, pathCost = fringe.pop()

        if (problem.isGoal(state)):
            return path

        for (successor, action, actionCost) in problem.successorStates(state):
            if (successor in seenNodes):
                continue

            fringe.push((successor, path + [action], pathCost + actionCost))
            seenNodes.add(successor)

    # No path found.
    return None
