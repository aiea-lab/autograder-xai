import ast
# import ast_grep_py
from ast_grep_py import SgRoot


# src = '''
# def greet(name):
#     print("Hello, " + name + "!")
#     print("line2")
    
# greet("John")
# '''
# root = SgRoot(src, "python")
# node = root.root()
# out = node.text()
# print(out)

# # matches = node.find_all(pattern="print($A)")
# matches = node.find_all(pattern="greet($A)")

# for match in matches:
#     out = match.get_match('A').text()
#     print(out)


# p1_soln_src = '''
# def _generalTreeSearch(problem, fringe):
#     seenNodes = set()

#     startState = problem.startingState()

#     fringe.push((startState, [], 0))
#     seenNodes.add(startState)

#     while (not fringe.isEmpty()):
#         state, path, pathCost = fringe.pop()

#         if (problem.isGoal(state)):
#             return path

#         for (successor, action, actionCost) in problem.successorStates(state):
#             if (successor in seenNodes):
#                 continue

#             fringe.push((successor, path + [action], pathCost + actionCost))
#             seenNodes.add(successor)

#     # No path found.
#     return None
# '''


"""
Here, let's say we are checking p1 DFS.
We teach that DFS is supposed to follow this essential structure:

function DFS(...)
    
    for (...)
        
        if (...)
            call function DFS(...)

^and the goal condition would be in here somewhere too.
    between the for and the if to the recursive call, i think
"""
class Node:
    def __init__(self):
        self.visited = False
        self.neighbours = []

def DFS(node: Node):
    node.visited = True
    for neighbour in node.neighbours:
        if neighbour.visited is False:
            DFS(neighbour)

dfs_src = '''
def DFS(node: Node):
    node.visited = True
    for neighbour in node.neighbours:
        if neighbour.visited is False:
            DFS(neighbour)
'''

"""
and so to verify the DFS algorithm, we would:
    go to root
        find child, make sure it is a 'for'
            find child, make sure it is an 'if'
                find child, make sure it is a 'call' to original function
"""


def verify_dfs(src: str):
    ast = SgRoot(src, "python")
    root_node = ast.root()
    out = root_node.text()
    print("======dfs_src======\n" + out)

    # # matches = node.find_all(pattern="print($A)")
    # matches = root_node.find_all(pattern="$A", kind="call")
    # # print(matches)

    # for match in matches:
    #     out = match.get_match('A').text()
    #     print(out)

    for_child = root_node.find(pattern="for")
    print(for_child)
    print("|-> " + for_child.text())

    if_child = for_child.get_root().root().find(pattern="if")
    print(if_child)
    print("|-> " + if_child.text())

    recurse_child = if_child.get_root().root().find(pattern="$A", kind="call")
    print(recurse_child)
    print("|-> " + recurse_child.text())
    
    # root_children = root_node.children()
    # ch_dfs_def = root_children[0].get_root().root()
    # print(ch_dfs_def.text())

verify_dfs(dfs_src)

"""
Continued concerns:
-how 
"""