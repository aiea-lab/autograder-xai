class Explainer:
    def __init__(self, course, assignment):
        self.course = course
        self.assignment = assignment

    # need to also implement the some_info input
    def get_feedback(self, default="TODO"):
        return default