#!/usr/bin/env python3

import importlib
import math
import glob
import os
import shutil
import sys
import time

from importlib import util

from flake8.main import application

from cse40.assignment import Assignment
from cse40.question import Question
from cse40.style import Style

THIS_DIR = os.path.dirname(os.path.realpath(__file__)) # p1 path
BASE_DIR = os.path.join(THIS_DIR, '..') # pacman-dev path

CI_DIR = os.path.join(BASE_DIR, 'pacman', '.ci', 'flake8.cfg')
SOLUTION_DIRS = [
    os.path.join(BASE_DIR, 'p1', 'solution')
]

class Q1(Question):
    def __init__(self, name, max_points):
        super().__init__(name, max_points)
        self.solution = [146]
        self.leeway = [1.0]
        self.layouts = ['mediumMaze']

    def score_question(self, submission):
        startState = pacman.PacmanGameState(layout.getLayout(self.layouts[0]))
        problem = PositionSearchProblem(startState)
        path = search_student.depthFirstSearch(problem)

        if problem.getExpandedCount() / self.solution[0] <= self.leeway[0] or math.isclose(problem.getExpandedCount(), self.solution[0]):
            self.full_credit()
        else:
            self.add_message('Wrong number of nodes expanded for %s: %d vs %d' % (self.name, problem.getExpandedCount(), self.solution[0]))

class Q2(Question):
    def __init__(self, name, max_points):
        super().__init__(name, max_points)
        self.solution = [269]
        self.leeway = [1.0]
        self.layouts = ['mediumMaze']

    def score_question(self, submission):
        startState = pacman.PacmanGameState(layout.getLayout(self.layouts[0]))
        problem = PositionSearchProblem(startState)
        path = search_student.breadthFirstSearch(problem)

        if problem.getExpandedCount() / self.solution[0] <= self.leeway[0] or math.isclose(problem.getExpandedCount(), self.solution[0]):
            self.full_credit()
        else:
            self.add_message('Wrong number of nodes expanded for %s: %d vs %d' % (self.name, problem.getExpandedCount(), self.solution[0]))

class Q3(Question):
    def __init__(self, name, max_points):
        super().__init__(name, max_points)
        self.solution = [268, 260, 173, 13]
        self.leeway = [1.1, 2.0]
        self.layouts = ['mediumMaze', 'testSearch']

    def score_question(self, submission):
        positionStartState = pacman.PacmanGameState(layout.getLayout(self.layouts[0]))
        foodStartState = pacman.PacmanGameState(layout.getLayout(self.layouts[1]))

        tests = []
        tests.append((PositionSearchProblem(positionStartState), self.leeway[0], self.solution[0]))
        tests.append((PositionSearchProblem(positionStartState, lambda pos: 0.5 ** pos[0]), self.leeway[0], self.solution[1]))
        tests.append((PositionSearchProblem(positionStartState, lambda pos: 2 ** pos[0]), self.leeway[0], self.solution[2]))
        tests.append((FoodSearchProblem(foodStartState), self.leeway[0], self.solution[3]))

        for problem, leeway, solution in tests:
            search_student.uniformCostSearch(problem)
            if problem.getExpandedCount() / solution <= leeway or math.isclose(problem.getExpandedCount(), solution):
                self.score += 0.5
            else:
                self.add_message('Wrong number of nodes expanded for %s: %d vs %d' % (self.name, problem.getExpandedCount(), solution))

        self.score = int(self.score)

class Q4(Question):
    def __init__(self, name, max_points):
        super().__init__(name, max_points)
        self.solution = [219]
        self.leeway = [1.1]
        self.layouts = ['mediumMaze']

    def score_question(self, submission):
        startState = pacman.PacmanGameState(layout.getLayout(self.layouts[0]))
        problem = PositionSearchProblem(startState)
        path = search_student.aStarSearch(problem, heuristic.manhattan)

        if problem.getExpandedCount() / self.solution[0] <= self.leeway[0] or math.isclose(problem.getExpandedCount(), self.solution[0]):
            self.full_credit()
        else:
            self.add_message('Wrong number of nodes expanded for %s: %d vs %d' % (self.name, problem.getExpandedCount(), self.solution[0]))

class Q5(Question):
    def __init__(self, name, max_points):
        super().__init__(name, max_points)
        self.solution = [28]
        self.leeway = [1.0]
        self.layouts = ['tinyCorners']

    def score_question(self, submission):
        startState = pacman.PacmanGameState(layout.getLayout(self.layouts[0]))
        problem = searchAgents_student.CornersProblem(startState)
        path = search_student.breadthFirstSearch(problem)
        visited = getStatesFromPath(startState.getPacmanPosition(), path)

        layout_top = startState.getInitialLayout().getHeight() - 2
        layout_right = startState.getInitialLayout().getWidth() - 2

        corners = ((1, 1), (1, layout_top), (layout_right, 1), (layout_right, layout_top))

        if path == None:
            self.add_message('Optimal path from student problem did not match the optimal path for %s: %s vs %d' % (self.name, "NoneType", self.solution[0]))
            return

        if len(path) / self.solution[0] <= self.leeway[0] or math.isclose(len(path), self.solution[0]):
            for corner in corners:
                if corner not in visited:
                    self.add_message('Path missed corner ' + str(corner))
                else:
                    self.score += 0.5
            if self.score != self.max_points:
                self.score = 0
        else:
            self.add_message('Optimal path from student problem did not match the optimal path for %s: %d vs %d' % (self.name, len(path), self.solution[0]))

class Q6(Question):
    def __init__(self, name, max_points):
        super().__init__(name, max_points)
        self.solution = [106]
        self.layouts = ['mediumCorners']
        self.thresholds = [2000, 1600, 1200]

    def score_question(self, submission):
        heuristic = searchAgents_student.cornersHeuristic
        for name, cost, text_layout in CORNER_TESTS:
            if not cornerAdmissible(text_layout, cost, heuristic):
                self.add_message('Corners heuristic failed admissibility test %s' % (name))
                return
            self.add_message('Corners heuristic passed admissibility test %s' % (name))

        startState = pacman.PacmanGameState(layout.getLayout(self.layouts[0]))
        problem = searchAgents_student.CornersProblem(startState)
        path = search_student.aStarSearch(problem, heuristic)

        if heuristic(problem.startingState(), problem) > self.solution[0]:
            self.add_message('Corners heuristic failed admissibility test (mediumCorners)')
            return
        if problem.actionsCost(path) > self.solution[0]:
            self.add_message('A* gave a non-optimal solution to mediumCorners; maybe not admissible!')
            return

        self.add_message("For mediumCorners, the A* agent expanded %d nodes" % (problem.getExpandedCount()))
        for threshold in self.thresholds:
            if problem.getExpandedCount() < threshold:
                self.add_message('Passed Threshold: %d' % (threshold))
                self.score += 1

class Q7(Question):
    def __init__(self, name, max_points):
        super().__init__(name, max_points)
        self.solution = [60]
        self.layouts = ['trickySearch']
        self.thresholds = [15000, 12000, 9000, 7000]
        self.consistency = True

    def score_question(self, submission):
        heuristic = searchAgents_student.foodHeuristic
        for name, cost, text_layout in FOOD_TESTS:
            if not foodAdmissible(text_layout, cost, heuristic):
                self.add_message('Food heuristic failed admissibility test %s' % (name))
                return
            self.add_message('Food heuristic passed admissibility test %s' % (name))

            if not foodConsistency(text_layout, cost, heuristic):
                self.add_message('Food heuristic failed consistency test %s' % (name))
                self.consistency = False
                continue
            self.add_message('Food heuristic passed consistency test %s' % (name))

        startState = pacman.PacmanGameState(layout.getLayout(self.layouts[0]))
        problem = FoodSearchProblem(startState)
        path = search_student.aStarSearch(problem, heuristic)

        if heuristic(problem.startingState(), problem) > self.solution[0]:
            self.add_message('Food heuristic failed admissibility test trickySearch')
            return
        if problem.actionsCost(path) > self.solution[0]:
            self.add_message('A* gave a non-optimal solution to trickySearch; maybe not admissible!')
            return

        self.add_message("For trickySearch, the A* agent expanded %d nodes" % (problem.getExpandedCount()))
        for threshold in self.thresholds:
            if problem.getExpandedCount() < threshold:
                self.add_message('Passed Threshold: %d' % (threshold))
                self.score += 1

        if self.consistency:
            self.score += 1

class Q8(Question):
    def __init__(self, name, max_points):
        super().__init__(name, max_points)
        self.solution = [1, 1, 1, 3, 1, 2, 1, 1, 1, 1, 2, 3, 1]

    def score_question(self, submission):
        problem = searchAgents_student.ClosestDotSearchAgent(0)

        for i in range(0, len(FOOD_TESTS)):
            gameState = pacman.PacmanGameState(layout.Layout(FOOD_TESTS[i][2]))
            path = problem.findPathToClosestDot(gameState)

            if len(path) != self.solution[i]:
                self.add_message('Closest dot not found in %s' % (FOOD_TESTS[i][0]))
                return

        self.full_credit()

class Extra(Question):
    """
    Evaluates their mini-contest entry but times-out after max_time seconds
    """
    def __init__(self, name, max_points):
        super().__init__(name, max_points)

    def score_question(self, submission):
        start_time = time.time()
        args = pacman.readCommand(['-l', 'bigSearch', '-p', 'ApproximateSearchAgent', '--null-graphics'])
        games = pacman.runGames(**args)
        extra_time = (time.time() - start_time)

        self.add_message('Extra credit runtime: %1.2f' % (extra_time))
        self.add_message('Extra credit total moves %d' % (len(games[0].moveHistory)))

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module

def prepare_submission(submission_dir):
    # Import into the global namespace.

    submission_dir = os.path.join(THIS_DIR, submission_dir)
    submission_student_dir = os.path.join(BASE_DIR, 'pacman', 'pacai', 'student')

    # Copy Python files from the student's submission directory to the destination directory.
    for path in glob.glob(os.path.join(submission_dir, '*.py')):
        shutil.copy(path, submission_student_dir)

    pacman_templates = os.path.join(BASE_DIR, 'pacman')

    sys.path.insert(0, pacman_templates)

    global Actions
    global FoodSearchProblem
    global PositionSearchProblem
    global heuristic
    global layout
    global pacman
    global search_student
    global searchAgents_student
    global PacmanTextView

    from pacai.bin import pacman
    from pacai.core import layout
    from pacai.core.actions import Actions
    from pacai.core.search import heuristic
    from pacai.core.search.food import FoodSearchProblem
    from pacai.core.search.position import PositionSearchProblem
    from pacai.student import search as search_student
    from pacai.student import searchAgents as searchAgents_student
    from pacai.ui.pacman.text import PacmanTextView

def main(submission_dir):
    prepare_submission(submission_dir)
    questions = [
        Q1("Q1", 2),
        Q2("Q2", 1),
        Q3("Q3", 2),
        Q4("Q4", 3),
        Q5("Q5", 2),
        Q6("Q6", 3),
        Q7("Q7", 5),
        Q8("Q8", 2),
        Extra("Extra", 0),
        Style(os.path.join(submission_dir, "search.py"), max_points=5),
        Style(os.path.join(submission_dir, "searchAgents.py"), max_points=0),
    ]

    assignment = Assignment('Project 1: Search', questions)
    score = assignment.grade(None)
    print(assignment.report())
    return score

def _load_args(args):
    executable = args.pop(0)
    if (len(args) != 1 or ({'h', 'help'} & {arg.lower().strip().replace('-', '') for arg in args})):
        print("USAGE: python3 %s <submission dir>" % (executable), file = sys.stderr)
        sys.exit(1)

    submission_dir = os.path.abspath(args.pop(0))

    return submission_dir

# Support testing functions.

def getStatesFromPath(start, path):
    """
    Returns the list of states visited along the path
    """

    vis = [start]
    curr = start

    if path == [] or path == None:
        return vis

    for a in path:
        x, y = curr
        dx, dy = Actions.directionToVector(a)
        curr = (int(x + dx), int(y + dy))
        vis.append(curr)

    return vis

def foodConsistency(layoutText, cost, heuristic):
    gameState = pacman.PacmanGameState(layout.Layout(layoutText))
    problem = FoodSearchProblem(gameState)
    state = problem.startingState()

    h0 = heuristic(state, problem)
    succs = problem.successorStates(state)
    for succ in succs:
        h1 = heuristic(succ[0], problem)
        if h0 - h1 > 1:
            return False

    return True

def foodAdmissible(layoutText, cost, heuristic):
    gameState = pacman.PacmanGameState(layout.Layout(layoutText))
    problem = FoodSearchProblem(gameState)
    startState = problem.startingState()

    return heuristic(startState, problem) <= cost

def cornerAdmissible(layoutText, cost, heuristic):
    gameState = pacman.PacmanGameState(layout.Layout(layoutText))
    problem = searchAgents_student.CornersProblem(gameState)
    startState = problem.startingState()

    return heuristic(startState, problem) <= cost

CORNER_TESTS = [
    ('ct1', 8, [
        "%%%%%",
        "%. .%",
        "%   %",
        "%   %",
        "%.P.%",
        "%%%%%"
    ]),

    ('ct2', 8, [
        "%%%%%",
        "%. .%",
        "%%% %",
        "%P% %",
        "%. .%",
        "%%%%%"
    ]),

    ('ct3', 28, [
        "%%%%%%%%",
        "%.    .%",
        "%   P  %",
        "% %%%% %",
        "% %    %",
        "% % %%%%",
        "%.%   .%",
        "%%%%%%%%"
    ])
]

FOOD_TESTS = [
    ("Test 7", 11, [
        "%%%%%",
        "%...%",
        "%...%",
        "%...%",
        "%P..%",
        "%%%%%"
    ]),

    ("Test 6", 5, [
        "%%%%%",
        "% ..%",
        "% . %",
        "% P %",
        "% . %",
        "%%%%%"
    ]),

    ("Test 5", 7, [
        "%%%%%",
        "% ..%",
        "% . %",
        "% P %",
        "%   %",
        "% . %",
        "%%%%%"
    ]),

    ("Test 4", 5, [
        "%%%%%",
        "%...%",
        "%   %",
        "%   %",
        "%P  %",
        "%%%%%"
    ]),

    ("Test 3", 6, [
        "%%%%%",
        "%.. %",
        "% %.%",
        "%.%%%",
        "%P  %",
        "%%%%%"
    ]),

    ("Test 2", 7, [
        "%%%%%",
        "% . %",
        "%   %",
        "% P %",
        "%   %",
        "%   %",
        "% . %",
        "%%%%%"
    ]),

    ("Test 1", 8, [
        "%%%%%",
        "%.  %",
        "%   %",
        "%.P %",
        "%   %",
        "%   %",
        "%.  %",
        "%%%%%"
    ]),

    ("Test 8", 1, [
        "%%%%%",
        "% . %",
        "% P %",
        "%   %",
        "%   %",
        "%   %",
        "%   %",
        "%%%%%"
    ]),

    ("Test 9", 5, [
        "%%%%%",
        "% . %",
        "%   %",
        "%   %",
        "%   %",
        "% . %",
        "% P %",
        "%%%%%"
    ]),

    ("Test 10", 31, [
        "%%%%%%%%%%%",
        "% ....... %",
        "% %%%%%%. %",
        "% ....... %",
        "% .%%%%%% %",
        "% ....... %",
        "% %%%%%%. %",
        "% ....... %",
        "% P       %",
        "%%%%%%%%%%%"
    ]),

    ("Test 11", 21, [
        "%%%%%%%%%%%%%%%%%%%%%%%%",
        "%.    P .       ..     %",
        "%%%%%%%%%%%%%%%%%%%%%%%%"
    ]),

    ("Test 13", 7, [
        "%%%%%%%",
        "%.   .%",
        "%  P  %",
        "%%%%%%%"
    ]),

    ("Test 12", 16, [
        "%%%%%%",
        "%....%",
        "% %%.%",
        "% %%.%",
        "%.P .%",
        "%.%%%%",
        "%....%",
        "%%%%%%"
    ])
]

if (__name__ == '__main__'):
    main(_load_args(sys.argv))
