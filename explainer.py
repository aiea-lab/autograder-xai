from data import data

class Explainer:
    def __init__(self, course, assignment, question):
        self.course = course
        self.assignment = assignment
        self.question = question
        self.messages = []

    # need to also implement the some_info input
    def get_feedback(self, default="TODO"):
        return default + "\n> " + self.get_explanation()
    
    def get_explanation(self, issue_id):
        if issue_id in data:
            return data[issue_id]
        return "sample explanation"