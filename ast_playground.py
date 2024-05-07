import ast
import pprint
from graphviz import Digraph


code0 = '''
def greet(name):
    print("Hello, " + name + "!")
    
greet("John")
'''

code1 = '''
def calculate_average(numbers):
        total = sum(numbers)
        average = total / len(numbers)
        print("Average:", average)
   
data = [1, 2, 3, 4, 5]
calculate_average(data)
print("End of program")
    '''

code2 = str('''"""
orderList: List of (fruit, weight) tuples

Returns cost of order
"""

# Here's the total cost
totalCost = 0.0

for (fruit, weight) in orderList:
    totalCost += FRUIT_PRICES[fruit] * weight

return totalCost''')

code2_clean = '''
def solution():
    totalCost = 0.0

    for (fruit, weight) in orderList:
        totalCost += FRUIT_PRICES[fruit] * weight

    return totalCost
print("Finished calculation.")
'''

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
Note that 
Let's try a rule, e.g. 'a' before 'b' rule.
using code1
We have a way to identify certain expressions; e.g. 'increment' inside 'for loop'
and then use node visiting to make sure that we identify things in the right order?
Let's try it.

So after looking around and learning some stuff, the process for the above rule would have to be:
Visit_For() ->
Visit() node.body ->
inside node.body, have to check for the behaviour we want to see, e.g 'AugAssign'
(Note: assignment is classified differently than Assignment, so we'd have to look for both of those)
then, if we see the 'AugAssign' node, we're mark the rule as fulfilled. If not, then not.

"""

class FunctionCallVisitor(ast.NodeVisitor):
    # so you can make different functions, to visit different types.
    # e.g. Visit_Call()
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            args = [arg for arg in node.args if isinstance(arg, ast.Constant)]
            if args:
                print("Detected print statements with string literals:")
                for arg in args:
                    print(arg.value)  # Print the string literal directly
        self.generic_visit(node)

    def visit_For(self, node):
        # if isinstance(node.func, ast.Name) and node.func.id == "print":
        # print(f"args = {node.args}")
        # args = [arg for arg in node.args if isinstance(arg, ast.Constant)]
        # print(f"node.func = {node.func}")
        # args = [arg for arg in node.args if isinstance(arg, ast.For)]
        # if args:

        # class ast.For(target, iter, body, orelse, type_comment)
        # https://docs.python.org/3/library/ast.html > ctrl+f > ast.for

        print("Detected For statement with...")
        print(f"node.target={node.target} \nnode.iter={node.iter} \nnode.body={node.body} \nnode.orelse={node.orelse} \nnode.type_comment={node.type_comment}")
            # for arg in args:
                # print(arg.value)  # Print the string literal directly
        # self.visit(node.target)
        node2 = node.body
        # if isinstance(node2.stmt, ast.Name) and node2.stmt.id == "AugAssign":
        #     print("yea")
        # self.generic_visit(node)
    

def perform_static_analysis(code):
    tree = ast.parse(code)
    # pprint.pprint(ast.dump(tree))

    visitor = FunctionCallVisitor()
    visitor.visit(tree)

# perform_static_analysis(code1)
perform_static_analysis(code2_clean)

