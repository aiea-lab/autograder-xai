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

p0_q1_src = '''
def buyLotsOfFruit(orderList):
    """
    orderList: List of (fruit, weight) tuples

    Returns cost of order
    """

    totalCost = 0.0

    for (fruit, weight) in orderList:
        totalCost += FRUIT_PRICES[fruit] * weight

    return totalCost
'''

# let's make it so that you can give:
#   - src: the source code
#   - rules: a list of lists, where each internal list is:
#       - [a nested set of dependences]
#
#   then, it will parse the src into an AST
#   then, for each internal list in rules:
#       - do a whole little try loop for it

def verify_p0_q1(src: str):
        """
        Rules:
        for
            increment OR assignment
        return
        """
        # instead of =, use regex to find = or +=
        # =|+=
        rule1 = ["for", "="]  # should fail to find return
        rule2 = ["return"]

        # rule2 = ["return"]
        rules = [rule1]
        return enforce_ruleset(src, rules)

def enforce_ruleset(src: str, rules: list[list[str]]):
        """
        General function.
        .find() function takes arguments:
            -pattern: str
            -kind: type
            -regex: str
            should use regex ok
        
        there are some interesting functions, such as 
        .inside()
        .has()
        .precedes()
        .follows()
        What exactly do they do?
        """
        ast = SgRoot(src, "python")
        root_node = ast.root()
        for rule_group in rules:
            # try:
            #     root = ast.root().find(pattern=rule_group[0])
            #     print("|-> " + root.text())
            #     cur = root
            #     child = None
            #     for rule in rule_group[1:]:
            #         child = cur.get_root().root().find(pattern=rule)
            #         print("|-> " + child.text())
            #         cur = child
            # except:
            #     print("ERROR!! Some structure part not detected!")
            print(root_node.child(0).text())

            # try:
            for_child = root_node.find(pattern="for")
            # for_child = root_node.find(regex="[for]")
            print("|-> " + for_child.text())
            # print("|-> " + for_child.get_match('A').text())

            # assign_child = for_child.next()
            assign_child = for_child.next()
            # assign_child = for_child.get_root().root().find(pattern="=")
            # assign_child = for_child.find(pattern="=")
            print("|-> " + assign_child.text())

            # for_children = for_child.next_all()
            # print(for_children)

            """
            1. create a new subtree using SgRoot() including all the code of the for loop
            2. find the correct way to do a search within a new node's context
                (the new node not being the root)
            3. node.next() or node.next_all(), and i think you could use that to look for the next dependency

            iterate through node.next for a given node to check its context
                -look at the node to see if it's satisfies the rule you're looking for
                -if it does, update your rule to the next one, and now look in
                 this new node's children

            """



            # # return_child = root_node.find(pattern="return")
            # return_child = assign_child.find(pattern="return")
            # print("|-> " + return_child.text())
            # # ^write a function to generalize this kind of thing?
            # # would pass in: (parent node, pattern)
            # # returns: ('child node' or maybe 'None')
            # # just a cute little abstraction helper function

            # except:
            #     print("ERROR!! Some structure part not detected!")
        # could add variables in the 'try' section to set bools for each child
        # then could print out a list here with each expected child....T/F

        # feedback_start = "Dynamic feedback for p0_q1 begins:\n"
        # feedback = ""

        # instead of print(), switch to just add to feedback string
        # ok boss

        # if '-' not in feedback:
        #     feedback += "lgtm."
        # return feedback_start + feedback

verify_p0_q1(p0_q1_src)

def verify_dfs(src: str):
    ast = SgRoot(src, "python")
    root_node = ast.root()
    out = root_node.text()
    print("======dfs_src======\n" + out + "===================")

    # # matches = node.find_all(pattern="print($A)")
    # matches = root_node.find_all(pattern="$A", kind="call")
    # # print(matches)

    # for match in matches:
    #     out = match.get_match('A').text()
    #     print(out)

    """
    Run the validation check against all matching occurrences of the starter term.
    If any one of them returns success, then return success.
    If all of them fail, then how do we know which one to give feedback to?

    Maybe it makes more sense to just try it against the first one.
    Then we can easily give feedback against it, and it can also be easily understood by the students.
    """

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

# verify_dfs(dfs_src)

"""
Continued concerns:

"""