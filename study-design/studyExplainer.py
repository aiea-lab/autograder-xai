import ast

""" 
This class is a simplified version of the more general Analysis class found in explainer.py at the root level.
This more focused implementation should be sufficient for the study.
"""
class Analysis:

    # Setup the rules to be used in enforce ruleset
    def get_feedback(self, src) -> str:
        """
        Feedback within a particular ruleset is set up in pairs of (ast type, response to failing that test)
        So a ruleset would be a list of tuples: [(ast type, response to failing that test)]
        """
        
        # look for an assign node that calls slogan.split(' ') to break the input into words, making it much easier to work with
        split_rule = [ast.Assign]  # just the assign isn't enough, need to check that they split on whitespace
        
        # look for an assign node that then has a bunch of '*'s characters in it. Try to find where the student is creating this. We would try to find an 'assign' character, and then within that line, try to find a 
        # if we can't find it, then we recommend that they create the top and bottom border somewhere. You should be able to derive the length based on the longest word in the group.
        border_rule = [ast.Assign]  # just the assign isn't enough, need to check for asterisks (this is possible by looking at the string underlying the node.)

        # for the main loop. 
        # -It should iterate through 'words'
        # -check if each word obeys the conditions: not empty, is alphanumeric
        # -assign or aug assign the word and the asterisks to your string solution
        loop_rule = [ast.For, ast.If]

        # for return at the end
        # -you just gotta make sure to return at the end, that's all.
        return_rule = [ast.Return]

        rules = [border_rule, loop_rule, return_rule]
        return self.enforce_ruleset(src, rules)
    
    # Traverse the tree and enforce the prescribed rules
    def enforce_ruleset(self, src: str, rules: list[list[type]]) -> str:
        """ 
        General rule-matching function.
        Parses 'src' as an AST and then checks for each list of rules in 'rules'
        
        Match the rulesets one at a time. As soon as one fails, stop matching and give out feedback.
        """

        message = []
        message.append("\n== Structural Explanation")

        def check_local_context(local_context_node, rules) -> bool:
            nonlocal message
            if len(rules) == 0:
                message.append("-local structure trivially matched!")
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

        # try:
        root = ast.parse(src)
    
        # here are all the contexts at the highest level inside the source code
        print(root)
        print(root.body)
        print(root.body[0])
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
                        message.append(f"matching top node {top_node}: entering context...")
                        result = check_local_context(top_node, ruleset[1:])
                        if result:
                            fully_matched += 1
                            index = top_level_context_nodes.index(top_node)
                            top_list.append(index)
                            break
                            
    
        message.append(f"\n({fully_matched}/{len(rules)} rules matched)")
        if fully_matched < len(rules):
            message.append("***---</3---FAILED TO MATCH ALL RULES---</3---***")
        else:
            message.append("***---<3---EVERYTHING MATCHED---<3---***")
        message.append("")
        return "\n".join(message)
        # except:
        #     message.append("")
        #     message.append("Exception thrown during structural rule-checking after grading")
        #     return "\n".join(message)
