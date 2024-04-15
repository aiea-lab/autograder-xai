class Analysis:
    def __init__(self):
        """
        create a dictionary of format:
           arguments: analysis function to call
        then get_feedback() can just directly call the analysis function directly
        from the dictionary. 
        """
        pass
    def get_feedback(self, key, source):
        # key tells us what analysis function to run
        return self.p0_buyLotsOfFruit(source)
        # feedback = f"dynamic feedback for {assignment} and {question}"
        # return feedback
    
    def p0_buyLotsOfFruit(self, source):
        """
        What would be something to check for here, as a proof of concept?
        Well, how about something pretty simple, like:
            -we update the return value in a loop?
            or maybe that's too complicated
            -we run a for-loop before we return? That's simple.
        """
        feedback = f"dynamic feedback for P0 Q1 'buyLotsOfFruit.'"
        return feedback 