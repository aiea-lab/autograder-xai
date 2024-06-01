from ast_grep_py import SgRoot

class Analysis:
    def __init__(self):
        """
        create a dictionary of format:
           arguments: analysis function to call
        then get_feedback() can just directly call the analysis function directly
        from the dictionary. 
        """
        # format: 'key' : 'function'
        self.function_links = {
            'p0_q1' : self.verify_p0_q1,
            'p0_q2' : self.p0_q2
        }
    def get_feedback(self, key, source):
        """
        The parameter 'key' tells us what analysis function to run
        The parameter 'source' is the submission code
        """
        if key in self.function_links:
            return self.function_links[key](source)
        return "Dynamic feedback implementation not found."

    # Helper Functions
    def enforce_ruleset(self, src: str, rules: list[list[str]]):
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

    # Question Analysis Functions
    def verify_p0_q1(self, src: str):
        """
        Rules:
        for
            increment OR assignment
        return
        """
        # instead of =, use regex to find = or +=
        # =|+=
        loop_increment_rule = ["for", "+="]
        return_rule = ["return"]
        rules = [loop_increment_rule, return_rule]
        return self.enforce_ruleset(src, rules)

    # def p0_q1(self, src):
    #     """
    #     Rules:
    #     for
    #         increment OR assignment
    #     return
    #     """
    #     feedback_start = "Dynamic feedback for p0_q1 begins:\n"
    #     feedback = ""

        
        
    #     if '-' not in feedback:
    #         feedback += "lgtm."
    #     return feedback_start + feedback

    def p0_q2(self, src):
        feedback_start = "Dynamic feedback for p0_q2 begins:\n"
        feedback = "    -Analysis not yet implemented."

        return feedback_start + feedback
    
    def p1_q1(self, src):
        feedback_start = "Dynamic feedback for p1_q1 begins:\n"
        feedback = "    -Analysis not yet implemented."

        return feedback_start + feedback
    
    # Helper Functions
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

