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

def verify_p0_q1(src: str):
    """
    Rules:
    for
        increment OR assignment
    return
    """
    # instead of =, use regex to find = or +=
    # =|+=
    rule1 = ["for", "+="]
    rule2 = ["return"]
    # rule3 = ["should not match"]
    rules = [rule1, rule2]
    return enforce_ruleset(src, rules)

def verify_dfs(src: str):
    """
    Rules:
    for
        if
            recursion
    """
    # instead of =, use regex to find = or +=
    # =|+=
    rule1 = ["for", "if", "DFS"]
    rules = [rule1]
    return enforce_ruleset(src, rules)

def enforce_ruleset(src: str, rules: list[list[str]]):
    """
    General function.
    .find() function takes (one of) arguments:
        -pattern: str
        -kind: type
        -regex: str
    
    we will update this to use regex in a bit; should be better i think
    """

    ast = SgRoot(src, "python")
    root_node = ast.root()
    report_string = ""

    # for each seperate rule sequence
    for ruleset in rules:
        report_string += (f"=== matching against ruleset: {ruleset}\n")
        # find local context for this ruleset
        node = root_node.find(pattern= ruleset[0])

        # we have now been setup within the context of this rule
        # we search for our structure rules within 'node's context
        ruleset_counter = 0
        while node:
            # print("-----")
            # print(f"node.text() = {node.text()}")
            # print(f"rule_str = {rule_str}")

            # TODO: replace with regex match
            # match_node = node.find(pattern = rule_str)
            # if match_node:

            # switched to 'while' over 'if' because of inconsistent node parsing
            while ruleset_counter < len(ruleset) and ruleset[ruleset_counter] in node.text():
                # print(f"|-> '{match_node.text()}' matched")
                # print(f"|-> '{ruleset[ruleset_counter]}' matched")
                report_string += (f"|-> '{node.text()}' matched\n")
                ruleset_counter += 1
            node = node.next()
        
        if ruleset_counter >= len(ruleset):
            report_string += (f"Successfully matched against all rules in ruleset\n")
        else:
            report_string += (f"|-> ERROR '{ruleset[ruleset_counter]}' failed to match\n")
    
    return report_string

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
a = verify_p0_q1(p0_q1_src)
print(a)

dfs_src = '''
def DFS(node: Node):
    node.visited = True
    for neighbour in node.neighbours:
        if neighbour.visited is False:
            DFS(neighbour)
'''
b = verify_dfs(dfs_src)
print(b)
