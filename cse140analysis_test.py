from cse140analysis import Analysis

a = Analysis()

# read in dummy string text for p0_buyLotsOfFruit()
s = str('''"""
    orderList: List of (fruit, weight) tuples

    Returns cost of order
    """

    # Here's the total cost
    totalCost = 0.0

    for (fruit, weight) in orderList:
        totalCost += FRUIT_PRICES[fruit] * weight

    return totalCost''')

chunk_s = a.chunk_source(s)

# print(chunk_s)
for ln in chunk_s:
    print(ln)

feed = a.get_feedback("", s)
print(f'\n{feed}')