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
        split_rule = [ast.Assign, "slogan.split(' ')"]  # uses .split() function on input slogan
        split_adv = "Consider using the built-in '.split()' function to make parsing input easier."
        
        # look for an assign node that then has a bunch of '*'s characters in it. Try to find where the student is creating this. We would try to find an 'assign' character, and then within that line, try to find a 
        # if we can't find it, then we recommend that they create the top and bottom border somewhere. You should be able to derive the length based on the longest word in the group.
        border_rule = [ast.Assign, "*"]  # just the assign isn't enough, need to check for asterisks (this is possible by looking at the string underlying the node.)
        border_adv = "You might want to calculate the length of the top and bottom border all at once. It should be wide enough to fit around the longest word."

        # for the main loop. 
        # -It should iterate through 'words'
        # -check if each word obeys the conditions: not empty, is alphanumeric
        # -assign or aug assign the word and the asterisks to your string solution
        loop_rule = [ast.For, ast.Assign, "*"]
        loop_adv = "You'll probably need to loop through each word in the slogan. Remember to place the needed asterisks around it!"

        # for return at the end
        # -you just gotta make sure to return at the end, that's all.
        return_rule = [ast.Return]
        return_adv = "Remember to return your result at the end!"

        rules = [split_rule, border_rule, loop_rule, return_rule]
        advice = [split_adv, border_adv, loop_adv, return_adv]
        return self.enforce_ruleset(src, rules, advice)
    
    # Traverse the tree and enforce the prescribed rules
    def enforce_ruleset(self, src: str, rules: list[list[type]], advice: list[str]) -> str:
        """ 
        General rule-matching function.
        Parses 'src' as an AST and then checks that each rule in 'rules' is present.
        Reports that all nodes were successfully matched or which node could not be found.
        """

        def unparse(node):
            return f"'{ast.unparse(node)[:30]}...'"

        def check_local_context(sub_tree, sub_rules) -> bool:
            nonlocal local_message_try
            # If there are no rules, there is nothing we have to match; trivial success.
            if len(sub_rules) == 0:
                local_message_try.append("\t-trivially matched all nodes!")
                return True
            
            # Otherwise, we have to step through the sub_tree and try to match all the sub_rules
            rule_counter = 0
            for node in ast.walk(sub_tree):                
                current_rule = sub_rules[rule_counter]
                
                # If current_rule is a string, then we try to match that directly
                if isinstance(current_rule, str):
                    # local_message_try.append(f"{current_rule} is a str type")
                    # local_message_try.append(f"ast.unparse(node): {ast.unparse(node)}")
                    if current_rule in ast.unparse(node):
                        # local_message_try.append(f"\tnode '{current_rule}' matched against '{ast.unparse(node)}'")
                        local_message_try.append(f"\tnode '{current_rule}' matched against '{unparse(node)}'")

                        rule_counter += 1
                # Otherwise, current_rule is a node, then we try to match instead.
                else:
                    if isinstance(node, current_rule):
                        # local_message_try.append(f"\tnode '{current_rule}' matched against '{ast.unparse(node)}'")
                        local_message_try.append(f"\tnode '{current_rule}' matched against '{unparse(node)}'")
                        rule_counter += 1

                # Check if we've matched everything
                if rule_counter >= len(sub_rules):
                    local_message_try.append("\t-matched all nodes!")
                    return True
            
            # If we escape, then report failure with the most recent node we failed to match
            local_message_try.append(f"\t-failed to find match for node '{current_rule}'")
            return False
               
        message = []
        message.append("\n== Structural Explanation")

        
        root = ast.parse(src)
        top_tree_nodes = root.body[0].body

        # Match rulesets against local contexts of top level nodes
        fully_matched_counter = 0
        for i, ruleset in enumerate(rules[:]):
            message.append(f"starting matching for ruleset = {ruleset}")
            
            local_message_max = []
            
            # try to match start of ruleset against top level nodes
            first_rule = ruleset[0]
            for top_node in top_tree_nodes:
                # print(f"top_node:{top_node}; first_rule={first_rule}")
                local_message_try = []
                if isinstance(top_node, first_rule):
                    
                    # local_message_try.append(f"\tmatched against node {top_node}, entering local context")
                    local_message_try.append(f"\tmatched against node {unparse(top_node)}, entering local context")

                    success = check_local_context(top_node, ruleset[1:])
                    # print(f"success state = {success}")

                    # keep a running max for the local message
                    # we want to take the longest one, since that one is the closest match (each element is a matched rule)
                    if success:
                        fully_matched_counter += 1
                        local_message_max = local_message_try
                        break
                    else:
                        local_message_max = local_message_try + [f"\t{advice[i]}"] if len(local_message_try) > len(local_message_max) else local_message_max
            
            # If we failed to match any top-level node
            if not local_message_max:
                message += [f"\tCould not match first rule {first_rule}."]
                message += [f"\t{advice[i]}"]
            else:
                # Finish and add the message that got the furthest
                message += local_message_max
            message += [""]

            # Notes:
            # Maybe we should stop as soon as we failed to match something?
            # Maybe we should only bother adding messages for things we failed to match? 
            #   (if the whole ruleset was go, then it gives no useful information?)
            #   (probably it should stay, though)

        message.append(f"({fully_matched_counter}/{len(rules)} rules matched)")
        if fully_matched_counter < len(rules):
            message.append("***---</3---FAILED TO MATCH ALL RULES---</3---***")
        else:
            message.append("***---<3---MATCHED ALL RULES---<3---***")
        message.append("")
        return "\n".join(message)
        # except:
        #     message.append("")
        #     message.append("Exception thrown during structural rule-checking after grading")
        #     return "\n".join(message)
