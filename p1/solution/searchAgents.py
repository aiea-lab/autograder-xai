"""
This file contains incomplete versions of some agents that can be selected to control Pacman.
You will complete their implementations.

Good luck and happy searching!
"""

import logging

from pacai.core import distance
from pacai.core.actions import Actions
from pacai.core.directions import Directions
from pacai.core.search import search
from pacai.core.search.position import PositionSearchProblem
from pacai.core.search.problem import SearchProblem
from pacai.agents.base import BaseAgent
from pacai.agents.search.base import SearchAgent

class CornersProblem(SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function.
    See the `pacai.core.search.position.PositionSearchProblem` class for an example of
    a working SearchProblem.

    Additional methods to implement:

    `pacai.core.search.problem.SearchProblem.startingState`:
    Returns the start state (in your search space,
    NOT a `pacai.core.gamestate.AbstractGameState`).

    `pacai.core.search.problem.SearchProblem.isGoal`:
    Returns whether this search state is a goal state of the problem.

    `pacai.core.search.problem.SearchProblem.successorStates`:
    Returns successor states, the actions they require, and a cost of 1.
    The following code snippet may prove useful:
    ```
        successors = []

        for action in Directions.CARDINAL:
            x, y = currentPosition
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]

            if (not hitsWall):
                # Construct the successor.

        return successors
    ```
    """

    def __init__(self, startingGameState):
        super().__init__()

        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top = self.walls.getHeight() - 2
        right = self.walls.getWidth() - 2

        self.corners = ((1, 1), (1, top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                logging.warning('Warning: no food in corner ' + str(corner))

    def actionsCost(self, actions):
        """
        Returns the cost of a particular sequence of actions.
        If those actions include an illegal move, return 999999.
        This is implemented for you.
        """

        if (actions is None):
            return 999999

        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999

        return len(actions)

    # Override
    def isGoal(self, state):
        # We are done if all four corners have been touched.
        for visitedCorner in state[1]:
            if (not visitedCorner):
                return False

        return True

    # Override
    def startingState(self):
        # Our state will be the agents position of the four corners the agent has touched.
        visitedCorners = tuple(False for corner in self.corners)
        return (self.startingPosition, visitedCorners)

    # Override
    def successorStates(self, state):
        successors = []
        self._numExpanded += 1

        for action in Directions.CARDINAL:
            (x, y), oldCorners = state
            dx, dy = Actions.directionToVector(action)
            nextX, nextY = int(x + dx), int(y + dy)

            if (self.walls[nextX][nextY]):
                continue

            newPosition = (nextX, nextY)
            newCorners = oldCorners

            if (newPosition in self.corners):
                newCorners = tuple(oldCorners[i] or (newPosition == self.corners[i])
                        for i in range(len(self.corners)))

            successor = ((newPosition, newCorners), action, 1)
            successors.append(successor)

        return successors

def cornersHeuristic(state, problem):
    position, touchedCorners = state

    # Find all the corners we still have to touch.
    remainingCorners = set()
    for i in range(len(touchedCorners)):
        if (not touchedCorners[i]):
            remainingCorners.add(problem.corners[i])

    # Touch all the corners in a greedy fashion.
    # Because of the rectangular board, manhattan distance,
    # and ignoring walls, we will never overestimate.
    totalCost = 0

    while (len(remainingCorners) > 0):
        # Find the closest corner and move to it.
        closestCorner, closestCost = _closestPoint(position, remainingCorners)

        # Move to the cosest corner.
        totalCost += closestCost
        position = closestCorner
        remainingCorners.remove(closestCorner)

    return totalCost

# Returns: (closestPoint, cost)
def _closestPoint(position, points, distanceFunction = distance.manhattan):
    closestPoint = None
    closestCost = None

    for point in points:
        cost = distance.manhattan(position, point)
        if (closestPoint is None or cost < closestCost):
            closestPoint = point
            closestCost = cost

    return (closestPoint, closestCost)

def foodHeuristic(state, problem):
    position, foodGrid = state
    foodList = foodGrid.asList()

    if (len(foodList) == 0):
        return 0

    if (len(foodList) == 1):
        return distance.manhattan(position, foodList[0])

    # The best-case distance to the closest food.
    minCost = 0
    closestFood = None

    # Get the closest (manhattan) food.
    for food in foodList:
        cost = distance.manhattan(position, food)
        if (closestFood is None or cost < minCost):
            minCost = cost
            closestFood = food

    # We will be finding the max distance to the next piece of food.
    maxCost = 0
    nextFood = None

    # Find another piece of food that is furthest from the closest piece of food.
    for food in foodList:
        if (food == closestFood):
            continue

        cost = distance.manhattan(closestFood, food)
        isMaze = False

        # Take the max of the manhattan and maze distance between these two foods.
        # Note that we are only bothering to compute the maze distance if we are not already
        # beating the old max cost (since maze >= manhattan).
        if (cost < maxCost):
            cost = distance.maze(closestFood, food, problem.startingGameState)
            isMaze = True

        if (nextFood is None or cost > maxCost):
            maxCost = cost
            nextFood = food

            # Make sure the max distance is a maze distance.
            if (not isMaze):
                maxCost = distance.maze(closestFood, nextFood, problem.startingGameState)

    return minCost + maxCost - 1

class ClosestDotSearchAgent(SearchAgent):
    def __init__(self, index, **kwargs):
        super().__init__(index)

    def registerInitialState(self, state):
        self._actions = []
        self._actionIndex = 0

        currentState = state

        while (currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState)  # The missing piece
            self._actions += nextPathSegment

            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' %
                            (str(action), str(currentState)))

                currentState = currentState.generateSuccessor(0, action)

        logging.info('Path found with cost %d.' % len(self._actions))

    # Just use bfs.
    def findPathToClosestDot(self, gameState):
        problem = AnyFoodSearchProblem(gameState)
        return search.bfs(problem)

class AnyFoodSearchProblem(PositionSearchProblem):
    def __init__(self, gameState, start = None):
        super().__init__(gameState, goal = None, start = start)

        # Store the food for later reference.
        self.food = gameState.getFood()

    def isGoal(self, state):
        (x, y) = state
        return self.food[x][y]

# Just use a ClosestDotSearchAgent.
class ApproximateSearchAgent(BaseAgent):
    def __init__(self, index, **kwargs):
        super().__init__(index)

    def registerInitialState(self, state):
        self.agent = ClosestDotSearchAgent(self.index)
        self.agent.registerInitialState(state)

    def getAction(self, state):
        return self.agent.getAction(state)
