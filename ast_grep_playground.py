from ast_grep_py import SgRoot
from cse140analysis import Analysis

exp = Analysis()

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
a = exp.verify_p0_q1(p0_q1_src)
print(a)


# dfs_src = '''
# def DFS(node: Node):
#     node.visited = True
#     for neighbour in node.neighbours:
#         if neighbour.visited is False:
#             DFS(neighbour)
# '''
# b = exp.verify_dfs(dfs_src)
# print(b)


p0_q2_src = '''
def shopSmart(orderList, fruitShops):
    """
    orderList: List of (fruit, numPound) tuples
    fruitShops: List of FruitShops
    """

    minCost = None
    bestShop = None

    for fruitShop in fruitShops:
        cost = fruitShop.getPriceOfOrder(orderList)
        if ((minCost is None) or (cost < minCost)):
            minCost = cost
            bestShop = fruitShop

    return bestShop
'''

c = exp.verify_p0_q2(p0_q2_src)
print(c)