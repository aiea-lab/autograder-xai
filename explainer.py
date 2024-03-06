import csv

class Explainer:
    def __init__(self, course, assignment, question, csv_file):
        self.course = course
        self.assignment = assignment
        self.question = question
        self.messages = []
        self.data = {}
        with open(csv_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                key = ('_').join(row[0:3])
                val = row[5]
                self.data[key] = val

    # need to also implement the some_info input
    def get_feedback(self, default="TODO", issue_id=-1):
        return default + "\n> " + self.get_explanation(issue_id)
    
    def get_explanation(self, issue_id):
        key = f"{self.assignment}_{self.question}_{issue_id}"
        if key in self.data:
            return self.data[key]
        return f"Error: No explanation found for {key}."
    
    def get_data(self):
        return self.data
