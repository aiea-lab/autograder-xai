import csv

class Explainer:
    def __init__(self, course, assignment, question, csv_file):
        self.course = course
        self.assignment = assignment
        self.question = question
        self.messages = []
        self.data = []
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.data.append(row)

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

# e = Explainer("cse140", "p0", "q1")
# f = e.get_feedback("ERROR: you failed the example!", 0)
# print(f)