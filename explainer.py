import csv

# by course
# a single analyser can hold all the analysis functions for an course/PA?
#   should instantiate a class by course, e.g. cse140_analyser()
#   which will be stored in a separate file
from autograderXAI import cse140analysis as analysisClass

class Explainer:
    def __init__(self, course, assignment, question, csv_file):
        # Linking question to spreadsheet answer and analysis
        self.course = course
        self.assignment = assignment
        self.question = question
        self.messages = []

        # Spreadsheet (static explanations)
        self.data = {}
        with open(csv_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                key = ('_').join(row[0:3])
                val = row[5]
                self.data[key] = val
        
        # Analysis (dynamic explanations)
        
        self.analyser = analysisClass()

    # need to also implement the some_info input
    def get_feedback(self, default="TODO", issue_id=-1):
        # Dynamic explanation
        key = f"{self.assignment}_{self.question}_{issue_id}"
        dynamic_exp = self.analyser.get_feedback(key, source)
        return default + "\n> " + dynamic_exp
        
        # Static explanation
        # return default + "\n> " + self.get_explanation(issue_id)

    
    def get_explanation(self, issue_id):
        key = f"{self.assignment}_{self.question}_{issue_id}"
        if key in self.data:
            return self.data[key]
        return f"Error: No explanation found for {key}."
    
    def get_data(self):
        return self.data
