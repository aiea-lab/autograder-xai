class Explainer:
    def __init__(self, course, assignment):
        self.course = course
        self.assignment = assignment
        self.messages = []

    # need to also implement the some_info input
    def get_feedback(self, default="TODO"):
        return default
    
    def add_message(self, message):
        self.messages.append(message)
    
    def print_feedback(self):
        for message in self.messages:
            print(message)