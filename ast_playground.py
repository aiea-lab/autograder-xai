import ast
import pprint
from graphviz import Digraph


# Note that ast parsing does NOT remove multiline comments. So we might want to still do that by hand.
"""
tree = ast.parse(code2_clean)
pprint.pprint(ast.dump(tree))

# Create a Graphviz Digraph object
dot = Digraph()

# Define a function to recursively add nodes to the Digraph
def add_node(node, parent=None):
    node_name = str(node.__class__.__name__)
    dot.node(str(id(node)), node_name)
    if parent:
        dot.edge(str(id(parent)), str(id(node)))
    for child in ast.iter_child_nodes(node):
        add_node(child, node)

# Add nodes to the Digraph
add_node(tree)

# Render the Digraph as a PNG file
dot.format = 'png'
dot.render('my_ast', view=True)
"""

"""
To verify the DFS algorithm, we would:
    go to root
        find child, make sure it is a 'for'
            find child, make sure it is an 'if'
                find child, make sure it is a 'call' to original function
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

class DFSNodeVisitor(ast.NodeVisitor):
    # so you can make different functions, to visit different types.
    # def visit_Call(self, node):
    #     if isinstance(node.func, ast.Name) and node.func.id == "print":
    #         args = [arg for arg in node.args if isinstance(arg, ast.Constant)]
    #         if args:
    #             print("Detected print statements with string literals:")
    #             for arg in args:
    #                 print(arg.value)  # Print the string literal directly
    #     self.generic_visit(node)

    def visit_If(self, node2):
        # print(type(node2))  # ast.If
        print("Detected If statement with...")
        # print(f"node2.target={node2.target} \nnode2.iter={node2.iter} \nnode2.body={node2.body} \nnode2.orelse={node2.orelse} \nnode2.type_comment={node2.type_comment}")
        print(type(node2))
        print(node2)
        print(node2.test)
        print(node2.body)
        print(node2.orelse)

        
        # node3 = node2.body[0]
        # print(node3.value)

    # def visit_For(self, node):
    #     # if isinstance(node.func, ast.Name) and node.func.id == "print":
    #     # print(f"args = {node.args}")
    #     # args = [arg for arg in node.args if isinstance(arg, ast.Constant)]
    #     # print(f"node.func = {node.func}")
    #     # args = [arg for arg in node.args if isinstance(arg, ast.For)]
    #     # if args:

    #     # class ast.For(target, iter, body, orelse, type_comment)
    #     # https://docs.python.org/3/library/ast.html > ctrl+f > ast.for

    #     print("Detected For statement with...")
    #     print(f"node.target={node.target} \nnode.iter={node.iter} \nnode.body={node.body} \nnode.orelse={node.orelse} \nnode.type_comment={node.type_comment}")
    #         # for arg in args:
    #             # print(arg.value)  # Print the string literal directly
    #     # self.visit(node.target)
    #     node2 = node.body[0]

    #     self.visit_If(node2)

    #     # from here

    #     # if isinstance(node2.stmt, ast.Name) and node2.stmt.id == "AugAssign":
    #     #     print("yea")
    #     # self.generic_visit(node)
    

def perform_static_analysis(code):
    tree = ast.parse(code)

    # visitor = DFSNodeVisitor()
    # visitor.visit(tree)

    for node in ast.walk(tree):
        is_for = False
        try:
            is_for = isinstance(node, ast.For)
            print(f"looking at node {node} with type: '{type(node)}'\n")
            # print(f"|-> node type = {type(node)}\n")
            # is_for = (node.id == 'if')
        except AttributeError:
            pass
        if is_for:
            return check_dfs(node)

def check_dfs(node):
    """
    To verify the DFS algorithm, we would:
    go to root
        find child, make sure it is a 'for'
            find child, make sure it is an 'if'
                find child, make sure it is a 'call' to original function
    
    Returns true if validates, false otherwise.
    """
    print("Detected For statement with...")
    print(f"node.target={node.target} \nnode.iter={node.iter} \nnode.body={node.body} \nnode.orelse={node.orelse} \nnode.type_comment={node.type_comment}")
        # for arg in args:
            # print(arg.value)  # Print the string literal directly
    # self.visit(node.target)
    node2 = node.body

# perform_static_analysis(code1)
perform_static_analysis(dfs_src)

