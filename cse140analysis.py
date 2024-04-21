import re

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
    def p0_q1(self, source):
        """
        What would be something to check for here, as a proof of concept?
        Break the source down into meaningful chunks, e.g.
        - for loop (if we can't find it; error)
        - increment inside the loop (if we can't find it; error)
        - return statement (if we can't find it; error)
        
        Enforce rules, e.g.
        - increment must be inside for loop
        - return statement must be the very last chunk
        """
        feedback_start = "Dynamic feedback for p0_Q1 begins:\n"
        feedback = ""
        
        # Break into chunks
        chunks = self.chunk_source(source)

        # Create chunk dictionary of format, keyword : order by appearance
        chunk_dict = {
            'return': 'NOT_FOUND',
            'for': 'NOT_FOUND',
            'increment': 'NOT_FOUND',
            # 'unfindable': 'NOT_FOUND'
        }
        for i, chunk in enumerate(chunks):
            if 'return' in chunk:
                chunk_dict['return'] = i
            elif 'for' in chunk:
                chunk_dict['for'] = i
            elif '+' in chunk:
                chunk_dict['increment'] = i
        rules = [
            # format: ({chunk key}, 'before' or 'after', {chunk key} or 'all')
            ('return', 'after', 'for'),
            ('increment', 'after', 'for')
        ]
        # Enforce rules:
        # - Existence rule
        feedback += self.existence_rule(chunk_dict)
        # - Order rule
        feedback += self.order_rule(chunk_dict, rules)
        
        """
        Maybe some application of LLMs would be possible here.
        Like we could have a set of questions corresponding to each question,
        like 'is the return variable incremented in the for loop'

        and see how accurate that is.
        Because writing it out like this is maybe not the most effective or efficient.
        
        Also, this current approach will fail with more complicated functions, i think.
        Like, you can't search properly for a 'for loop' if there are like 3 for loops
        in the code, right? So something would have to change there.
        """
        if '-' not in feedback:
            feedback += "lgtm."
        return feedback_start + feedback

    def p0_q2(self, source):
        feedback_start = "Dynamic feedback for p0_Q2 begins:\n"
        feedback = "    -Analysis not yet implemented."

        return feedback_start + feedback

