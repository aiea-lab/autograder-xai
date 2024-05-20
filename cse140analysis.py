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
            'p0_q1' : self.p0_q1,
            'p0_q2' : self.p0_q2
        }
    def get_feedback(self, key, source):
        """
        The parameter 'key' tells us what analysis function to run
        The parameter 'source' is the code
        
        Currently set to always use p0_Q1() regardless
        """
        if key in self.function_links:
            return self.function_links[key](source)
        else:
            return "Dynamic feedback implementation not found."
        # return self.p0_Q1(source)
        # feedback = f"dynamic feedback for {assignment} and {question}"
        # return feedback

    # Helper Functions
    def chunk_source(self, source):
        """
        Steps:
        - break single source string into a list of lines
        - remove all blank lines
        - remove all single line comments
        - remove all multiline comments 

        what does string.strip() do?
        """
        chunks = source.split("\n")

        # remove all whitespace blank lines
        chunks = [chunk for chunk in chunks if len(chunk) > 0]

        # remove all single line comments
        chunks = [chunk for chunk in chunks if '#' not in chunk]
        
        # remove all multiline comments
        # find an opening """, find a closing """
        # slice away all the lines between them
        on = False
        start = 0
        end = 0
        i = 0
        while i < len(chunks):
        # for i, chunk in enumerate(chunks):
            chunk = chunks[i]
            if '"""' in chunk:
                on = not on

                # If on is true, then we mark start, but should not cut yet
                if on:
                    start = i

                # If on is false, that means we should cut
                else:
                    end = i + 1
                    chunks = chunks[0:start] + chunks[end:]
            i += 1

        return chunks 

    def existence_rule(self, chunk_dict):
        """
        Enforces that every chunk was found in the answer
        """
        feedback = ""
        for key, value in chunk_dict.items():
            if value == 'NOT_FOUND':
                feedback += "   -" + f'{key} chunk not found in source.\n'
        return feedback
    
    def order_rule(self, chunk_dict, rules):
            """
            Enforces rules, adding a message to feedback for each violated rule.
            Rules format: ({chunk key}, 'before' or 'after', {chunk key} or 'all')
            """
            feedback = ""
            for rule in rules:
                prior, condition, post = rule
                if chunk_dict[prior] == 'NOT_FOUND' or chunk_dict[post] == 'NOT_FOUND':
                    continue

                if condition == 'before':
                    if chunk_dict[prior] > chunk_dict[post]:
                        feedback += "   -'" + " ".join(rule) + "' rule violated.\n"
                    else:
                        feedback += "   +'" + " ".join(rule) + "' rule enforced.\n"

                elif condition == 'after':
                    if chunk_dict[prior] < chunk_dict[post]:
                        feedback += "   -'" + " ".join(rule) + "' rule violated.\n"
                    else:
                        feedback += "   +'" + " ".join(rule) + "' rule enforced.\n"
            
            return feedback

    # Question Analysis Functions
    def p0_q1(self, src):
        """
        Rules:
        for
            increment OR assignment
        return
        """
        feedback_start = "Dynamic feedback for p0_q1 begins:\n"
        feedback = ""

        
        
        if '-' not in feedback:
            feedback += "lgtm."
        return feedback_start + feedback

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

