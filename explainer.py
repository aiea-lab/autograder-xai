import ast

class Analysis:
    def __init__(self):
        self.function_links = {
            # assignment 1
            'bfs' : self.verify_bfs,
            'dfs' : self.verify_dfs,
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
        recursive_rule = [ast.FunctionDef, ast.If, ast.For, ast.If, ast.Call]
        return_rule = [ast.Return]
        rules = [recursive_rule, return_rule]
        return self.enforce_ruleset(src, rules)
    
    def verify_a_star(self, src: str) -> str:
        loop_rule = [ast.While, ast.If, ast.For]
        rules = [loop_rule]
        return self.enforce_ruleset(src, rules)

    #   Assignment 2
    def verify_minimax(self, src: str) -> str:
        max_rule = [ast.FunctionDef, ast.If, ast.For, ast.If, ast.Return]
        min_rule = [ast.FunctionDef, ast.If, ast.For, ast.If, ast.Return]
        return_rule = [ast.Return]
        rules = [max_rule, min_rule, return_rule]
        return self.enforce_ruleset(src, rules)
    
    def verify_expectimax(self, src: str) -> str:
        max_rule = [ast.FunctionDef, ast.If, ast.For, ast.If, ast.Return]
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

        message = []

        def check_local_context(local_context_node, rules) -> bool:
            nonlocal message
            if len(rules) == 0:
                message.append("-local structure fully matched!")
                return True

            rule_counter = 0
            for node in ast.walk(local_context_node):
                # if node matches structural requirement, then increment rule counter
                if isinstance(node, rules[rule_counter]):
                    message.append(f"matching rule {rules[rule_counter]} on node {node}")
                    rule_counter += 1
                    if rule_counter >= len(rules):
                        message.append("-local structure fully matched!")
                        return True
                # if not, do nothing

            message.append(f"-failed to match local structure on rule {rules[rule_counter]}")
            return False

        try:
            root = ast.parse(src)
        
            # here are all the contexts at the highest level inside the source code
            top_level_context_nodes = root.body[0].body
            # try to find the correct local context to match the first rule in the ruleset
            
            fully_matched = 0
            top_list = []  # used to keep track of what top nodes have already been matched against before
            for i, ruleset in enumerate(rules):
                message.append(f"\n** trying to match ruleset {i+1}/{len(rules)}...")
                top_context_rule = ruleset[0]

                check = [isinstance(node, top_context_rule) for node in top_level_context_nodes]
                # print(check)
                # print(top_context_rule)
                if not any(check):
                    message.append(f"-no top level node matches for rule {top_context_rule}")
                    top_level_context_nodes = top_level_context_nodes[1:]
                    continue
                
                for top_node in top_level_context_nodes:
                    if top_node not in top_list:  # prevent matching two rulesets against the same local context
                        if isinstance(top_node, top_context_rule):
                            message.append(f"matching top node {top_node}: checking local context for more rules...")
                            result = check_local_context(top_node, ruleset[1:])
                            if result:
                                fully_matched += 1
                                index = top_level_context_nodes.index(top_node)
                                top_list.append(index)
                                break
                                
        
            message.append(f"\n({fully_matched} / {len(rules)} rules matched)")
            if fully_matched < len(rules):
                message.append("***---</3---FAILED TO MATCH ALL RULES---</3---***")
            else:
                message.append("***---<3---EVERYTHING MATCHED---<3---***")
            message.append("")
            return "\n".join(message)
        except:
            print(message)
            return "Exception, failed to parse source (probably)."
