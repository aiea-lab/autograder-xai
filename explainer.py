import ast

class Analysis:
    def __init__(self):
        self.function_links = {
            # assignment 1
            'bfs' : self.verify_bfs,
            'dfs' : self.verify_bfs,
            'a_star' : self.verify_a_star,

            # assignment 2
            'minimax' : self.verify_minimax,
            'expectimax' : self.verify_expectimax

            # ...
        }
    
    # Analysis Functions
    #   Assignment 1
    def verify_bfs(self, src: str) -> str:
        loop_rule = [ast.While, ast.If, ast.For, ast.If]
        rules = [loop_rule]
        return self.enforce_ruleset(src, rules)
    
    def verify_dfs(self, src: str) -> str:
        recursive_rule = [ast.FunctionDef, ast.If, ast.For, ast.If, ast.Call]  # ast.Call might be wrong though?
        return_rule = [ast.Return]
        rules = [recursive_rule, return_rule]
        return self.enforce_ruleset(src, rules)
    
    def verify_a_star(self, src: str) -> str:
        loop_rule = [ast.While, ast.If, ast.For]
        rules = [loop_rule]
        return self.enforce_ruleset(src, rules)

    #   Assignment 2
    def verify_minimax(self, src: str) -> str:
        max_rule = [ast.FunctionDef, ast.If, ast.For, ast.IF, ast.Return]
        min_rule = [ast.FunctionDef, ast.If, ast.For, ast.IF, ast.Return]
        return_rule = [ast.Return]
        rules = [max_rule, min_rule, return_rule]
        return self.enforce_ruleset(src, rules)
    
    def verify_expectimax(self, src: str) -> str:
        max_rule = [ast.FunctionDef, ast.If, ast.For, ast.IF, ast.Return]
        chance_rule = [ast.FunctionDef, ast.If, ast.For, ast.Return]
        return_rule = [ast.Return]
        rules = [max_rule, chance_rule, return_rule]
        return self.enforce_ruleset(src, rules)

    # General Functions
    def get_feedback(self, key, source) -> str:
        """
        The parameter 'key' tells us what analysis function to run
        The parameter 'source' is the submission code
        """
        if key in self.function_links:
            return self.function_links[key](source)
        return "Dynamic feedback implementation not found."
    
    def enforce_ruleset(self, src: str, rules: list[list[type]]) -> str:
        """ 
        General rule-matching function.
        Parses 'src' as an AST and then checks for each list of rules in 'rules'
        Confirms and rejects each list of rules separately.
        """

        def check_local_context(local_context_node, rules) -> str:
            if len(rules) == 0:
                return "Structure fully matched!"

            rule_counter = 0
            for node in ast.walk(local_context_node):
                # if node matches structural requirement, then increment rule counter
                if isinstance(node, rules[rule_counter]):
                    print(f"matching rule {rules[rule_counter]} on node {node}")
                    rule_counter += 1
                    if rule_counter >= len(rules):
                        return "Structure fully matched!"
                # if not, do nothing

            return (f"Failed to match structure on rule {rules[rule_counter]}")

        try:
            root = ast.parse(src)
        
            # here are all the contexts at the highest level inside the source code
            top_level_context_nodes = root.body[0].body
            # try to find the correct local context to match the first rule in the ruleset
            
            fully_matched = True
            top_list = []
            failed = 0
            for ruleset in rules:
                top_context_rule = ruleset[0]
                check = [isinstance(node, top_context_rule) for node in top_level_context_nodes]

                if not any(check):
                    print("Failed to match top level node")
                    failed += 1
                    top_level_context_nodes = top_level_context_nodes[1:]
                    continue

                for top_node in top_level_context_nodes:
                    if top_node not in top_list:        
                        if isinstance(top_node, top_context_rule):
                            print(f"{top_node}: Top node matched, checking local context for remaining ruleset")
                            result = check_local_context(top_node, ruleset[1:])
                            if "Structure fully matched!" in result:
                                print("——Structure fully matched!")
                                index = top_level_context_nodes.index(top_node)
                                top_list.append(index)
                                break
                            else:
                                fully_matched = False
                                
            if failed >= 1:
                return "***———</3———FAILED TO MATCH ALL RULES———</3———***"
            elif fully_matched:
                return "***———<3———EVERYTHING MATCHED———<3———***"

            return "Failed to match any ruleset"
        except:
            return "Failed to parse source"


# Test run
src = '''def minimax(b: chess.Board, player: bool, depth: int):

    def get_max_move(b: chess.Board, player: bool, depth: int, alpha: int, beta: int):
        # e = evaluation(b, player)['total_score']
        e = eval_material(b, player)
        if depth == 0 or abs(e) == inf:
            return e, None

        best_value = -inf
        best_moves = []
        for m in b.legal_moves:
            temp_board = b.copy()
            temp_board.push(m)
            new_value = get_min_move(temp_board, depth - 1, player, alpha, beta)[0]

            # Maintain a running max of the best move
            if new_value > best_value:
                best_value = new_value
                best_moves = [m]
            elif new_value == best_value:
                best_moves.append(m)

            # Alpha-beta pruning
            if best_value >= beta:
                break
            alpha = max(alpha, best_value)

        return best_value, random.choice(best_moves)

    def get_min_move(b: chess.Board, player: bool, depth: int, alpha: int, beta: int):
        # e = evaluation(b, player)['total_score']
        e = eval_material(b, player)
        if depth == 0 or abs(e) == inf:
            return e, None
        
        worst_value = +inf
        for m in b.legal_moves:
            temp_board = b.copy()
            temp_board.push(m)
            new_value = get_max_move(temp_board, depth - 1, player, alpha, beta)[0]

            # Maintain a running minimum
            if new_value < worst_value:
                worst_value = new_value

            # Alpha-beta pruning        
            if worst_value <= alpha:
                break
            beta = min(beta, worst_value)

        return worst_value, None

    # print("starting minimax")
    return get_max_move(b, player, depth, -inf, +inf)'''
explainer = Analysis() 
feedback = explainer.get_feedback('minimax', src)
print(feedback)